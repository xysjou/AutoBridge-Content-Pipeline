"""Collection/evidence boundary. Only fixture retrieval exists in milestone one."""
from copy import deepcopy
from urllib.parse import urlsplit
import re
from .contract import validate, require, digest, SCOPE

CONFIDENCE = {"VERIFIED", "CROSS_CHECKED", "SINGLE_SOURCE", "CONFLICT", "UNVERIFIED", "TIME_SENSITIVE"}

def normalized(text):
    return " ".join(re.findall(r"\w+", text.casefold()))

def evidence_gate(packet, history):
    validate(packet)
    require(history.get("complete") is True, "HISTORY_UNKNOWN")
    require(history.get("baseline_sha") == packet["baseline_sha"], "HISTORY_DRIFT")
    require(packet.get("research_lock") is False, "RESEARCH_LOCKED")
    require(packet.get("research_status") in ("RESEARCH_PASS", "RESEARCH_CONDITIONAL"), "RESEARCH_FAIL")
    require(packet.get("writing_ai_ready") is True, "WRITER_NOT_READY")
    for key in ("search_intent", "buyer_task", "topic_key", "proposed_url"):
        require(bool(packet.get(key)), "MISSING:" + key)
    require(packet["proposed_url"].startswith("/mock-only/"), "MOCK_URL_NAMESPACE")
    for row in history["entries"]:
        require(row.get("article_id") != packet["article_id"], "ARTICLE_DUPLICATE")
        require(row.get("url") != packet["proposed_url"], "URL_COLLISION")
        require(normalized(row.get("search_intent", "")) != normalized(packet["search_intent"]), "INTENT_DUPLICATE")
        require(row.get("topic_key") != packet["topic_key"], "TOPIC_DUPLICATE")
    sources = {s["id"]: s for s in packet["sources"]}
    facts = {f["id"]: f for f in packet["facts"]}
    require(len(sources) == len(packet["sources"]), "DUPLICATE_SOURCE_ID")
    require(len(facts) == len(packet["facts"]), "DUPLICATE_FACT_ID")
    allowed, blocked = set(packet["allowed_facts"]), set(packet["blocked_facts"])
    require(allowed and allowed <= facts.keys() and not allowed & blocked, "ALLOWED_BLOCKED_CONFLICT")
    used = set()
    for fid in allowed:
        fact = facts[fid]
        require(fact["confidence"] in CONFIDENCE, "CONFIDENCE_INVALID")
        require(fact["confidence"] not in ("CONFLICT", "UNVERIFIED"), "UNVERIFIED_ALLOWED")
        require(bool(fact.get("source_ids")), "NO_SOURCE_BINDING")
        require(all(fact.get(k) for k in SCOPE), "UNLOCKED_FACT_SCOPE")
        matched = []
        for sid in fact["source_ids"]:
            require(sid in sources, "UNKNOWN_SOURCE")
            s = sources[sid]
            require(s.get("synthetic") is True and s.get("access_status") == "FIXTURE_ONLY", "NOT_A_MOCK_SOURCE")
            require(urlsplit(s["url"]).hostname.endswith(".invalid"), "FIXTURE_SOURCE_DOMAIN")
            require(s.get("publisher") == s.get("observed_publisher"), "SOURCE_INTEGRITY_FAIL")
            require(bool(s.get("parent_org")) and bool(s.get("checked_date")), "SOURCE_METADATA_MISSING")
            require(s.get("scope_match") == "MATCHED", "SOURCE_SCOPE_FAIL")
            require(all(s.get(k) == fact[k] for k in SCOPE), "FACT_SCOPE_MISMATCH")
            require(fid in s["supported_facts"] and fact["text"] in s["excerpt"], "NO_DIRECT_SUPPORT")
            require(s.get("official_source") == (s["tier"] == "T1"), "OFFICIAL_SOURCE_COUNT_T1_ONLY")
            matched.append(s)
            used.add(sid)
        if fact["confidence"] == "VERIFIED":
            require(any(s["tier"] == "T1" for s in matched), "PRIMARY_SOURCE_REQUIRED")
        if fact["confidence"] == "CROSS_CHECKED":
            require(len({s["parent_org"] for s in matched if s["tier"] in ("T1", "T2", "T3")}) >= 2, "SAME_FACT_CROSS_CHECK")
        if fact["confidence"] == "TIME_SENSITIVE":
            require(fact.get("current_applicability_verified") is True, "CURRENTNESS_UNKNOWN")
    require(used == sources.keys(), "IRRELEVANT_SOURCE_PADDING")
    source_count = len({s["url"] for s in sources.values()})
    org_count = len({s["parent_org"] for s in sources.values()})
    if packet["research_status"] == "RESEARCH_PASS":
        require(source_count >= 6 and org_count >= 4, "SOURCE_DEPTH_GATE")
    else:
        require(bool(blocked), "CONDITIONAL_NEEDS_BLOCKED_FACTS")
    return {"source_url_count": source_count, "source_org_count": org_count,
            "official_source_count": sum(s["tier"] == "T1" for s in sources.values()),
            "history_hash": digest(history)}

def collect(packet, history):
    result = deepcopy(packet)
    result["research_checks"] = evidence_gate(result, history)
    result["provenance_hash"] = digest({"facts": result["facts"], "sources": result["sources"]})
    result["research_packet_hash"] = digest(result)
    return result

def validate_collected(packet, history):
    raw = {k: v for k, v in packet.items() if k != "research_packet_hash"}
    require(packet.get("research_packet_hash") == digest(raw), "RESEARCH_PACKET_CHANGED")
    require(packet.get("provenance_hash") == digest({"facts":packet["facts"], "sources":packet["sources"]}), "PROVENANCE_CHANGED")
    evidence_gate(packet, history)
