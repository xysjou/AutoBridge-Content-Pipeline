#!/usr/bin/env python3
"""Export DOCX files to reviewable Markdown without changing article text."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph


def escape_cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")


def paragraph_markdown(paragraph: Paragraph) -> str:
    text = paragraph.text.strip()
    if not text:
        return ""

    style_name = paragraph.style.name if paragraph.style else ""
    if style_name.startswith("Heading "):
        try:
            level = min(max(int(style_name.split()[-1]), 1), 6)
        except ValueError:
            level = 2
        return f"{'#' * level} {text}"

    if style_name.startswith("List"):
        return f"- {text}"

    return text


def table_markdown(table: Table) -> str:
    rows = [[escape_cell(cell.text) for cell in row.cells] for row in table.rows]
    if not rows:
        return ""

    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    lines = [
        "| " + " | ".join(rows[0]) + " |",
        "| " + " | ".join(["---"] * width) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows[1:])
    return "\n".join(lines)


def export_docx(source: Path, destination: Path) -> None:
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    document = Document(source)
    blocks = [
        "<!-- Mechanical DOCX export for independent review. -->",
        f"<!-- Source file: {source.name} -->",
        f"<!-- Source SHA-256: {digest} -->",
    ]

    for item in document.iter_inner_content():
        if isinstance(item, Paragraph):
            rendered = paragraph_markdown(item)
        elif isinstance(item, Table):
            rendered = table_markdown(item)
        else:
            rendered = ""
        if rendered:
            blocks.append(rendered)

    destination.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()

    args.destination.mkdir(parents=True, exist_ok=True)
    sources = sorted(args.source.glob("*.docx"))
    if not sources:
        raise SystemExit(f"No DOCX files found in {args.source}")

    for source in sources:
        export_docx(source, args.destination / f"{source.stem}.md")

    print(f"Exported {len(sources)} DOCX files to {args.destination}")


if __name__ == "__main__":
    main()
