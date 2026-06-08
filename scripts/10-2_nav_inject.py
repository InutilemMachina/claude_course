"""10-2_nav_inject.py — Látható MARP renditionök a navigációs modellből.

A forrás `N_Prezentacio.md` keret-diáin a navigációt ma egy kép adja
(`_prezi_assets/navigator.png` / `secN.png`). Ez a script ezeket a navigációs
képeket SZÖVEGGÉ cseréli, két variánsban:

  - mindmap : a kép helyére beágyazott sorszámozott TOC markdown-lista
              (az aktuális csomópont kiemelve) → `N_Prezentacio_mindmap.md`
  - default : a navigációs kép elhagyva, a dia tetejére breadcrumb-sor kerül
              → `N_Prezentacio_default.md`

A valódi (nem navigációs) ábrák érintetlenek — azokat a `10-1_mermaid_render.py`
rendereli PNG-be. A navigáció soha nem kép.

Használat:
    python scripts/10-2_nav_inject.py --week-dir test_outputs/<tárgy>/N_het --variant both
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _nav_util as nav  # noqa: E402

# Navigációs kép (+ opcionális felirat-span a következő soron) a MARP-ban.
_NAV_BLOCK = re.compile(
    r'!\[[^\]]*\]\((_prezi_assets/(?:navigator|sec\d+)\.png)\)'
    r'[^\S\n]*(?:\n[^\S\n]*<span class="cap">.*?</span>)?',
    re.DOTALL | re.IGNORECASE,
)
_TITLE = re.compile(r'^##\s+(.*)$', re.MULTILINE)


def _toc_html_div(root, current_id) -> str:
    """render_toc HTML-nézetbe csomagolva <div class="toc">…</div>."""
    toc = nav.render_toc(root, current_id, view="html")
    return f'<div class="toc">\n{toc}\n</div>'


def _slide_title(block: str) -> str:
    m = _TITLE.search(block)
    return m.group(1).strip() if m else ""


def transform_block(block: str, variant: str, root) -> str:
    """Egy dia-blokk navigációs képének cseréje a variáns szerint."""
    m = _NAV_BLOCK.search(block)
    if not m:
        return block  # nincs navigációs kép (belső / valódi ábra / cím / hivatkozás)
    nav_path = m.group(1)
    title = _slide_title(block)
    current_id = None
    if root is not None:
        sec = nav.section_from_nav_image(nav_path)
        node = (nav.node_for_number(root, sec) if sec
                else nav.node_for_number(root, nav.number_from_title(title)))
        current_id = node.id if node else None

    if variant == "mindmap":
        repl = _toc_html_div(root, current_id) if root is not None else ""
        return block[:m.start()] + repl + block[m.end():]

    # default variáns:
    # - navigator.png (áttekintő/záró): teljes TOC beillesztve (current_id=None)
    # - secN.png (szakasz-nyitó): kép eltávolítva, nincs breadcrumb
    sec = nav.section_from_nav_image(nav_path)
    if sec is None:
        # navigator.png → teljes TOC, minden szakasz összecsukva
        repl = _toc_html_div(root, None) if root is not None else ""
        return block[:m.start()] + repl + block[m.end():]
    else:
        # secN.png → csak a kép törlése
        return block[:m.start()] + block[m.end():]


def transform_md(md_text: str, variant: str, root) -> str:
    parts = md_text.split("\n---\n")
    return "\n---\n".join(transform_block(p, variant, root) for p in parts)


def run_one(md_path: Path, out_path: Path, root, variant: str):
    md_text = md_path.read_text(encoding="utf-8")
    result = transform_md(md_text, variant, root)
    out_path.write_text(result, encoding="utf-8")
    print(f"[10-2] {variant:8s} → {out_path}")


def _detect_week(week_dir: Path) -> int:
    m = re.match(r"^(\d+)_het$", week_dir.name)
    if m:
        return int(m.group(1))
    raise ValueError(f"Nem tudja meghatározni a hét számát: {week_dir.name!r}")


def main():
    ap = argparse.ArgumentParser(description="MARP navigáció-injektálás (default / mindmap)")
    ap.add_argument("--week-dir", default=None,
                    help="Pipeline hét-mappa (pl. test_outputs/<tárgy>/N_het)")
    ap.add_argument("--variant", choices=["default", "mindmap", "both"], default="both")
    ap.add_argument("--input", default=None, help="Forrás MARP .md (week-dir nélkül)")
    ap.add_argument("--mindmap", default=None, help="mindmap.md útvonal felülírás")
    args = ap.parse_args()

    if args.week_dir:
        week = Path(args.week_dir)
        if not week.is_dir():
            sys.exit(f"Nem található: {week}")
        n = _detect_week(week)
        md_path = week / "4_wip_outputs" / f"{n}_Prezentacio.md"
        mindmap_path = args.mindmap or str(week / "3_mindmap" / "mindmap.md")
    elif args.input:
        md_path = Path(args.input)
        mindmap_path = args.mindmap
    else:
        ap.error("Kötelező: --week-dir VAGY --input")

    if not md_path.exists():
        sys.exit(f"Nem található: {md_path}")
    root = (nav.parse_mindmap(mindmap_path)
            if mindmap_path and Path(mindmap_path).exists() else None)
    if root is None:
        print("  ⚠️  Nincs mindmap.md — a navigáció üres marad.")

    variants = ["default", "mindmap"] if args.variant == "both" else [args.variant]
    for v in variants:
        out_path = md_path.with_name(f"{md_path.stem}_{v}{md_path.suffix}")
        run_one(md_path, out_path, root, v)


if __name__ == "__main__":
    main()
