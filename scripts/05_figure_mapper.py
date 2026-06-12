"""
05_figure_mapper.py -- `<!-- FIGURE: src/id -->` placeholder-feloldás a WIP jegyzeten.

A 04_content_synthesizer (Claude) a jegyzetbe `<!-- FIGURE: <forrás>/<fig_id> -->`
placeholdereket helyez oda, ahova egy ábra kerül. Ez a script **determinisztikusan**
feloldja őket a v4 `figure_catalog.json` alapján: kikeresi a kép útját, a citáció-kulcsot
és az oldalszámot, és a placeholder helyére beírja a kép-blokkot:

    ![<alt>](../2_clean_inputs/<stem>/images/pNNN_figNNN.png)
    *<n>. ábra. <katalógus-caption> [<cit>], <page>. o.*

A katalógus-caption gyakran angol (MinerU); a magyar, önálló koherens feliratmondatot a
Claude finomítja a 05 skill §3.3 kézi lépésében. A folytonos ábraszámozást a
07-3_figure_numberer.py véglegesíti — ez a script futó sorszámot ír (`<n>. ábra.`).

Idempotens: ha nincs placeholder (már feloldott jegyzet), 0 csere, a fájl nem változik.

Usage:
    python scripts/05_figure_mapper.py --week-dir test_outputs/atg/1_het
    python scripts/05_figure_mapper.py --week-dir test_outputs/atg/1_het --dry-run
"""

import argparse
import json
import re
import sys
from pathlib import Path

try:
    from _encoding_fix import fix_stdout as _fix_stdout
    _fix_stdout()
except ImportError:
    pass

try:
    from _citations_util import resolve_week
except ImportError:
    from scripts._citations_util import resolve_week  # type: ignore

# `<!-- FIGURE: <src>/<id> -->`  vagy  `<!-- FIGURE: <id> -->` (forrás nélkül).
# Tolerálja a ` — megjegyzés` utótagot és a változó whitespace-t.
_RE_PLACEHOLDER = re.compile(
    r'<!--\s*FIGURE:\s*(?:(?P<src>[^/\s>]+)\s*/\s*)?(?P<id>fig_\d+|\w+?)\s*(?:—[^>]*)?-->'
)
_RE_FIG_PREFIX = re.compile(r'^\s*(?:Figure|Fig\.?|Ábra|ábra)\s*\d+[.:]\s*', re.IGNORECASE)


def load_md(path: Path) -> str:
    """Markdown beolvasás BOM/CRLF kezeléssel, LF-re normalizálva."""
    return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def build_index(catalog: dict) -> dict[tuple[str, str], dict]:
    """v4 katalógus → {(forrás-norm, fig_id): figure+citation_key} lookup.

    A forrás kulcsa többféleképp is megadható a placeholderben (teljes fájlnév vagy
    stem); ezért minden forráshoz a teljes kulcsot ÉS a kiterjesztés nélküli stemet is
    indexeljük.
    """
    index: dict[tuple[str, str], dict] = {}
    for src_key, src_obj in catalog.get("sources", {}).items():
        citation_key = src_obj.get("citation_key")
        stem = Path(src_key).stem
        for fig in src_obj.get("figures", []):
            fig_id = fig.get("id")
            if not fig_id:
                continue
            entry = {**fig, "citation_key": citation_key, "source_key": src_key}
            for src_variant in {src_key, stem}:
                index[(src_variant, fig_id)] = entry
    return index


def resolve_one(src: str | None, fig_id: str,
                index: dict[tuple[str, str], dict]) -> tuple[dict | None, str | None]:
    """Egy placeholder feloldása. Visszaad: (entry, hibaüzenet)."""
    if src:
        entry = index.get((src, fig_id)) or index.get((Path(src).stem, fig_id))
        if entry:
            return entry, None
        return None, f"nincs a katalógusban: {src}/{fig_id}"
    # forrás nélküli id: keresd minden forrásban
    hits = [e for (s, i), e in index.items() if i == fig_id]
    uniq = {e["source_key"]: e for e in hits}
    if len(uniq) == 1:
        return next(iter(uniq.values())), None
    if not uniq:
        return None, f"nincs a katalógusban: {fig_id}"
    return None, f"többértelmű (forrás nélkül): {fig_id} → {list(uniq)}"


