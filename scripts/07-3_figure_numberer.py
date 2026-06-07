"""
07-3_figure_numberer.py -- Ábra- és táblázatfeliratok automatikus, folytonos
újraszámozása a WIP jegyzeten (Instructions §7.1).

Miért kell: a 04/05 revízióknál (pl. a 08 §3.5 felhasználói revíziós csatorna)
gyakran szúrunk be ábrát/táblázatot a dokumentum közepére. A feliratok kézi
számozása ilyenkor elcsúszik, és minden későbbi feliratot át kellene írni. Ez a
script ezt determinisztikusan, idempotensen elvégzi — a 07-2_heading_numberer.py
ábra/tábla-megfelelője.

Konvenció (Instructions §7.1), a feliratok önálló, dőlt sorok:
  *N. ábra. Önálló koherens feliratmondat. [forrás / saját szerk.]*
  *N. táblázat. Önálló koherens feliratmondat. [forrás / saját szerk.]*

A két sorozatot KÜLÖN, előfordulási (dokumentum-) sorrendben számozza:
  ábra:    1, 2, 3, ...
  táblázat: 1, 2, 3, ...

Biztonság: csak a felirat-sor vezető sorszámát írja át; a szövegtörzset nem
módosítja. (A jegyzetben a szövegközi "N. ábra" hivatkozás nem konvenció — ha
később mégis bevezetjük, ezt a scriptet ki kell egészíteni a ref-frissítéssel.)
Kódblokkon (``` / ~~~) belüli sorokat kihagyja.

Exit kód: 0 mindig (lint-jellegű lépés); a változások számát kiírja.

Usage:
    python scripts/07-3_figure_numberer.py --week-dir <path/to/N_het>
    python scripts/07-3_figure_numberer.py <file.md> [--dry-run]
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

try:
    from _encoding_fix import fix_stdout as _fix_stdout
    _fix_stdout()
except ImportError:
    pass

# Felirat-sor: opcionális vezető whitespace, '*', szám, '. ', 'ábra'|'táblázat', '.'
CAPTION_RE = re.compile(r'^(\s*\*)(\d+)(\.\s+)(ábra|táblázat)(\.)', re.IGNORECASE)


def renumber(text: str) -> tuple[str, int]:
    """Újraszámozza az ábra/táblázat feliratokat. Visszaad: (új_szöveg, változások)."""
    lines = text.splitlines(keepends=True)
    counters = {"ábra": 0, "táblázat": 0}
    in_code = False
    n = 0
    out = []

    for line in lines:
        s = line.rstrip('\n')
        stripped = s.lstrip()
        if stripped.startswith('```') or stripped.startswith('~~~'):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue

        m = CAPTION_RE.match(s)
        if not m:
            out.append(line)
            continue

        kind = m.group(4).lower()
        counters[kind] += 1
        new_num = str(counters[kind])
        if m.group(2) != new_num:
            n += 1
        newline = CAPTION_RE.sub(
            lambda mm: f"{mm.group(1)}{new_num}{mm.group(3)}{mm.group(4)}{mm.group(5)}",
            line, count=1)
        out.append(newline)

    return ''.join(out), n


def find_jegyzet(week_dir: Path) -> Path | None:
    wip = week_dir / "4_wip_outputs"
    cands = sorted(wip.glob("*_Jegyzet.md"))
    return cands[0] if cands else None


def process(path: Path, dry_run: bool = False) -> int:
    # Sortörés-normalizálás olvasáskor (mint a 07-1): a CRLF-et LF-re hozzuk, mert
    # a splitlines(keepends=True) különben megőrizné a `\r\n`-t, és a write_text
    # OS-fordítása `\r\r\n`-t gyártana (üres-sor felszaporodás). Lásd: 07 skill §8.
    text = path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    new_text, n = renumber(text)
    if n == 0:
        print(f"  OK (nincs változás): {path.name}")
        return 0
    if dry_run:
        print(f"  [DRY] {n} felirat-átszámozás: {path.name}")
        for o, nu in zip(text.splitlines(), new_text.splitlines()):
            if o != nu:
                print(f"    - {o.strip()}\n    + {nu.strip()}")
        return n
    shutil.copy2(str(path), str(path) + ".bak")
    path.write_text(new_text, encoding="utf-8")
    print(f"  JAVÍTVA ({n}): {path.name}")
    return n


def main():
    p = argparse.ArgumentParser(description="Ábra/táblázat feliratok újraszámozása")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--week-dir", metavar="DIR", type=Path,
                   help="A heti mappa (N_het); a 4_wip_outputs/*_Jegyzet.md-t számozza")
    g.add_argument("md_path", nargs="?", default=None, help="Egy .md fájl elérési útja")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if args.week_dir is not None:
        jegyzet = find_jegyzet(args.week_dir.resolve())
        if not jegyzet:
            sys.exit(f"HIBA: nem található *_Jegyzet.md itt: {args.week_dir / '4_wip_outputs'}")
        path = jegyzet
    else:
        path = Path(args.md_path)
        if not path.exists():
            sys.exit(f"HIBA: nincs ilyen fájl: {path}")

    n = process(path, args.dry_run)
    print(f"Összesen: {n} változás")


if __name__ == "__main__":
    main()
