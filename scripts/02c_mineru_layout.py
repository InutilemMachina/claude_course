"""
02c_mineru_layout.py — Layout-aware kiegészítő (image_rag_OCR sprint).

MinerU 2.7.6 futtatása a heti raw inputon → 2_clean_inputs/<stem>/mineru/{md,_content_list.json,images}.
A 02b_figure_enricher skill ezt preferálja text_context + caption + visual_content forrásként.

Output szerkezet (flat-elve a MinerU dupla <stem>/auto/ szintjéről):
    2_clean_inputs/<stem>/mineru/
      ├── <stem>.md                      # MinerU markdown
      ├── <stem>_content_list.json       # strukturált oldalanként
      └── images/<hash>.jpg              # extrahált képek

Usage:
    python scripts/02c_mineru_layout.py --week-dir test_outputs/atg/1_het
    python scripts/02c_mineru_layout.py --week-dir test_outputs/atg/1_het --source X.pdf
    python scripts/02c_mineru_layout.py --week-dir test_outputs/atg/1_het --lang-map "nagyi2013_eloadas.pdf=latin"

Nyelvi mapping: a MinerU 2.7.6 `-l` csak `en/ch/latin/...` választható (NEM `hun`).
Magyar oldalakra `-l latin` ajánlott. Default `en`, override CLI `--lang-map`-pal.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from _encoding_fix import fix_stdout as _fix_stdout
    _fix_stdout()
except ImportError:
    pass

MINERU_ENV = "mineru"
DEFAULT_LANG = "en"
# Heurisztika: forrás-stem kulcsszó alapján
LANG_HINT = {
    "nagyi":   "latin",   # magyar
    "magyar":  "latin",
    "hu":      "latin",
}


def detect_lang(src_stem: str, override: dict[str, str]) -> str:
    if src_stem in override:
        return override[src_stem]
    name = src_stem.lower()
    for hint, lang in LANG_HINT.items():
        if hint in name:
            return lang
    return DEFAULT_LANG


def flatten_mineru_output(out_root: Path, src_stem: str) -> bool:
    """A MinerU `<out>/<stem>/auto/...` szerkezetét flat-eljük `<out>/<stem>/`-be.
    Idempotens: ha már flat (auto/ nincs), no-op."""
    nested = out_root / src_stem / "auto"
    flat   = out_root / src_stem
    if not nested.exists():
        return False
    for item in nested.iterdir():
        target = flat / item.name
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        shutil.move(str(item), str(target))
    nested.rmdir()
    return True


def run_mineru_for_source(src: Path, out_root: Path, lang: str,
                          start_page: int | None = None,
                          end_page: int | None = None) -> bool:
    out_root.mkdir(parents=True, exist_ok=True)
    cmd = [
        "conda", "run", "-n", MINERU_ENV, "--no-capture-output",
        "mineru", "-p", str(src), "-o", str(out_root),
        "-m", "auto", "-b", "pipeline", "-l", lang,
    ]
    if start_page is not None:
        cmd += ["-s", str(start_page)]
    if end_page is not None:
        cmd += ["-e", str(end_page)]
    print(f"  → conda run mineru ({lang}) {src.name}")
    proc = subprocess.run(cmd, capture_output=False, timeout=3600)
    return proc.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="02c MinerU layout extractor (image_rag_OCR)")
    parser.add_argument("--week-dir", required=True, type=Path)
    parser.add_argument("--source", type=str, default=None,
                        help="Csak ez a forrás (fájlnév); ha hiányzik, minden PDF a 1_raw_inputs/-ban")
    parser.add_argument("--lang-map", type=str, default="",
                        help="filename=lang,filename=lang formátum, pl. 'X.pdf=latin,Y.pdf=en'")
    parser.add_argument("--start", type=int, default=None)
    parser.add_argument("--end",   type=int, default=None)
    args = parser.parse_args()

    week_dir = args.week_dir.resolve()
    raw_in   = week_dir / "1_raw_inputs"
    clean_in = week_dir / "2_clean_inputs"
    if not raw_in.is_dir():
        sys.exit(f"HIBA: nincs {raw_in}")

    # Per-source nyelvi override
    override = {}
    for chunk in (args.lang_map or "").split(","):
        chunk = chunk.strip()
        if "=" in chunk:
            fname, lang = chunk.split("=", 1)
            override[Path(fname).stem] = lang

    if args.source:
        sources = [raw_in / args.source]
    else:
        sources = sorted(f for f in raw_in.iterdir()
                         if f.is_file() and f.suffix.lower() == ".pdf"
                         and not f.name.startswith("_"))

    ok = err = 0
    for src in sources:
        src_stem = src.stem
        out_root = clean_in / src_stem / "mineru"
        # MinerU magát `<out>/<stem>/auto/`-ba írja, így ha az `out` már `mineru/`, akkor
        # `mineru/<stem>/auto/`. A flatten ezt majd `mineru/`-ba mozgatja át (`<stem>/auto/` → `mineru/`).
        # Egyszerűbb: futtassuk `<clean_in>/<stem>/`-be, és onnan flat-eljük.
        out_root_mineru_parent = clean_in / src_stem  # ide írja: <stem>/<stem>/auto
        lang = detect_lang(src_stem, override)
        if not run_mineru_for_source(src, out_root_mineru_parent, lang, args.start, args.end):
            print(f"  ✗ HIBA: {src.name}")
            err += 1
            continue
        # MinerU output: clean_in/<stem>/<stem>/auto/...
        # Cél:           clean_in/<stem>/mineru/...
        nested_auto = out_root_mineru_parent / src_stem / "auto"
        if nested_auto.exists():
            # Töröljük a régi mineru/-t és átnevezzük
            mineru_dir = out_root_mineru_parent / "mineru"
            if mineru_dir.exists():
                shutil.rmtree(mineru_dir)
            mineru_dir.mkdir(parents=True, exist_ok=True)
            for item in nested_auto.iterdir():
                shutil.move(str(item), str(mineru_dir / item.name))
            nested_auto.rmdir()
            (out_root_mineru_parent / src_stem).rmdir()
        print(f"  ✓ {src.name} → {clean_in / src_stem / 'mineru'}")
        ok += 1

    print(f"\nKész: {ok} OK, {err} hiba")
    return 0 if err == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
