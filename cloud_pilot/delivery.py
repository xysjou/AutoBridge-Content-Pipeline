"""Orchestrator/draft-PR contract; never writes production paths or CURRENT."""
from .contract import require, digest, production_gate
from .research import collect
from .writing import write
from .review import inspect
from .state import transact
from .budget import reserve, settle

def draft_pr_request(article, review, base, head):
    require(base.startswith(("feature/work-cloud-pilot-", "integration/work-cloud-pilot-")), "ISOLATED_BASE_REQUIRED")
    require(head.startswith(("feature/work-cloud-pilot-", "integration/work-cloud-pilot-")) and head != base, "ISOLATED_HEAD_REQUIRED")
    require(review["content_hash"] == article["content_hash"], "STALE_REVIEW")
    require(review["review_hash"] == digest({k:v for k,v in review.items() if k != "review_hash"}), "REVIEW_TAMPERED")
    require(review["decision"] == "MOCK_REVIEW_PASS", "REVIEW_NOT_PASSED")
    require(review["reviewer_id"] != article["writer_id"], "SELF_REVIEW")
    require(production_gate(article)["eligible"] is False, "PRODUCTION_DISABLED")
    return dict(draft=True, base=base, head=head, article_id=article["article_id"],
                content_hash=article["content_hash"], review_hash=review["review_hash"],
                title="[SYNTHETIC MOCK] " + article["title"],
                publish_approved=False, human_reviewed=False, current_promotion=False,
                allowed_prefix="cloud_pilot/", idempotency_key=digest([article["article_id"], article["version"], article["content_hash"]]))

def run_one(packet, history, store, prior_bodies=()):
    aid, version = packet["article_id"], packet["version"]
    def transition(status, h):
        transact(store, f"{aid}:v{version}:{status}", dict(kind="transition", article_id=aid,
                 version=version, status=status, artifact_hash=h))
    try:
        research = collect(packet, history)
    except ValueError:
        transition("RESEARCH_FAILED", digest(packet))
        raise
    transition("RESEARCH_READY", research["research_packet_hash"])
    # Three labelled simulated model stages exercise the *same* program budget.
    for role, model in (("research", "gpt-6-luna"), ("writing", "gpt-6.1-terra"), ("review", "gpt-6.1-terra")):
        rid = reserve(store, f"{aid}:v{version}:{role}", 1, model, 20000, 6000)
        settle(store, rid, "success", dict(input_tokens=1000, output_tokens=500,
                  reasoning_tokens=100, cached_input_tokens=0, cache_write_tokens=0))
    sections = [{"claim_id": f["id"], "text": f["text"]} for f in research["facts"] if f["id"] in research["allowed_facts"]]
    article = write(research, history, sections)
    transition("WRITTEN", article["content_hash"])
    review = inspect(article, research, history, prior_bodies)
    status = "REJECTED" if review["decision"] == "REJECT" else review["decision"]
    transition(status, article["content_hash"])
    require(status == "MOCK_REVIEW_PASS", "REVIEW_REQUIRES_REPAIR")
    request = draft_pr_request(article, review, "integration/work-cloud-pilot-m1-20261102", "feature/work-cloud-pilot-mock-articles")
    transition("DRAFT_PR_PREPARED", article["content_hash"])
    return dict(research=research, article=article, review=review, draft_pr_request=request)
