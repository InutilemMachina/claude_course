"""
00_init_course.py -- Új tantárgy struktúra + subject_status.md inicializálás.

Felállítja egy tantárgy mappastruktúráját, és a
templates/subject_status_template.md-ból generálja a subject_status.md-t:
a YAML frontmattert (subject, weeks, tags, dátum) és a heti pipeline-státusz
táblát automatikusan kitölti.

Létrehozza:
    test_outputs/<Tantargy>/subject_status.md    (a sablonból, ha még nincs)
    test_outputs/<Tantargy>/N_het/1_raw_inputs/  ... 5_clean_outputs/  (minden hétre)

Idempotens: meglévő subject_status.md-t és mappákat nem ír felül.

Usage:
    python scripts/00_init_course.py --subject Termografia --weeks 3
    python scripts/00_init_course.py --subject mini --weeks 1 --root test_outputs
"""

import argparse
import sys
import unicodedata
from datetime import date
from pathlib import Path

try:
    from _encoding_fix import fix_stdout as _fix_stdout
    _fix_stdout()
except ImportError:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = PROJECT_ROOT / "templates" / "subject_status_template.md"

WEEK_SUBDIRS = ["1_raw_inputs", "2_clean_inputs", "3_mindmap",
                "4_wip_outputs", "5_clean_outputs"]

# A subject_status.md §2 táblájának sorai = pipeline-lépések (🚦 = checkpoint).
PIPELINE_STEPS = [
    "00 init", "01 source_collector", "02 source_extractor",
    "03 mindmap 🚦", "04 content_synthesizer", "05 visual_enricher",
    "06 typesetter", "07 quality_reviewer 🚦", "08 question_bank",
    "09 presentation_maker", "10 bsc_export",
]


def _dwidth(s: str) -> int:
    """Megjelenítési szélesség: a széles (emoji, CJK) karakterek 2-t érnek."""
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in s)


def _pad(s: str, width: int) -> str:
    """Jobbra tölti szóközzel megjelenítési szélesség szerint."""
    return s + " " * max(0, width - _dwidth(s))


def render_status_table(weeks: int) -> str:
    """Markdown státusz-tábla: sorok = pipeline-lépések, oszlopok = hetek.
    A `|` karakterek megjelenítési szélesség szerint igazítva, hogy az
    emoji-soroknál is egybeessenek a fejléccel."""
    head = "Lépések (↓) / Hetek (→)"
    week_nums = [str(w) for w in range(1, weeks + 1)]
    w0 = max(_dwidth(head), _dwidth("*Téma*"), max(_dwidth(s) for s in PIPELINE_STEPS))
    wk = max(2, _dwidth("❌"), max((_dwidth(n) for n in week_nums), default=2))

    def row(label, cells):
        return "| " + " | ".join([_pad(label, w0)] + [_pad(c, wk) for c in cells]) + " |"

    sep = "| " + " | ".join([":" + "-" * (w0 - 1)] + [":" + "-" * (wk - 1) for _ in week_nums]) + " |"
    lines = [row(head, week_nums), sep, row("*Téma*", ["" for _ in week_nums])]
    lines += [row(step, ["❌" for _ in week_nums]) for step in PIPELINE_STEPS]
    return "\n".join(lines)


def instantiate_template(text: str, subject: str, weeks: int, tag: str, today: str) -> str:
    """A sablon placeholdereit kitölti. A MINTA-HATÁR jelölőtől a sablon-
    dokumentációt (mintatáblázat) levágja — az nem kerül az instancekba."""
    text = text.split("<!-- MINTA-HATÁR")[0].rstrip() + "\n"
    return (text
            .replace("{{SUBJECT}}", subject)
            .replace("{{TAGS}}", tag)
            .replace("{{WEEKS}}", str(weeks))
            .replace("{{DATE}}", today)
            .replace("{{STATUS_TABLE}}", render_status_table(weeks)))


def main():
    parser = argparse.ArgumentParser(description="Új tantárgy struktúra + subject_status.md")
    parser.add_argument("--subject", required=True, help="Tantárgy mappanév")
    parser.add_argument("--weeks", type=int, default=1, help="Hetek száma (default: 1)")
    parser.add_argument("--root", default="test_outputs",
                        help="Gyökér mappa (default: test_outputs)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    course_dir = (PROJECT_ROOT / args.root / args.subject).resolve()
    status_md = course_dir / "subject_status.md"
    tag = "test" if Path(args.root).name == "test_outputs" else "prod"
    today = date.today().isoformat()

    created = []
    skipped = []

    # 1. subject_status.md a sablonból, kitöltött frontmatterrel + táblával
    if status_md.exists():
        skipped.append(f"subject_status.md (már létezik)")
    else:
        if not TEMPLATE.exists():
            sys.exit(f"HIBA: nincs sablon: {TEMPLATE}")
        if not args.dry_run:
            course_dir.mkdir(parents=True, exist_ok=True)
            content = instantiate_template(
                TEMPLATE.read_text(encoding="utf-8"),
                args.subject, args.weeks, tag, today,
            )
            status_md.write_text(content, encoding="utf-8")
        created.append(f"subject_status.md (← subject_status_template.md, kitöltve)")

    # 2. Heti struktúra
    for w in range(1, args.weeks + 1):
        for sub in WEEK_SUBDIRS:
            d = course_dir / f"{w}_het" / sub
            if d.exists():
                continue
            if not args.dry_run:
                d.mkdir(parents=True, exist_ok=True)
            created.append(f"{w}_het/{sub}/")

    # Report
    prefix = "[DRY] " if args.dry_run else ""
    print(f"{prefix}Tantárgy: {course_dir.relative_to(PROJECT_ROOT).as_posix()}")
    for c in created:
        print(f"  + {c}")
    for s in skipped:
        print(f"  = {s}")
    print(f"{prefix}Kész: {len(created)} létrehozva, {len(skipped)} kihagyva.")
    if created and not args.dry_run:
        print(f"\nKövetkező: töltsd ki a subject_status.md-t, majd 01_source_collector.")


if __name__ == "__main__":
    main()
