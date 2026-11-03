"""Read tracked baseline files; emit exact inventory without modifying them."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import subprocess
from .contract import BASELINE, ROOT, digest, rules

def inventory(root=ROOT):
    raw = subprocess.check_output(["git", "ls-tree", "-rz", "--long", BASELINE], cwd=root)
    rows = []
    for record in raw.decode().split("\0"):
        if not record:
            continue
        meta, path = record.split("\t", 1)
        mode, kind, blob, size = meta.split()
        rows.append(dict(path=path, blob_sha=blob, bytes=int(size), mode=mode))
    current = []
    for row in rows:
        if row["path"].endswith("/CURRENT"):
            p = root / row["path"]
            version = p.read_text().strip()
            target = p.parent / "versions" / (version + ".md")
            current.append(dict(path=row["path"], version=version, target=str(target.relative_to(root)), exists=target.is_file()))
    return dict(baseline_sha=BASELINE, total_files=len(rows),
                counts=dict(Counter(r["path"].split("/")[0] for r in rows)),
                versions=sum("/versions/" in r["path"] for r in rows),
                current_pointers=current, files=rows, rules=rules(root))

def history_snapshot(root=ROOT):
    inv = inventory(root)
    entries, documents = [], []
    def walk(obj):
        if isinstance(obj, dict):
            if any(k in obj for k in ("article_id", "search_intent", "SEARCH_INTENT", "slug", "suggested_url", "model_key")):
                entries.append(dict(article_id=obj.get("article_id", obj.get("ARTICLE_ID", "")),
                    search_intent=obj.get("search_intent", obj.get("SEARCH_INTENT", "")),
                    url=obj.get("slug", obj.get("suggested_url", "")),
                    topic_key=obj.get("model_key", obj.get("topic_cluster", ""))))
            for value in obj.values():
                walk(value)
        elif isinstance(obj, list):
            for value in obj:
                walk(value)
    for row in inv["files"]:
        path = row["path"]
        if path.split("/")[0] not in ("batches", "daily", "incoming", "state", "reviews", "reports", "deliveries"):
            continue
        if path.endswith(".json"):
            walk(json.loads((root / path).read_text()))
        if path.endswith(".md"):
            documents.append(dict(path=path, sha256=hashlib.sha256((root / path).read_bytes()).hexdigest()))
    # Complete structural scan, not a semantic adjudication of old unstructured topics.
    return dict(complete=True, coverage="STRUCTURAL_INDEX_ONLY_REAL_SEMANTIC_DEDUP_PENDING",
                baseline_sha=BASELINE, entries=entries, documents=documents)

def preserved(root=ROOT):
    changed = []
    for row in inventory(root)["files"]:
        p = root / row["path"]
        if not p.is_file():
            changed.append(row["path"]); continue
        body = p.read_bytes()
        oid = hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()
        if oid != row["blob_sha"]:
            changed.append(row["path"])
    return changed
