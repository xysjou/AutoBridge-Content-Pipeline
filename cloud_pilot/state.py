"""Append-only, hash-chained program journal with optimistic compare-and-swap.

LocalFileCAS is an offline simulator. GitHubCAS accepts a minimal Contents API
transport (read, replace-with-blob-SHA). No implicit network/client/credentials.
"""
import copy
import fcntl
import json
import os
from pathlib import Path
from .contract import PROGRAM, SCHEMA, require, digest, canonical

CAP_NANO_USD = 3_000_000_000
TRANSITIONS = {
    "NEW": {"RESEARCH_READY", "RESEARCH_FAILED"},
    "RESEARCH_FAILED": {"RESEARCH_READY", "REJECTED"},
    "RESEARCH_READY": {"WRITTEN", "RESEARCH_FAILED"},
    "WRITTEN": {"MOCK_REVIEW_PASS", "REVISION_REQUIRED", "NEEDS_RESEARCH", "REJECTED"},
    "REVISION_REQUIRED": {"RESEARCH_READY", "REJECTED"},
    "NEEDS_RESEARCH": {"RESEARCH_READY", "RESEARCH_FAILED", "REJECTED"},
    "MOCK_REVIEW_PASS": {"DRAFT_PR_PREPARED"},
    "DRAFT_PR_PREPARED": set(), "REJECTED": set(),
}

def empty():
    return dict(schema_version=SCHEMA, program_id=PROGRAM, mode="mock",
                cap_nano_usd=CAP_NANO_USD, events=[])

def replay(journal):
    require(journal.get("schema_version") == SCHEMA and journal.get("program_id") == PROGRAM, "STATE_IDENTITY")
    require(journal.get("mode") == "mock" and journal.get("cap_nano_usd") == CAP_NANO_USD, "STATE_BUDGET_CONFIG")
    view = dict(items={}, reservations={}, ids={}, allocated=0)
    previous = digest({k:v for k,v in journal.items() if k != "events"})
    for index, event in enumerate(journal["events"]):
        require(event["seq"] == index and event["previous"] == previous, "JOURNAL_CHAIN")
        require(event["hash"] == digest({k:v for k,v in event.items() if k != "hash"}), "JOURNAL_HASH")
        require(event["id"] not in view["ids"], "DUPLICATE_EVENT_ID")
        apply(view, event["payload"])
        view["ids"][event["id"]] = event["payload"]
        previous = event["hash"]
    view["head"] = previous
    return view

def integer(value):
    return type(value) is int and value >= 0

