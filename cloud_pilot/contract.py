"""Versioned wire contract; JSON packets are the only inter-stage context."""
import hashlib
import json
import re
from pathlib import Path

SCHEMA = "autobridge-cloud-pilot/1.0"
PROGRAM = "autobridge-two-en-pilot-20261102"
BASELINE = "92e97312f1f225023bd663ada41dfadfc9bfd848"
ROOT = Path(__file__).resolve().parent.parent
SCOPE = ("market", "model_year", "generation", "trim", "powertrain", "test_cycle")
RULE_PATHS = (
    "skills/README.md", "skills/autobridge-research/SKILL.md",
    "skills/autobridge-writing/SKILL.md", "LESSONS_LEARNED.md", "VERSIONING.md",
    "reviews/2026-09-06/review_handoff_20260902_20260905_5d167bef_GATE.json",
    "reviews/site-pilot-11-20260909/WRITING_V4_HANDOFF_20260912.json",
)

class GateError(ValueError):
    pass

def require(ok, message):
    if not ok:
        raise GateError(message)

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def rules(root=ROOT):
    return {p: file_hash(root / p) for p in RULE_PATHS}

def envelope(article_id, version=1):
    return dict(schema_version=SCHEMA, program_id=PROGRAM, article_id=article_id,
                version=version, synthetic=True, locale="en", baseline_sha=BASELINE,
                rules=rules(), rule_versions={"research": "1.1", "writing": "1.3"},
                human_reviewed=False, publish_approved=False, first_hand=False)

def validate(packet):
    require(packet.get("schema_version") == SCHEMA, "UNKNOWN_SCHEMA")
    require(packet.get("program_id") == PROGRAM, "PROGRAM_MISMATCH")
    require(packet.get("synthetic") is True, "REAL_CONTENT_DISABLED")
    require(packet.get("locale") == "en", "EN_ONLY_PILOT")
    require(re.fullmatch(r"MOCK-[A-Z0-9-]+", packet.get("article_id", "")), "INVALID_ID")
    require(type(packet.get("version")) is int and 1 <= packet["version"] <= 3, "MAX_TWO_REVISIONS")
    require(packet.get("baseline_sha") == BASELINE, "BASELINE_DRIFT")
    require(packet.get("rules") == rules(), "RULE_DRIFT")
    require(packet.get("rule_versions") == {"research": "1.1", "writing": "1.3"}, "RULE_VERSION")
    for flag in ("human_reviewed", "publish_approved", "first_hand"):
        require(packet.get(flag) is False, "FORBIDDEN_APPROVAL:" + flag)

def production_gate(packet):
    validate(packet)
    # No synthetic, English-only packet can ever satisfy the 12-language gate.
    return {"eligible": False, "reasons": ["SYNTHETIC", "EN_ONLY", "NO_HUMAN_APPROVAL",
            "NO_IMAGE_RIGHTS_REVIEW", "NO_INDEPENDENT_SEMANTIC_REVIEW"]}
