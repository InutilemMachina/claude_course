"""
15_backlog_index.py -- Nyitott pontok aggregátor (read-only nézet).

Az Instructions §11.1 elvét automatizálja: "lokálisan írni, centralizáltan
olvasni". Végigmegy a meta-fájlok `## Nyitott pontok` szekcióin és a skillek
`## 8. Visszajelzések` NYITOTT tételein (🔲 TODO / ❔ QUESTION / ⚠️ WARNING),
és egyetlen összesítő nézetet ad.

A ✅ KÉSZ és 💬 NOTE tételeket kihagyja (nem nyitott teendők).

Read-only: nem módosít semmit, csak riportot ír (stdout vagy --md).

Usage:
    python scripts/15_backlog_index.py
    python scripts/15_backlog_index.py --md > backlog_snapshot.md
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from _encoding_fix import fix_stdout as _fix_stdout
    _fix_stdout()
except ImportError:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Open-item markers (nyitott teendők). ✅ és 💬 NEM nyitott.
OPEN_MARKERS = ("🔲", "❔", "⚠️")


def extract_open_points_section(text: str) -> list[str]:
    """Return list items under a '## Nyitott pontok' heading (meta-files)."""
    items = []
    lines = text.splitlines()
    in_section = False
    for line in lines:
        s = line.strip()
        if re.match(r'^##\s+Nyitott pontok\s*$', s):
            in_section = True
            continue
        if in_section:
            if s.startswith('## ') or s.startswith('# '):
                break  # next section
            if s.startswith('- '):
                items.append(s[2:].strip())
    return items


def extract_open_feedback(text: str) -> list[str]:
    """Return OPEN list items from a skill '## 8. Visszajelzések' section."""
    items = []
    lines = text.splitlines()
    in_section = False
    for line in lines:
        s = line.strip()
        if re.match(r'^##\s+8\.\s+Visszajelz', s):
            in_section = True
            continue
        if in_section:
            if re.match(r'^##\s+\d', s) or re.match(r'^#\s', s):
                break
            if s.startswith('- ') and any(m in s for m in OPEN_MARKERS):
                items.append(s[2:].strip())
    return items


def truncate(s: str, n: int = 90) -> str:
    s = re.sub(r'\s+', ' ', s)
    return s if len(s) <= n else s[:n - 1] + "…"


def main():
    parser = argparse.ArgumentParser(description="Nyitott pontok aggregátor (read-only)")
    parser.add_argument("--md", action="store_true", help="Markdown kimenet")
    args = parser.parse_args()

    # Meta-files with '## Nyitott pontok'
    meta_files = [
        PROJECT_ROOT / "CLAUDE.md",
        PROJECT_ROOT / "Instructions.md",
        PROJECT_ROOT / ".claude" / "pipeline.md",
    ]
    meta_files += sorted((PROJECT_ROOT / ".claude" / "prompts").glob("*.md"))

    skills_dir = PROJECT_ROOT / ".claude" / "skills"
    skill_files = sorted(skills_dir.glob("*.md")) if skills_dir.is_dir() else []

    results: list[tuple[str, list[str]]] = []
    total = 0

    for f in meta_files:
        if not f.exists():
            continue
        text = f.read_bytes().decode("utf-8-sig")
        items = extract_open_points_section(text)
        if items:
            rel = f.relative_to(PROJECT_ROOT).as_posix()
            results.append((rel, items))
            total += len(items)

    for f in skill_files:
        text = f.read_bytes().decode("utf-8-sig")
        items = extract_open_feedback(text)
        if items:
            rel = f.relative_to(PROJECT_ROOT).as_posix()
            results.append((rel, items))
            total += len(items)

    # Output
    if args.md:
        print("# Backlog snapshot (generált, read-only)\n")
        print(f"Összes nyitott tétel: **{total}**\n")
        print("| Fájl | Nyitott |")
        print("|------|--------:|")
        for rel, items in results:
            print(f"| `{rel}` | {len(items)} |")
        print("\n## Tételek\n")
        for rel, items in results:
            print(f"### {rel}")
            for it in items:
                print(f"- {truncate(it, 120)}")
            print()
    else:
        print(f"=== Nyitott pontok aggregátor ===  (összesen: {total})")
        for rel, items in results:
            print(f"\n{rel}  ({len(items)})")
            for it in items:
                print(f"  - {truncate(it)}")
        print(f"\nForrás: meta-fájlok '## Nyitott pontok' + skillek '§8' nyitott (🔲/❔/⚠️) tételei.")
        print("Operatív prioritás: .claude/project_status.md §1 Backlog.")


if __name__ == "__main__":
    main()
