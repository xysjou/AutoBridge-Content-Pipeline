# Work Cloud first milestone — synthetic only

This package is an isolated engineering prototype, not a replacement for the
repository's Research/Writing Skills or a production authoring system. Existing
content, CURRENT pointers, workflows and site settings remain unchanged.

Four modules exchange versioned JSON packets: `research.py` -> `writing.py` ->
`review.py` -> `delivery.py`. The reviewer recomputes evidence/content checks and
accepts no writer self-evaluation. Its identity is a deterministic mock worker,
not an independent AI or human. The two short English fixtures intentionally fail
the formal 900-word and 12-language gates. All source publishers, vehicles and
`.invalid` URLs are synthetic. `MOCK_REVIEW_PASS` means a contract test passed.

Run from the repository root (Python 3.11+, standard library only):

```sh
python -m unittest discover -s cloud_pilot/tests -v
python -m cloud_pilot.pilot --verify
```

`python -m cloud_pilot.pilot` creates missing immutable mock artifacts only.
It never resets committed state. `--verify` reproduces in a temporary offline
store, compares every output, and checks every original tracked file's blob hash.

See [audit](docs/AUDIT.md), [design and limitations](docs/DESIGN.md),
[official model/pricing snapshot](docs/OPENAI.md), and
[next-stage key/approval gate](docs/NEXT_GATE.md).
