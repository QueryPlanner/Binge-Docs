#!/usr/bin/env python3
"""
collect_markdown_docs.py
------------------------
Quick utility to aggregate a markdown document and all *directly* linked local
markdown files (non-HTTP links) into a single combined markdown file.

Usage
-----
python collect_markdown_docs.py <input_markdown_path> [output_markdown_path]

If *output_markdown_path* is omitted, a file named ``<input_stem>_combined.md``
will be created in the same directory as *input_markdown_path*.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import List, Set

# Regex to match standard markdown links: [text](link)
# We capture the link target and ensure it ends with .md (optionally followed by
# an anchor like #section).
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+?\.md[^)]*)\)")


def extract_markdown_links(markdown: str) -> List[str]:
    """Return a list of markdown link targets found in *markdown* text.

    Only links pointing to ``*.md`` files are returned, and HTTP(S) links are
    ignored.
    """
    links: List[str] = []
    for match in MD_LINK_RE.finditer(markdown):
        target = match.group(1)
        # Skip HTTP URLs completely
        if target.startswith("http://") or target.startswith("https://"):
            continue
        links.append(target)
    return links


def resolve_paths(base: Path, link_targets: List[str]) -> List[Path]:
    """Resolve *link_targets* relative to *base* directory.

    Removes any anchor (``#...``) part from the link. Only existing files are
    returned.
    """
    resolved: List[Path] = []
    seen: Set[Path] = set()
    for target in link_targets:
        # Strip anchor if present
        target_path = target.split("#", 1)[0]
        full_path = (base / target_path).resolve()
        if full_path.is_file() and full_path not in seen:
            resolved.append(full_path)
            seen.add(full_path)
    return resolved


def assemble_documents(main_doc: Path, linked_docs: List[Path]) -> str:
    """Return combined markdown content from *main_doc* and *linked_docs*."""
    sections: List[str] = []

    def add_section(path: Path, title: str) -> None:
        try:
            rel_path_str = str(path.relative_to(main_doc.parent))
        except ValueError:
            # If the path is not a subpath, fall back to a filesystem relative path
            rel_path_str = os.path.relpath(path, start=main_doc.parent)
        sections.append(f"# {title}: {rel_path_str}\n")
        sections.append(path.read_text(encoding="utf-8"))
        sections.append("\n\n")

    add_section(main_doc, "Source")
    for doc in linked_docs:
        add_section(doc, "Included from")

    return "".join(sections)


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help"}:
        print(__doc__)
        sys.exit(0)

    input_path = Path(sys.argv[1]).expanduser().resolve()
    if not input_path.is_file():
        sys.exit(f"Error: '{input_path}' is not a valid file path.")

    output_path: Path
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2]).expanduser().resolve()
    else:
        output_path = input_path.with_name(f"{input_path.stem}_combined.md")

    base_dir = input_path.parent
    markdown_text = input_path.read_text(encoding="utf-8")

    link_targets = extract_markdown_links(markdown_text)
    linked_paths = resolve_paths(base_dir, link_targets)

    combined_markdown = assemble_documents(input_path, linked_paths)
    output_path.write_text(combined_markdown, encoding="utf-8")

    print(f"Combined markdown written to {output_path}")


if __name__ == "__main__":
    main() 