def apply(view, p):
    kind = p["kind"]
    if kind == "transition":
        aid, target = p["article_id"], p["status"]
        old = view["items"].get(aid, {"status":"NEW", "revision":0, "version":1})
        require(target in TRANSITIONS.get(old["status"], set()), "INVALID_TRANSITION")
        revision = old["revision"] + (target == "RESEARCH_READY" and old["status"] in ("REVISION_REQUIRED", "NEEDS_RESEARCH"))
        require(revision <= 2, "MAX_TWO_REVISIONS")
        require(p["version"] == revision + 1, "VERSION_SEQUENCE")
        require(bool(p.get("artifact_hash")), "ARTIFACT_BINDING_MISSING")
        if target in ("MOCK_REVIEW_PASS", "DRAFT_PR_PREPARED"):
            require(p["artifact_hash"] == old["artifact_hash"], "REVIEW_CONTENT_DRIFT")
        view["items"][aid] = dict(status=target, revision=revision, version=p["version"], artifact_hash=p["artifact_hash"])
    elif kind == "reserve":
        require(p.get("mock") is True, "REAL_COST_DISABLED")
        require(p["reservation_id"] not in view["reservations"], "RESERVATION_REUSED")
        require(integer(p["amount"]) and p["amount"] > 0, "INVALID_RESERVATION")
        require(view["allocated"] + p["amount"] <= CAP_NANO_USD, "PROGRAM_CAP_EXCEEDED")
        attempts = [v for v in view["reservations"].values() if v["operation_id"] == p["operation_id"]]
        require(len(attempts) < 3, "MAX_ATTEMPTS")
        require(p["attempt"] == len(attempts) + 1, "ATTEMPT_SEQUENCE")
        require(not any(a["status"] == "success" for a in attempts), "SUCCESS_NOT_RETRYABLE")
        require(not any(a["status"] in ("uncertain", "unknown_usage") for a in view["reservations"].values()), "PROGRAM_USAGE_UNKNOWN")
        require(not any(a["status"] == "reserved" for a in attempts), "UNRESOLVED_ATTEMPT")
        view["allocated"] += p["amount"]
        view["reservations"][p["reservation_id"]] = dict(p, status="reserved")
    elif kind == "settle":
        require(p["reservation_id"] in view["reservations"], "UNKNOWN_RESERVATION")
        r = view["reservations"][p["reservation_id"]]
        require(r["status"] == "reserved", "ALREADY_SETTLED")
        require(p["outcome"] in ("success", "known_failure", "uncertain", "unknown_usage"), "INVALID_OUTCOME")
        actual = p.get("actual")
        if p["outcome"] in ("uncertain", "unknown_usage"):
            require(actual is None, "UNCERTAIN_COST_MUST_STAY_RESERVED")
        else:
            require(integer(actual) and actual <= r["amount"], "USAGE_EXCEEDS_RESERVATION")
            view["allocated"] -= r["amount"] - actual
        r.update(status=p["outcome"], actual=actual, usage=p.get("usage"))
    else:
        require(False, "UNKNOWN_EVENT")

def append(journal, event_id, payload):
    view = replay(journal)
    if event_id in view["ids"]:
        require(view["ids"][event_id] == payload, "IDEMPOTENCY_CONFLICT")
        return journal
    result = copy.deepcopy(journal)
    event = dict(id=event_id, seq=len(result["events"]), previous=view["head"], payload=payload)
    event["hash"] = digest(event)
    result["events"].append(event)
    replay(result)
    return result

class LocalFileCAS:
    def __init__(self, path):
        self.path = Path(path)

    def initialize(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("x") as stream:
            stream.write(canonical(empty()))

    def read(self):
        require(self.path.is_file(), "STATE_UNKNOWN_NO_AUTO_RESET")
        data = json.loads(self.path.read_text())
        replay(data)
        return data, digest(data)

    def cas(self, expected, data):
        replay(data)
        with self.path.with_suffix(".lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            old, actual = self.read()
            require(actual == expected, "CAS_CONFLICT")
            require(data["events"][:len(old["events"])] == old["events"], "HISTORY_REWRITE")
            temp = self.path.with_suffix(".tmp")
            with temp.open("w") as stream:
                stream.write(canonical(data)); stream.flush(); os.fsync(stream.fileno())
            os.replace(temp, self.path)
            return digest(data)

class GitHubCAS:
    # Fixed namespace prevents accidental budgets split by article/run/chat.
    path = "cloud_pilot/state/program-journal.json"
    branch = "integration/work-cloud-pilot-m1-20261102"

    def __init__(self, transport):
        self.transport = transport

    def read(self):
        data, blob_sha = self.transport.read(self.branch, self.path)
        require(bool(blob_sha), "GITHUB_STATE_UNKNOWN")
        replay(data)
        return data, blob_sha

    def cas(self, expected, data):
        old, actual = self.read()
        require(actual == expected, "CAS_CONFLICT")
        require(data["events"][:len(old["events"])] == old["events"], "HISTORY_REWRITE")
        replay(data)
        # The transport MUST use the Contents API sha precondition. A ref GET
        # followed by an unconditional PUT is not a valid implementation.
        return self.transport.replace(self.branch, self.path, expected, data)

def transact(store, event_id, payload):
    old, token = store.read()
    new = append(old, event_id, payload)
    if new == old:
        return token
    # No silent CAS retry: reread and recalculate the budget after a collision.
    return store.cas(token, new)
