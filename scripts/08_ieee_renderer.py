"""
07-2_ieee_renderer.py -- IEEE-stílusú hivatkozásjegyzék renderelése

Bemenet:
  - 3_raw_outputs/citations.json
  - 4_wip_outputs/N_Jegyzet.md

Kimenet:
  - 4_wip_outputs/N_Jegyzet.md  (## Hivatkozásjegyzék szekció újraírva IEEE-re)

Forrástípus-specifikus formátum:
  paper / slides  : [N] Author, "Title," *Venue*, Year.
  book            : [N] Author, *Title*, Publisher, Year.
  chapter         : [N] Author, "Title," in *Book*, Publisher, Year.
  webpage         : [N] Author, "Title," *Venue*. [Online]. Available: URL.

Inline <sup>[N]</sup> érintetlen marad (már IEEE-konform, a 07_citations_renumber.py állítja elő).

Futtatás:
    python scripts/07-2_ieee_renderer.py --week-dir test_outputs/mini2/1_het
    python scripts/07-2_ieee_renderer.py --week-dir test_outputs/mini2/1_het --dry-run
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


SECTION_HEADER = "## Hivatkozásjegyzék"
ALT_HEADERS = ["## Forrásjegyzék"]

UNKNOWN_YEAR = "é.n."
UNKNOWN_AUTHOR = "Ismeretlen szerző"
UNKNOWN_TITLE = "Cím nélkül"


# ---------------------------------------------------------------------------
# JSON I/O
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict:
    """Load JSON file (UTF-8-sig safe, CRLF safe)."""
    return json.loads(path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n"))


# ---------------------------------------------------------------------------
# IEEE formatting
# ---------------------------------------------------------------------------

def _clean_year(year) -> str:
    if not year:
        return UNKNOWN_YEAR
    s = str(year).strip()
    if s.upper() in ("NA", "N/A", "NONE", ""):
        return UNKNOWN_YEAR
    return s


def _clean_venue(venue) -> str:
    if not venue:
        return ""
    s = str(venue).strip()
    if s.upper() in ("NA", "N/A", "NONE"):
        return ""
    return s


def format_ieee(num: int, entry: dict) -> str:
    """Format a single citations.json entry as an IEEE reference line.

    Returns plain text (Markdown *italics* supported for venue/title).
    """
    authors = str(entry.get("authors") or UNKNOWN_AUTHOR).strip()
    title   = str(entry.get("title")   or UNKNOWN_TITLE).strip()
    year    = _clean_year(entry.get("year"))
    venue   = _clean_venue(entry.get("venue") or entry.get("source") or "")
    url     = (entry.get("url") or "").strip()
    etype   = (entry.get("type") or "paper").lower()

    if etype in ("paper", "slides", "pdf"):
        # [N] Author, "Title," *Venue*, Year.
        if venue:
            return f"[{num}] {authors}, \"{title},\" *{venue}*, {year}."
        else:
            return f"[{num}] {authors}, \"{title},\" {year}."

    elif etype == "book":
        # [N] Author, *Title*, Publisher, Year.
        if venue:
            return f"[{num}] {authors}, *{title}*, {venue}, {year}."
        else:
            return f"[{num}] {authors}, *{title}*, {year}."

    elif etype == "chapter":
        # [N] Author, "Chapter Title," in *Venue*, Year.
        if venue:
            return f"[{num}] {authors}, \"{title},\" in *{venue}*, {year}."
        else:
            return f"[{num}] {authors}, \"{title},\" {year}."

    elif etype == "webpage":
        # [N] Author, "Title," *Venue*. [Online]. Available: [url](url).
        parts = [f"[{num}] {authors}, \"{title},\""]
        if venue:
            parts.append(f" *{venue}*.")
        if url:
            parts.append(f" \\[Online\\]. Available: [{url}]({url}).")
        else:
            parts.append(f" {year}.")
        return "".join(parts)

    else:
        # Fallback: paper-style
        if venue:
            return f"[{num}] {authors}, \"{title},\" *{venue}*, {year}."
        else:
            return f"[{num}] {authors}, \"{title},\" {year}."


def build_ieee_section(citations: dict) -> str:
    """Build the full ## Hivatkozásjegyzék block as Markdown string."""
    entries = sorted(
        [(int(k), v) for k, v in citations.items() if not k.startswith("_")],
        key=lambda x: x[0]
    )
    lines = [SECTION_HEADER, ""]
    for num, entry in entries:
        lines.append(format_ieee(num, entry))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Section replacement
