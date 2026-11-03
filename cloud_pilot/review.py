"""Independent deterministic reviewer, without writer self-evaluation input.

This is mock contract review, NOT independent AI editorial/semantic approval.
"""
import re
from .contract import validate, require, digest, production_gate
from .research import validate_collected

def similarity(a, b):
    def grams(s):
        words = re.findall(r"\w+", s.casefold())
        return {tuple(words[i:i+5]) for i in range(max(0, len(words)-4))}
    x, y = grams(a), grams(b)
    return len(x & y) / len(x | y) if x | y else 0.0

def inspect(article, research, history, prior_bodies=(), reviewer_id="mock-independent-reviewer-v1"):
    validate(article)
    validate_collected(research, history)
    require(reviewer_id.startswith("mock-independent-reviewer-") and reviewer_id != article["writer_id"], "REVIEWER_NOT_INDEPENDENT")
    require("self_evaluation" not in article, "WRITER_EVALUATION_NOT_REVIEW_INPUT")
    expected_hash = digest({k:v for k,v in article.items() if k != "content_hash"})
    require(article["content_hash"] == expected_hash, "CONTENT_HASH_DRIFT")
    require(article["article_id"] == research["article_id"] and article["version"] == research["version"], "ARTICLE_VERSION_DRIFT")
    require(article["title"] == research["title"], "TITLE_BASELINE_DRIFT")
    require(article["research_packet_hash"] == research["research_packet_hash"], "RESEARCH_BASELINE_DRIFT")
    require(article["provenance_hash"] == research["provenance_hash"], "PROVENANCE_DRIFT")
    facts = {f["id"]: f for f in research["facts"]}
    require(article["body"] == "\n\n".join(s["text"] for s in article["sections"]), "UNBOUND_BODY")
    require(len({s["claim_id"] for s in article["sections"]}) == len(article["sections"]), "DUPLICATE_BODY_CLAIM")
    for section in article["sections"]:
        fid = section["claim_id"]
        require(fid in research["allowed_facts"] and section["text"] == facts[fid]["text"], "CLAIM_SOURCE_BINDING_FAIL")
    leakage = re.search(r"Research AI|Writing AI|Review AI|Codex|QA_PASS|PUBLISH_APPROVED|Freeze the scope|Build a primary-evidence ledger", article["body"], re.I)
    require(not leakage, "PUBLIC_WORKFLOW_LEAK")
    require(not re.search(r"we (tested|drove|inspected|imported)", article["body"], re.I), "FAKE_FIRST_HAND")
    maximum = max((similarity(article["body"], b) for b in prior_bodies), default=0)
    decision = "REJECT" if maximum >= .70 else "REVISION_REQUIRED" if maximum > .50 else "MOCK_REVIEW_PASS"
    result = dict(schema_version=article["schema_version"], synthetic=True,
                  reviewer_id=reviewer_id, review_kind="DETERMINISTIC_MOCK_ONLY",
                  article_id=article["article_id"], version=article["version"],
                  content_hash=article["content_hash"], research_packet_hash=research["research_packet_hash"],
                  decision=decision, similarity_max=maximum,
                  english_words=len(re.findall(r"\b[\w'-]+\b", article["body"])),
                  production_gate=production_gate(article), human_reviewed=False, publish_approved=False)
    result["english_length_gate"] = result["english_words"] >= 900
    if not result["english_length_gate"]:
        result["production_gate"]["reasons"].append("EN_BELOW_900_WORDS")
    result["review_hash"] = digest(result)
    return result
