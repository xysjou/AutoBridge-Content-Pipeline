# Article Versioning Policy

Each article is versioned independently.

- Existing version folders are immutable.
- A modification creates the next version: `v1` -> `v2` -> `v3`.
- Never overwrite `versions/vN/`.
- `CURRENT` contains the active version name.
- Batch manifests point to each article's current version.
- Git history is an additional audit trail, not a replacement for article version folders.

Example:

```text
batches/<batch_id>/articles/<article_id>/
  CURRENT
  versions/
    v1/
      article.md
      version.json
    v2/
      article.md
      version.json
```
