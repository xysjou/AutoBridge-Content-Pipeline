"""One durable real-dollar ledger, with atomic result+cost checkpoints."""
import copy
from ..contract import PROGRAM, BASELINE, digest, canonical, require
from .policy import CAP, AMENDED_CAP, BUDGET_APPROVAL_HASH, SCHEMA, reservation, usage_cost, STATE_PATH, BRANCH

def genesis(mock_hash):
    return dict(schema=SCHEMA, program_id=PROGRAM, cap_nano_usd=CAP, actual_prior_nano_usd=0,
                baseline_sha=BASELINE, m1_mock_journal_hash=mock_hash, events=[])

def replay(data):
    require(data.get("schema") == SCHEMA and data.get("program_id") == PROGRAM, "LEDGER_IDENTITY")
    require(data.get("cap_nano_usd") == CAP and data.get("actual_prior_nano_usd") == 0, "LEDGER_CAP_OR_SEED")
    require(data.get("baseline_sha") == BASELINE and bool(data.get("m1_mock_journal_hash")), "LEDGER_BASELINE")
    view = dict(allocated=0, cap_nano_usd=CAP, operations={}, event_ids={}, checkpoints={}, halts=[])
    previous = digest({k:v for k,v in data.items() if k != "events"})
    for i, e in enumerate(data["events"]):
        require(e["seq"] == i and e["previous"] == previous, "LEDGER_CHAIN")
        require(e["hash"] == digest({k:v for k,v in e.items() if k != "hash"}), "LEDGER_TAMPER")
        require(e["id"] not in view["event_ids"], "LEDGER_DUPLICATE_EVENT")
        p = e["payload"]
        if p["kind"] == "reserve":
            require(not any(o["status"] in ("reserved", "sent", "uncertain") for o in view["operations"].values()), "UNRESOLVED_PROGRAM_CALL")
            require(p["id"] not in view["operations"], "ATTEMPT_ID_REUSE")
            prior = [o for o in view["operations"].values() if o["operation"] == p["operation"]]
            require(len(prior) < 3 and p["attempt"] == len(prior)+1, "MAX_THREE_ATTEMPTS_OR_SEQUENCE")
            require(not any(o["status"] == "completed" for o in prior), "COMPLETED_NOT_RETRYABLE")
            require(all(o["request_hash"] == p["request_hash"] for o in prior), "RETRY_REQUEST_DRIFT")
            require(p["amount"] == reservation(p["model"],p.get('input_bound'),p.get('output_bound')), "RESERVATION_PRICE_MISMATCH")
            if 'input_bound' in p:require(p.get('token_count_hash') and p.get('counted_request_hash')==p['request_hash'],'PROVIDER_COUNT_BINDING')
            require(view["allocated"] + p["amount"] <= view['cap_nano_usd'], "PROGRAM_CAP_EXCEEDED")
            require(p.get("price_hash") and p.get("request_hash"), "RESERVATION_PROVENANCE")
            view["allocated"] += p["amount"]
            view["operations"][p["id"]] = dict(p, status="reserved")
        elif p['kind'] == 'budget_amendment':
            require(view['cap_nano_usd'] == CAP and p.get('previous_cap_nano_usd') == CAP
                    and p.get('cap_nano_usd') == AMENDED_CAP
                    and p.get('approval_hash') == BUDGET_APPROVAL_HASH, 'INVALID_BUDGET_AMENDMENT')
            require(not any(o['status'] in ('reserved','sent','uncertain') for o in view['operations'].values()),
                    'UNRESOLVED_PROGRAM_CALL')
            require(p.get('settled_nano_usd') == view['allocated'], 'BUDGET_AMENDMENT_SPEND_DRIFT')
            view['cap_nano_usd'] = AMENDED_CAP
        elif p["kind"] == "sent":
            o = view["operations"][p["id"]]
            require(o["status"] == "reserved", "ALREADY_SENT")
            o["status"] = "sent"
        elif p["kind"] == "result":
            o = view["operations"][p["id"]]
            require(o["status"] == "sent", "RESULT_WITHOUT_SEND")
            require(p["response"].get("model") == o["model"], "RESPONSE_MODEL_DRIFT")
            cost = usage_cost(o["model"], p["response"].get("usage"))
            require(p['response']['usage']['output_tokens']<=o.get('output_bound',8000),'USAGE_EXCEEDS_OUTPUT_BOUND')
            if 'input_bound' in o:require(p['response']['usage']['input_tokens']<=o['input_bound'],'USAGE_EXCEEDS_PROVIDER_COUNT')
            require(cost<=o['amount'],'COST_EXCEEDS_RESERVATION')
            require(p["cost"] == cost, "SETTLEMENT_COST_MISMATCH")
            view["allocated"] -= o["amount"] - cost
            o.update(status="completed", cost=cost, response=p["response"])
        elif p["kind"] == "uncertain":
            o = view["operations"][p["id"]]
            require(o["status"] in ("sent", "reserved"), "UNCERTAIN_INVALID_STATE")
            o.update(status="uncertain", reason=p["reason"])
        elif p["kind"] == "checkpoint":
            key = p["key"]
            require(key not in view["checkpoints"], "IMMUTABLE_CHECKPOINT")
            require(p["artifact_hash"] == digest(p["artifact"]), "CHECKPOINT_HASH")
            view["checkpoints"][key] = p["artifact"]
        elif p["kind"] == "halt":
            require(p['stage'] in ('source','research','writing','review','delivery'),'HALT_STAGE')
            require(p.get('article_id') and 1<=p.get('version',0)<=3 and p.get('reason'),'HALT_RECORD')
            view['halts'].append(p)
        elif p["kind"] == "reconcile":
            o=view["operations"][p["id"]]
            require(o["status"] in ("reserved","sent","uncertain"), "NOT_UNCERTAIN")
            require(p.get("operator_approval_hash") and p.get("provider_evidence_hash"), "RECONCILIATION_EVIDENCE_REQUIRED")
            require(p.get("request_proven_not_sent") is True and o["status"] == "reserved", "NO_AUTOMATIC_RELEASE_AFTER_SEND")
            # Only a crash before durable 'sent' can be proved not transmitted.
            view["allocated"] -= o["amount"]
            o["status"] = "not_sent"
        else:
            require(False, "UNKNOWN_LEDGER_EVENT")
        view["event_ids"][e["id"]] = p
        previous = e["hash"]
    require(view["allocated"] <= view['cap_nano_usd'], "PROGRAM_CAP_EXCEEDED")
    view["head"] = previous
    return view

