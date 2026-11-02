"""No research mutation; returns a separate immutable writing packet."""
from .contract import envelope, require, digest
from .research import validate_collected

def write(research, history, sections, writer_id="mock-writer-v1"):
    validate_collected(research, history)
    require(writer_id.startswith("mock-writer-"), "WRITER_ID")
    facts = {f["id"]: f for f in research["facts"]}
    require(bool(sections), "EMPTY_ARTICLE")
    require(len({s["claim_id"] for s in sections}) == len(sections), "DUPLICATE_BODY_CLAIM")
    for section in sections:
        require(section["claim_id"] in research["allowed_facts"], "BLOCKED_CLAIM")
        # M1 only: literal evidence rendering, not an LLM or paraphrase verifier.
        require(section["text"] == facts[section["claim_id"]]["text"], "UNBOUND_BODY_TEXT")
    result = envelope(research["article_id"], research["version"])
    result.update(writer_id=writer_id, research_packet_hash=research["research_packet_hash"],
                  provenance_hash=research["provenance_hash"], sections=sections,
                  title=research["title"], body="\n\n".join(s["text"] for s in sections),
                  writing_status="WRITING_COMPLETE", scope="SYNTHETIC_MECHANICAL_RENDER_ONLY")
    result["content_hash"] = digest(result)
    return result
