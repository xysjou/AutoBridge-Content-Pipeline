"""Pinned real-pilot policy, separate from immutable M1 synthetic contracts."""
from datetime import datetime, timezone
import json
from pathlib import Path
from ..contract import BASELINE, PROGRAM, ROOT, RULE_PATHS, canonical, digest, require, rules

SCHEMA = "autobridge-real-pilot/1.0"
REPO = "xysjou/AutoBridge-Content-Pipeline"
BRANCH = "integration/work-cloud-pilot-m1-20261102"
STATE_PATH = "cloud_pilot/state/live-program.json"
CAP = 3_000_000_000  # integer nano USD, for the entire program
AMENDED_CAP = 8_000_000_000
BUDGET_APPROVAL = '批准整个试点累计上限提高到 8 美元。'
BUDGET_APPROVAL_HASH = digest(dict(date='2026-11-03', instruction=BUDGET_APPROVAL,
    program_id=PROGRAM, previous_cap_nano_usd=CAP, cap_nano_usd=AMENDED_CAP))
STAGE_MODELS = {"research": ("gpt-6-luna", "medium"),
                "writing": ("gpt-6.1-terra", "medium"),
                "review": ("gpt-6.1-terra", "high")}
# Standard global endpoint, 30m TTL. All input reserved at LONG 30m write
# rates, using the FULL documented context window (no guessed tokenizer).
RATES = {
    "gpt-6-luna": dict(input=100, cached=10, write=125, output=500,
                       long_input=200, long_cached=20, long_write=250, long_output=750),
    "gpt-6.1-terra": dict(input=1000, cached=50, write=1250, output=5000,
                          long_input=2000, long_cached=100, long_write=2500, long_output=7500),
}
CONTEXT = 1_050_000
MAX_OUTPUT = 8_000
EDITORIAL_MAX_OUTPUT = 24_000

def now():
    return datetime.now(timezone.utc)

def timestamp():
    return now().isoformat()

def read_json(path):
    return json.loads(Path(path).read_text())

def load_rules(include_historical=True):
    from ..multilingual.startup import batch_context,review_context
    # Full authoritative files, not a substitute summary or old chat context.
    from ..multilingual.startup import BATCH_CONTEXT
    current={p:t for p,t in batch_context().items() if not p.endswith('pilot-intake-proposal.json')
             and (include_historical or p in BATCH_CONTEXT)}
    return {**{p: (ROOT / p).read_text() for p in RULE_PATHS},**current,**review_context(),
            '_review_handoff_inventory':{p:digest(t) for p,t in review_context(all_versions=True).items()}}

def validate_prices(snapshot, at=None):
    require(snapshot.get("rates") == RATES, "UNKNOWN_OR_CHANGED_PRICING")
    require(snapshot.get("context") == CONTEXT and snapshot.get("max_output") == MAX_OUTPUT, "TOKEN_LIMIT_SNAPSHOT")
    require(snapshot.get('editorial_max_output') == EDITORIAL_MAX_OUTPUT, 'EDITORIAL_OUTPUT_SNAPSHOT')
    require(snapshot.get("service_tier") == "default" and snapshot.get("cache_ttl") == "30m", "UNSUPPORTED_BILLING_PROFILE")
    verified = datetime.fromisoformat(snapshot["verified_at"])
    require(verified.tzinfo is not None, "PRICE_TIMEZONE")
    age = ((at or now()) - verified).total_seconds()
    require(0 <= age <= 86400, "PRICING_SNAPSHOT_EXPIRED")
    require(snapshot.get("source_urls") and snapshot.get("snapshot_ids") == list(RATES), "PRICE_PROVENANCE_UNKNOWN")
    return digest(snapshot)

def reservation(model,input_bound=None,output_bound=None):
    require(model in RATES, "UNKNOWN_MODEL_PRICE")
    p = RATES[model]
    output_bound=MAX_OUTPUT if output_bound is None else output_bound
    require(type(output_bound) is int and 0<output_bound<=EDITORIAL_MAX_OUTPUT,'INVALID_OUTPUT_BOUND')
    if input_bound is None:return CONTEXT * p["long_write"] + output_bound * p["long_output"]
    require(type(input_bound) is int and 0<input_bound<=CONTEXT,'INVALID_PROVIDER_TOKEN_BOUND')
    prefix='long_' if input_bound>272000 else ''
    return input_bound*p[prefix+'write']+output_bound*p[prefix+'output']

def usage_cost(model, usage):
    require(model in RATES and isinstance(usage, dict), "USAGE_UNKNOWN")
    def count(obj, field):
        n = obj.get(field)
        require(type(n) is int and n >= 0, "USAGE_UNKNOWN:" + field)
        return n
    inputs, outputs = count(usage, "input_tokens"), count(usage, "output_tokens")
    details = usage.get("input_tokens_details", {})
    cached, writes = count(details, "cached_tokens"), count(details, "cache_write_tokens")
    reasoning = count(usage.get("output_tokens_details", {}), "reasoning_tokens")
    require(inputs <= CONTEXT and outputs <= EDITORIAL_MAX_OUTPUT and reasoning <= outputs, "USAGE_OUTSIDE_BOUND")
    require(cached + writes <= inputs, "INVALID_CACHE_USAGE")
    p, prefix = RATES[model], "long_" if inputs > 272000 else ""
    cost = ((inputs-cached-writes)*p[prefix+"input"] + cached*p[prefix+"cached"]
            + writes*p[prefix+"write"] + outputs*p[prefix+"output"])
    require(cost <= reservation(model,output_bound=EDITORIAL_MAX_OUTPUT), "COST_OUTSIDE_RESERVATION")
    return cost

def check_permit(permit, plan, snapshot, code_sha, approval_digest):
    require(isinstance(permit, dict) and permit.get("authorized") is True, "LIVE_NOT_AUTHORIZED")
    require(approval_digest and digest(permit) == approval_digest, "PROTECTED_APPROVAL_MISSING")
    require(permit.get("program_id") == PROGRAM and permit.get("cap_nano_usd") in (CAP, AMENDED_CAP), "APPROVAL_PROGRAM_SCOPE")
    if permit['cap_nano_usd'] == AMENDED_CAP:
        require(permit.get('budget_approval_hash') == BUDGET_APPROVAL_HASH, 'BUDGET_AMENDMENT_APPROVAL_REQUIRED')
    require(permit.get("plan_hash") == digest(plan), "APPROVAL_PLAN_DRIFT")
    require(permit.get("prices_hash") == validate_prices(snapshot), "APPROVAL_PRICE_DRIFT")
    require(permit.get("code_sha") == code_sha and len(code_sha) == 40, "APPROVAL_CODE_DRIFT")
    require(permit.get("baseline_sha") == BASELINE and permit.get("rules") == rules(), "APPROVAL_RULE_DRIFT")
    expiry = datetime.fromisoformat(permit["expires_at"])
    require(expiry.tzinfo and expiry > now(), "APPROVAL_EXPIRED")
    require(permit.get("allowed_models") == list(RATES), "MODEL_AVAILABILITY_UNCONFIRMED")
    require(permit.get("account_models_verified") is True, "MODEL_AVAILABILITY_UNCONFIRMED")
    require(permit.get("protected_runtime_verified") is True, "SECRET_RUNTIME_UNVERIFIED")
    return True
