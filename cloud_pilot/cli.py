"""Offline process boundaries. Run `python -m cloud_pilot.cli --help`."""
import argparse
import json
from pathlib import Path
from .contract import require, ROOT, canonical
from .research import collect
from .writing import write
from .review import inspect

def load(path):
    return json.loads(Path(path).read_text())

def save_new(path, data):
    p = Path(path).resolve()
    require(p.is_relative_to(ROOT / "cloud_pilot"), "OUTPUT_OUTSIDE_PILOT")
    p.parent.mkdir(parents=True, exist_ok=True)
    content = canonical(data) + "\n"
    if p.exists():
        require(p.read_text() == content, "IMMUTABLE_ARTIFACT_EXISTS")
        return
    with p.open("x") as stream:
        stream.write(content)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["research", "writing", "review"])
    parser.add_argument("--input", required=True)
    parser.add_argument("--history", required=True)
    parser.add_argument("--research")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    packet, history = load(args.input), load(args.history)
    if args.stage == "research":
        result = collect(packet, history)
    elif args.stage == "writing":
        sections = [{"claim_id":f["id"], "text":f["text"]} for f in packet["facts"] if f["id"] in packet["allowed_facts"]]
        result = write(packet, history, sections)
    else:
        require(bool(args.research), "RESEARCH_INPUT_REQUIRED")
        result = inspect(packet, load(args.research), history)
    save_new(args.output, result)

if __name__ == "__main__":
    main()
