"""Mock-only conservative spending controller. All money uses integer nanodollars."""
from .contract import require, digest
from .state import transact

PRICES = {
    "gpt-6.1-terra": {"input": 1000, "output": 5000, "input_ceiling": 2500},
    "gpt-6-luna": {"input": 100, "output": 500, "input_ceiling": 250},
}
PRICE_VERSION = "official-standard-short-2026-11-02-v1"

def reserve(store, operation_id, attempt, model, max_input, max_output):
    require(model in PRICES, "UNKNOWN_PRICE")
    require(type(max_input) is int and 0 < max_input <= 20000, "INPUT_LIMIT")
    require(type(max_output) is int and 0 < max_output <= 6000, "OUTPUT_LIMIT")
    require(type(attempt) is int and 1 <= attempt <= 3, "MAX_ATTEMPTS")
    price = PRICES[model]
    rid = digest([operation_id, attempt, model, PRICE_VERSION])
    payload = dict(kind="reserve", reservation_id=rid, operation_id=operation_id,
                   attempt=attempt, model=model, mock=True, price_version=PRICE_VERSION,
                   max_input=max_input, max_output=max_output,
                   amount=max_input*price["input_ceiling"] + max_output*price["output"])
    transact(store, "reserve:"+rid, payload)
    return rid

def settle(store, rid, outcome, usage=None):
    from .state import replay
    state, _ = store.read()
    r = replay(state)["reservations"].get(rid)
    require(r is not None, "UNKNOWN_RESERVATION")
    actual = None
    if outcome in ("success", "known_failure"):
        require(isinstance(usage, dict), "USAGE_UNKNOWN")
        for k in ("input_tokens", "output_tokens", "reasoning_tokens", "cached_input_tokens", "cache_write_tokens"):
            require(type(usage.get(k)) is int and usage[k] >= 0, "USAGE_UNKNOWN:"+k)
        require(usage["reasoning_tokens"] <= usage["output_tokens"], "REASONING_SUBSET")
        require(usage["cached_input_tokens"] + usage["cache_write_tokens"] <= usage["input_tokens"], "CACHE_SUBSET")
        require(usage["input_tokens"] <= r["max_input"] and usage["output_tokens"] <= r["max_output"], "TOKEN_BOUND_EXCEEDED")
        # Do not double-count reasoning (already a subset of output_tokens).
        # Charge all input at the reserved highest cache-write rate: conservative.
        p = PRICES[r["model"]]
        actual = usage["input_tokens"]*p["input_ceiling"] + usage["output_tokens"]*p["output"]
    transact(store, "settle:"+rid, dict(kind="settle", reservation_id=rid,
             outcome=outcome, actual=actual, usage=usage, mock=True))