# ---------------------------------------------------------------------------

def _find_section(text: str) -> tuple[int, int, str | None]:
    """Find the start and end indices of the Hivatkozásjegyzék section.

    Returns (start, end, header_used) where start..end is the full section
    text (including the header line and trailing blank lines).
    Returns (-1, -1, None) if not found.
    """
    candidates = [SECTION_HEADER] + ALT_HEADERS

    for hdr in candidates:
        # Try as a mid-file section (preceded by newline)
        pattern = r"(?:^|\n)(" + re.escape(hdr) + r")(?:\n|$)"
        m = re.search(pattern, text)
        if not m:
            continue

        # Section starts at the beginning of the header line
        hdr_start = m.start() if m.start() == 0 else m.start() + 1

        # Find the end: next ## heading at the same or higher level, or EOF
        after_header = hdr_start + len(hdr)
        next_section = re.search(r"\n## ", text[after_header:])
        if next_section:
            hdr_end = after_header + next_section.start()
        else:
            hdr_end = len(text)

        return hdr_start, hdr_end, hdr

    return -1, -1, None


def replace_section(text: str, new_section: str) -> tuple[str, bool]:
    """Replace the existing Hivatkozásjegyzék section with new_section.

    If not found, appends to the end.
    Returns (new_text, was_replaced).
    """
    start, end, hdr = _find_section(text)

    if start == -1:
        return text, False

    # Preserve content before the section (with a separating newline)
    prefix = text[:start]
    suffix = text[end:].lstrip("\n")

    new_text = prefix
    if prefix and not prefix.endswith("\n\n"):
        new_text += "\n" if prefix.endswith("\n") else "\n\n"
    new_text += new_section
    if suffix:
        new_text += "\n" + suffix

    return new_text, True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="IEEE hivatkozásjegyzék renderelése a véglegesített Jegyzetbe"
    )
    parser.add_argument("--week-dir", required=True, type=Path,
                        help="Heti mappa (pl. test_outputs/mini2/1_het)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Csak kimenet-preview, fájl nem módosítva")
    args = parser.parse_args()

    week_dir = args.week_dir.resolve()
    citations_path = week_dir / "3_raw_outputs" / "citations.json"
    wip_dir = week_dir / "4_wip_outputs"

    if not citations_path.exists():
        sys.exit(f"HIBA: {citations_path} nem található")
    if not wip_dir.is_dir():
        sys.exit(f"HIBA: {wip_dir} nem létezik")

    citations = load_json(citations_path)

    # Detect N_Jegyzet.md (highest-numbered match)
    notes = sorted(wip_dir.glob("*_Jegyzet.md"))
    if not notes:
        sys.exit(f"HIBA: nincs *_Jegyzet.md a {wip_dir}-ban")
    jegyzet_path = notes[-1]

    text = jegyzet_path.read_text(encoding="utf-8")

    # Build IEEE section
    new_section = build_ieee_section(citations)

    # Replace
    new_text, replaced = replace_section(text, new_section)
    if not replaced:
        print("FIGYELEM: Nem találtam Hivatkozásjegyzék szekciót -- hozzáfűzöm a végéhez.")
        new_text = text.rstrip("\n") + "\n\n" + new_section

    entry_count = sum(1 for k in citations if not k.startswith("_"))
    print(f"[07-2_ieee_renderer] {jegyzet_path.name}")
    print(f"  Forrásszám: {entry_count}")
    print(f"  Szekció: {'cserélve' if replaced else 'hozzáfűzve'}")

    if args.dry_run:
        print("[DRY RUN] fájl nem módosítva. Generált szekció:")
        print("-" * 60)
        print(new_section)
        return

    bak = str(jegyzet_path) + ".bak"
    shutil.copy2(str(jegyzet_path), bak)
    jegyzet_path.write_text(new_text, encoding="utf-8")
    print(f"OK: {jegyzet_path} felülírva (backup: {bak})")


if __name__ == "__main__":
    main()
