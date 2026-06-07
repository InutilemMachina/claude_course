"""
08_quality_check.py -- Automatikus minőségi metrikák a kész Jegyzeten.

A 08_quality_reviewer skill §3.1 metrikáit futtatja deterministically,
API/kvóta nélkül. Strukturális és formázási ellenőrzéseket végez, és
exit kóddal jelzi a kritikus hibákat (CI-barát).

Mit ellenőriz:
  - ## szekciók száma (cél: 5-12)
  - Fejezetenkénti ### alszakaszok (figyelmeztetés >15)
  - IEEE [N] citációk száma (a <sup>[N]</sup> régi jelölést is lefedi)
  - Inline forrásblokk maradék (cél: 0)
  - Dupla <sup>[N]</sup>,<sup>[N]</sup> citáció (cél: 0)
  - Romlott <!, Q:N, > marker (Rule H regresszió-teszt, cél: 0)
  - Tartalomjegyzék blokkok száma (ToC idempotencia, cél: 1)
  - Törött ToC anchor (szóköz/nagybetű a #...-ben, cél: 0)
  - 💡 Összegzés (## alfejezet végén) + 🗺️ Fejezet összegfoglalása (# fejezet zárásánál) blokkok száma

Exit kód: 0 = OK, 1 = kritikus hiba (>0 a "cél: 0" metrikákból).

Usage:
    python scripts/08_quality_check.py --week-dir <path/to/N_het>
    python scripts/08_quality_check.py --week-dir <path> --json
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


def find_jegyzet(week_dir: Path) -> Path | None:
    wip = week_dir / "4_wip_outputs"
    cands = sorted(wip.glob("*_Jegyzet.md"))
    return cands[0] if cands else None


def compute_metrics(text: str) -> dict:
    lines = text.splitlines()

    h2 = []
    h3 = []
    ch_sizes = {}
    cur = None
    for l in lines:
        if l.startswith('## ') and 'Tartalomjegyz' not in l and 'Hivatkoz' not in l:
            h2.append(l)
            cur = re.sub(r'^##\s+', '', l).strip()
            ch_sizes[cur] = 0
        elif l.startswith('### '):
            h3.append(l)
            if cur:
                ch_sizes[cur] += 1
    max_chapter = max(ch_sizes.items(), key=lambda x: x[1]) if ch_sizes else (None, 0)

    # IEEE [N] citáció: a kanonikus `[N]` (Instructions §8) ÉS a régi `<sup>[N]</sup>`
    # jelölést is számolja, mert a `\[\d+\]` minta a <sup>…</sup>-on belüli [N]-t is lefedi (B-12).
    citations = len(re.findall(r'\[\d+\]', text))
    inline_src = sum(1 for l in lines if re.match(r'\s*Felhaszn', l, re.IGNORECASE))
    dup_sup = len(re.findall(r'<sup>\[(\d+)\]</sup>,\s*<sup>\[\1\]</sup>', text))
    broken_marker = text.count('<!, Q:')
    toc_blocks = len(re.findall(r'^##\s+Tartalomjegyz', text, re.M))
    # Broken anchor: space or uppercase inside (#...)
    broken_anchor = len(re.findall(r'\(#[^)]*[A-Z ][^)]*\)', text))
    osszegzes_sub = text.count('💡 **Összegzés')
    osszegfoglalas = text.count('🗺️ **Fejezet összegfoglalása')
    images = text.count('![')

    return {
        "h2_sections": len(h2),
        "h3_subsections": len(h3),
        "max_chapter_name": max_chapter[0],
        "max_chapter_subs": max_chapter[1],
        "citations": citations,
        "inline_source_blocks": inline_src,
        "duplicate_citations": dup_sup,
        "broken_markers": broken_marker,
        "toc_blocks": toc_blocks,
        "broken_anchors": broken_anchor,
        "osszegzes_sub_blocks": osszegzes_sub,
        "osszegfoglalas_blocks": osszegfoglalas,
        "images": images,
    }


# Critical metrics: any nonzero (or wrong) value = failure
def evaluate(m: dict) -> list[str]:
    """Return a list of critical issue strings (empty = pass)."""
    issues = []
    if m["inline_source_blocks"] > 0:
        issues.append(f"Inline forrásblokk: {m['inline_source_blocks']} (cél: 0)")
    if m["duplicate_citations"] > 0:
        issues.append(f"Dupla citáció: {m['duplicate_citations']} (cél: 0)")
    if m["broken_markers"] > 0:
        issues.append(f"Romlott <!, Q: marker: {m['broken_markers']} (cél: 0) -- Rule H regresszió!")
    if m["toc_blocks"] != 1:
        issues.append(f"Tartalomjegyzék blokkok: {m['toc_blocks']} (cél: 1) -- ToC idempotencia!")
    if m["broken_anchors"] > 0:
        issues.append(f"Törött ToC anchor: {m['broken_anchors']} (cél: 0)")
    return issues


def evaluate_warnings(m: dict) -> list[str]:
    """Return a list of non-critical warning strings."""
    warns = []
    if not (5 <= m["h2_sections"] <= 12):
        warns.append(f"## szekciók: {m['h2_sections']} (ajánlott: 5-12)")
    if m["max_chapter_subs"] > 15:
        warns.append(f"Túlterhelt fejezet: '{m['max_chapter_name']}' "
                     f"({m['max_chapter_subs']} ### alszakasz, ajánlott: ≤15)")
    if m["citations"] < 10:
        warns.append(f"Kevés citáció: {m['citations']} (<10)")
    return warns


def main():
    parser = argparse.ArgumentParser(description="Automatikus minőségi metrikák a Jegyzeten")
    parser.add_argument("--week-dir", required=True, type=Path)
    parser.add_argument("--json", action="store_true", help="JSON kimenet")
    args = parser.parse_args()

    week_dir = args.week_dir.resolve()
    jegyzet = find_jegyzet(week_dir)
    if not jegyzet:
        sys.exit(f"HIBA: nem található *_Jegyzet.md itt: {week_dir / '4_wip_outputs'}")

    text = jegyzet.read_bytes().decode("utf-8-sig")
    m = compute_metrics(text)
    issues = evaluate(m)
    warns = evaluate_warnings(m)

    if args.json:
        print(json.dumps({"metrics": m, "issues": issues, "warnings": warns},
                         ensure_ascii=False, indent=2))
    else:
        print(f"=== 11b minőségi metrikák: {jegyzet.name} ===")
        print(f"  ## szekciók:            {m['h2_sections']}")
        print(f"  ### alszakaszok:        {m['h3_subsections']}")
        print(f"  Legnagyobb fejezet:     '{m['max_chapter_name']}' ({m['max_chapter_subs']} ###)")
        print(f"  [N] citációk:           {m['citations']}")
        print(f"  💡 Összegzés (##):      {m['osszegzes_sub_blocks']}")
        print(f"  🗺️ Fejezet összegf. (#):{m['osszegfoglalas_blocks']}")
        print(f"  Képek (![):             {m['images']}")
        print(f"  --- kritikus metrikák ---")
        print(f"  Inline forrásblokk:     {m['inline_source_blocks']} (cél 0)")
        print(f"  Dupla citáció:          {m['duplicate_citations']} (cél 0)")
        print(f"  Romlott marker:         {m['broken_markers']} (cél 0)")
        print(f"  ToC blokkok:            {m['toc_blocks']} (cél 1)")
        print(f"  Törött anchor:          {m['broken_anchors']} (cél 0)")
        print()
        if warns:
            print("FIGYELMEZTETÉS:")
            for w in warns:
                print(f"  ⚠️  {w}")
        if issues:
            print("KRITIKUS HIBÁK:")
            for it in issues:
                print(f"  ❌ {it}")
        else:
            print("✅ Nincs kritikus hiba.")

    sys.exit(1 if issues else 0)


if __name__ == "__main__":
    main()