def append(data, event_id, payload):
    view = replay(data)
    if event_id in view["event_ids"]:
        require(view["event_ids"][event_id] == payload, "IDEMPOTENCY_PAYLOAD_CONFLICT")
        return data
    out=copy.deepcopy(data)
    event=dict(id=event_id, seq=len(out["events"]), previous=view["head"], payload=payload)
    event["hash"]=digest(event)
    out["events"].append(event)
    replay(out)
    require(len(canonical(out).encode()) <= 800000, "LEDGER_SIZE_LIMIT")
    return out

class Journal:
    def __init__(self, store):
        self.store=store

    def read(self):
        data, token=self.store.read()
        return data, token, replay(data)

    def commit(self, event_id, payload):
        data, token, _=self.read()
        updated=append(data,event_id,payload)
        if updated != data:
            self.store.cas(token,updated)  # conflict: no model call, no blind retry

    def checkpoint(self, key, artifact):
        if hasattr(self.store,'save_artifact'):
            artifact=self.store.save_artifact(artifact)
        self.commit('checkpoint:'+key,dict(kind='checkpoint',key=key,artifact=artifact,artifact_hash=digest(artifact)))

    def get_checkpoint(self,key):
        value=self.read()[2]['checkpoints'].get(key)
        if isinstance(value,dict) and value.get('_immutable_artifact_ref'):
            require(hasattr(self.store,'load_artifact'),'ARTIFACT_STORE_REQUIRED')
            return self.store.load_artifact(value)
        return value

    def halt(self,article_id,stage,version,reason):
        payload=dict(kind='halt',article_id=article_id,stage=stage,version=version,reason=reason)
        self.commit('halt:'+digest(payload),payload)

class GitHubStore:
    path=STATE_PATH
    branch=BRANCH

    def __init__(self, transport):
        self.transport=transport

    def read(self):
        data, sha=self.transport.read(self.branch,self.path)
        require(sha, "GITHUB_LEDGER_UNKNOWN")
        replay(data)
        return data,sha

    def cas(self, expected, data):
        replay(data)
        old, actual=self.read()
        require(actual == expected, "CAS_CONFLICT")
        require({k:v for k,v in data.items() if k!='events'} == {k:v for k,v in old.items() if k!='events'}, "LEDGER_HEADER_REWRITE")
        require(data['events'][:len(old['events'])] == old['events'], "LEDGER_HISTORY_REWRITE")
        return self.transport.replace(self.branch,self.path,expected,data)

    def save_artifact(self,artifact):
        body=(canonical(artifact)+'\n').encode()
        require(len(body)<=800000,'CHECKPOINT_ARTIFACT_TOO_LARGE')
        h=digest(artifact)
        path='cloud_pilot/live_artifacts/checkpoints/'+h+'.json'
        sha=self.transport.put_immutable(self.branch,path,body)
        return dict(_immutable_artifact_ref=True,path=path,blob_sha=sha,content_hash=h)

    def load_artifact(self,reference):
        data,sha=self.transport.read_artifact(self.branch,reference['path'])
        require(sha==reference['blob_sha'] and digest(data)==reference['content_hash'],'IMMUTABLE_ARTIFACT_DRIFT')
        return data