def clean_caption(caption: str | None) -> str:
    """„Figure N:" prefix levágása; a leíró rész marad (Claude fordítja magyarra §3.3)."""
    if not caption:
        return ""
    return _RE_FIG_PREFIX.sub("", caption.strip()).strip()


def make_block(entry: dict, n: int) -> str:
    """Kép-blokk a placeholder helyére (futó `n` sorszámmal; 07-3 véglegesíti)."""
    cat_path = entry.get("path", "")
    # a katalógus-út week-dir-relatív (2_clean_inputs/...); a jegyzet 4_wip_outputs/-ban
    # van, ezért `../` prefix.
    rel_path = f"../{cat_path}" if cat_path else ""
    caption = clean_caption(entry.get("caption"))
    alt = caption[:60] if caption else entry.get("id", "ábra")
    cit = entry.get("citation_key")
    page = entry.get("page")
    src_bits = []
    if cit:
        src_bits.append(f"[{cit}]")
    if page is not None:
        src_bits.append(f"{page}. o.")
    src_str = (" " + ", ".join(src_bits)) if src_bits else ""
    cap_line = f"*{n}. ábra. {caption}{src_str}*".replace("  ", " ")
    return f"![{alt}]({rel_path})\n{cap_line}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="`<!-- FIGURE: src/id -->` placeholder-feloldás (v4 katalógus)."
    )
    parser.add_argument("--week-dir", required=True, type=Path)
    parser.add_argument("--week", default=None, type=int)
    parser.add_argument("--dry-run", action="store_true",
                        help="Csak jelentés; a jegyzetet NEM írja át.")
    args = parser.parse_args()

    week_dir = args.week_dir.resolve()
    if not week_dir.is_dir():
        sys.exit(f"[HIBA] nem mappa: {week_dir}")
    week = resolve_week(week_dir, args.week)

    md_path = week_dir / "4_wip_outputs" / f"{week}_Jegyzet.md"
    cat_path = week_dir / "2_clean_inputs" / "figure_catalog.json"
    if not md_path.exists():
        sys.exit(f"[HIBA] nem található: {md_path}")
    if not cat_path.exists():
        sys.exit(f"[HIBA] nem található: {cat_path}")

    catalog = json.loads(cat_path.read_text(encoding="utf-8"))
    if catalog.get("_meta", {}).get("schema_version") != 4:
        sys.exit("[HIBA] nem v4 séma a figure_catalog.json-ban.")
    index = build_index(catalog)
    md_text = load_md(md_path)

    counter = [0]
    resolved, missing_img, unresolved = [], [], []

    def _sub(m: re.Match) -> str:
        src, fig_id = m.group("src"), m.group("id")
        entry, err = resolve_one(src, fig_id, index)
        if err:
            unresolved.append(err)
            return m.group(0)  # hagyd a placeholdert
        img_abs = week_dir / entry.get("path", "")
        if not img_abs.exists():
            missing_img.append(entry.get("path"))
            return f"<!-- FIGURE: {src or ''}{'/' if src else ''}{fig_id} — MISSING: {entry.get('path')} -->"
        counter[0] += 1
        resolved.append(f"{src or '?'}/{fig_id}")
        return make_block(entry, counter[0])

    new_text = _RE_PLACEHOLDER.sub(_sub, md_text)

    print(f"[05_figure_mapper] {md_path.name}: {counter[0]} placeholder feloldva, "
          f"{len(missing_img)} hiányzó kép, {len(unresolved)} feloldatlan")
    for r in resolved:
        print(f"  OK     {r}")
    for mi in missing_img:
        print(f"  MISSING {mi}")
    for u in unresolved:
        print(f"  SKIP   {u}")

    if args.dry_run:
        print("[05_figure_mapper] Dry-run: a jegyzet NEM íródott át.")
        return
    if new_text != md_text:
        md_path.write_text(new_text, encoding="utf-8")
        print(f"[05_figure_mapper] Mentve: {md_path}")
    else:
        print("[05_figure_mapper] Nincs változás (nem volt feloldható placeholder).")


if __name__ == "__main__":
    main()
