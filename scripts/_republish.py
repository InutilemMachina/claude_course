"""
_republish.py -- 12/13 gazdagítási kör orchestrátor (utility, nincs külön skill).

Egy negyedéves gazdagítási kör mechanizált végrehajtása (a 😎 ezt futtatja a kijelölés +
regiszter-sorok ✅ után):

  1. kiolvassa a wip `product_version`-t (current);
  2. kiszámolja az új verziót (minor bump, vagy --major);
  3. megjelöli a regiszter ✅, még verzió nélküli sorait (`verzió`=új, `dátum`=ma);
  4. ARCHIVÁLJA a meglévő 6_clean termékeket → 6_clean_outputs/archive/*_v{current}.*;
  5. visszaírja a wip `product_version`-t (= új);
  6. újra-exportál: 11-2_pandoc_export.py --enrich + 10_pptx_gyarto.py --enrich --variant both.

Ha nincs új (✅, verzió nélküli) gazdagítás és nincs --major/--force → nincs teendő.
--dry-run: csak a tervet írja ki, semmit nem módosít.

Usage:
    python scripts/_republish.py --week-dir test_outputs/<tárgy>/N_het
    python scripts/_republish.py --week-dir <path> --dry-run
    python scripts/_republish.py --week-dir <path> --major      # tartalmi revízió után
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import date as _date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _enrich_util as eu  # noqa: E402

try:
    from _encoding_fix import fix_stdout as _fix_stdout
    _fix_stdout()
except ImportError:
    pass

try:
    from _citations_util import resolve_week
except ImportError:
    from scripts._citations_util import resolve_week  # type: ignore

_SCRIPTS = Path(__file__).resolve().parent

# A kanonikus 6_clean termékek (amiket archiválunk + újra-exportálunk).
_PRODUCTS = ["{w}_Jegyzet.docx", "{w}_Prezentacio.pptx",
             "{w}_Prezentacio_mindmap.pptx", "{w}_Kerdesbank.xml"]


def _archive_current(clean_dir: Path, week: int, version: str, dry_run: bool) -> list[str]:
    """A meglévő kanonikus termékeket átmásolja az archive/-ba `_v{version}` utótaggal."""
    archive = clean_dir / "archive"
    done: list[str] = []
    for pat in _PRODUCTS:
        src = clean_dir / pat.format(w=week)
        if not src.exists():
            continue
        dst = archive / f"{src.stem}_v{version}{src.suffix}"
        if not dry_run:
            archive.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        done.append(dst.name)
    return done


def _run_export(script: str, week_dir: Path, extra: list[str]) -> bool:
    cmd = [sys.executable, str(_SCRIPTS / script), "--week-dir", str(week_dir), "--enrich", *extra]
    print(f"  → {' '.join(cmd[1:])}")
    res = subprocess.run(cmd)
    return res.returncode == 0


def main() -> None:
    ap = argparse.ArgumentParser(description="12/13 gazdagítási kör — verziózott újra-export")
    ap.add_argument("--week-dir", required=True, type=Path)
    ap.add_argument("--week", default=None, type=int)
    ap.add_argument("--dry-run", action="store_true", help="Csak a terv; semmit nem módosít.")
    ap.add_argument("--major", action="store_true", help="MAJOR bump (tartalmi revízió után).")
    ap.add_argument("--force", action="store_true", help="Akkor is fusson, ha nincs új ✅ gazdagítás.")
    args = ap.parse_args()

    week_dir = args.week_dir.resolve()
    if not week_dir.is_dir():
        sys.exit(f"[HIBA] nem mappa: {week_dir}")
    week = resolve_week(week_dir, args.week)

    wip = week_dir / "4_wip_outputs" / f"{week}_Jegyzet.md"
    reg = week_dir / "5_asset_outputs" / "enrichment_register.md"
    clean_dir = week_dir / "6_clean_outputs"
    if not wip.exists():
        sys.exit(f"[HIBA] nincs wip jegyzet: {wip}")

    wip_text = wip.read_bytes().decode("utf-8-sig")
    current = eu.current_version(wip_text)
    new_version = eu.bump_version(current, "major" if args.major else "minor")

    # Van-e új (✅, verzió nélküli) gazdagítás?
    pending = eu.stamp_register(reg, new_version, _date.today().isoformat(), dry_run=True)
    if not pending and not args.major and not args.force:
        print(f"[republish] Nincs új ✅ gazdagítás a regiszterben ({reg.name}) — nincs teendő.")
        print("  (Adj ✅ sort a regiszterhez, vagy használd a --major / --force kapcsolót.)")
        return

    tag = "[DRY] " if args.dry_run else ""
    print(f"{tag}[republish] {wip.name}: v{current} → v{new_version}"
          f"  (új gazdagítás: {', '.join(pending) or '—'})")

    archived = _archive_current(clean_dir, week, current, args.dry_run)
    print(f"{tag}  archív (v{current}): {', '.join(archived) or 'nincs meglévő termék'}")

    if args.dry_run:
        print(f"{tag}  regiszter-stamp: {', '.join(pending) or '—'} → v{new_version}")
        print(f"{tag}  wip product_version → {new_version}")
        print(f"{tag}  újra-export: 11-2 --enrich + 10 --enrich --variant both")
        print("[DRY] Nincs módosítás.")
        return

    # 3. regiszter-stamp (élesben)
    stamped = eu.stamp_register(reg, new_version, _date.today().isoformat(), dry_run=False)
    print(f"  regiszter-stamp: {', '.join(stamped) or '—'} → v{new_version}")

    # 5. wip product_version
    wip.write_text(eu.set_version(wip_text, new_version), encoding="utf-8")
    print(f"  wip product_version → {new_version}")

    # 6. újra-export
    ok_docx = _run_export("11-2_pandoc_export.py", week_dir, [])
    ok_pptx = _run_export("10_pptx_gyarto.py", week_dir, ["--variant", "both"])
    if ok_docx and ok_pptx:
        print(f"[republish] KÉSZ — v{new_version} kiadva ({clean_dir}); a v{current} az archive/-ban.")
    else:
        print(f"[republish] FIGYELEM: export hiba (docx={ok_docx}, pptx={ok_pptx}). "
              f"A verzió/regiszter már v{new_version}; futtasd újra az exportot a hiba után.",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
