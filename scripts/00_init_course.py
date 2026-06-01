"""
00_init_course.py -- Új tantárgy struktúra + context.md inicializálás.

Felállítja egy tantárgy mappastruktúráját és bemásolja a
templates/course_development_template.md-t context.md-ként.
Ezzel a sablon automatikusan a tantárgyhoz kerül (nem kézi másolás).

Létrehozza:
    test_outputs/<Tantargy>/context.md          (a sablonból, ha még nincs)
    test_outputs/<Tantargy>/N_het/1_raw_inputs/  ... 5_clean_outputs/  (minden hétre)

Idempotens: meglévő context.md-t és mappákat nem ír felül.

Usage:
    python scripts/00_init_course.py --subject Termografia --weeks 3
    python scripts/00_init_course.py --subject mini --weeks 1 --root test_outputs
"""

import argparse
import shutil
import sys
from pathlib import Path

try:
    from _encoding_fix import fix_stdout as _fix_stdout
    _fix_stdout()
except ImportError:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = PROJECT_ROOT / "templates" / "course_development_template.md"

WEEK_SUBDIRS = ["1_raw_inputs", "2_clean_inputs", "3_raw_outputs",
                "4_wip_outputs", "5_clean_outputs"]


def main():
    parser = argparse.ArgumentParser(description="Új tantárgy struktúra + context.md")
    parser.add_argument("--subject", required=True, help="Tantárgy mappanév")
    parser.add_argument("--weeks", type=int, default=1, help="Hetek száma (default: 1)")
    parser.add_argument("--root", default="test_outputs",
                        help="Gyökér mappa (default: test_outputs)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    course_dir = (PROJECT_ROOT / args.root / args.subject).resolve()
    context_md = course_dir / "context.md"

    created = []
    skipped = []

    # 1. context.md a sablonból
    if context_md.exists():
        skipped.append(f"context.md (már létezik)")
    else:
        if not TEMPLATE.exists():
            sys.exit(f"HIBA: nincs sablon: {TEMPLATE}")
        if not args.dry_run:
            course_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(TEMPLATE, context_md)
        created.append(f"context.md (← course_development_template.md)")

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
        print(f"\nKövetkező: töltsd ki a context.md-t, majd 01_references_collector.")


if __name__ == "__main__":
    main()
