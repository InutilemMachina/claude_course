"""
14_bsc_filter.py -- Remove MSc blocks and write BSc-only output files

Reads 4_wip_outputs/N_*.md files, strips:
  - <!-- MSc --> ... <!-- /MSc --> HTML comment blocks
  - Mermaid [MSc] nodes (lines containing "[MSc]" inside a mermaid fence)
  - Questions at SZINT:4 or SZINT:5

Writes BSc versions to 5_clean_outputs/ with _bsc suffix.

Usage:
    python scripts/14_bsc_filter.py --week-dir <path/to/N_het> [options]

    --week-dir   Path to weekly folder. Required.
    --week       Week number (default: read from citations_seed.json _meta.week).
    --files      File types to process: note glossary mindmap questions presentation
                 (default: all that exist)
    --dry-run    Print filtered output to stdout, do not write files.
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Filter logic
# ---------------------------------------------------------------------------

def remove_msc_blocks(text: str) -> str:
    """Remove <!-- MSc --> ... <!-- /MSc --> block pairs (multiline)."""
    return re.sub(
        r'[ \t]*<!--\s*MSc\s*-->.*?<!--\s*/MSc\s*-->[ \t]*\n?',
        '',
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )


def remove_mermaid_msc_nodes(text: str) -> str:
    """Remove lines containing [MSc] inside mermaid code fences."""
    lines = text.splitlines(keepends=True)
    result = []
    in_mermaid = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```mermaid'):
            in_mermaid = True
            result.append(line)
        elif in_mermaid and stripped == '```':
            in_mermaid = False
            result.append(line)
        elif in_mermaid and '[MSc]' in line:
            pass  # drop this node line
        else:
            result.append(line)
    return ''.join(result)


def remove_msc_questions(text: str) -> str:
    """Remove question blocks marked SZINT:4 or SZINT:5.

    A question block starts with **K[N]** SZINT:4 or SZINT:5 and ends
    before the next **K or end of file.
    """
    # Match from **K[N]** SZINT:[4-5] to the next **K or EOF
    return re.sub(
        r'\*\*K\[\d+\]\*\*\s+SZINT:[45].*?(?=\*\*K\[\d+\]\*\*|\Z)',
        '',
        text,
        flags=re.DOTALL,
    )


def bsc_filter(text: str) -> str:
    text = remove_msc_blocks(text)
    text = remove_mermaid_msc_nodes(text)
    text = remove_msc_questions(text)
    # Collapse 3+ consecutive blank lines to 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


# ---------------------------------------------------------------------------
# File type mapping
# ---------------------------------------------------------------------------

FILE_STEMS = {
    'note':         'Jegyzet',
    'glossary':     'Szozedet',
    'mindmap':      'Mindmap',
    'questions':    'Kerdesek',
    'presentation': 'Prezentacio',
}


def resolve_week(week_dir: Path, week_arg) -> int:
    if week_arg:
        return int(week_arg)
    seed = week_dir / '1_raw_inputs' / 'citations_seed.json'
    if seed.exists():
        data = json.loads(seed.read_bytes().decode('utf-8-sig'))
        return data.get('_meta', {}).get('week', 1)
    return 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='BSc filter -- strip MSc blocks')
    parser.add_argument('--week-dir', required=True, type=Path,
                        help='Heti mappa')
    parser.add_argument('--week', default=None, type=int,
                        help='Hét száma (default: seed _meta)')
    parser.add_argument('--files', nargs='+',
                        choices=list(FILE_STEMS.keys()),
                        default=list(FILE_STEMS.keys()),
                        help='Feldolgozandó fájltípusok')
    parser.add_argument('--dry-run', action='store_true',
                        help='Szűrt tartalom stdout-ra, fájl nem íródik')
    args = parser.parse_args()

    week_dir = args.week_dir.resolve()
    if not week_dir.exists():
        sys.exit(f'Nem található: {week_dir}')

    week = resolve_week(week_dir, args.week)
    wip_dir   = week_dir / '4_wip_outputs'
    clean_dir = week_dir / '5_clean_outputs'

    if not args.dry_run:
        clean_dir.mkdir(parents=True, exist_ok=True)

    ok = 0
    for ftype in args.files:
        stem = FILE_STEMS[ftype]
        src = wip_dir / f'{week}_{stem}.md'
        if not src.exists():
            print(f'  SKIP  {src.name} -- nem található', file=sys.stderr)
            continue

        original = src.read_bytes().decode('utf-8-sig').replace('\r\n', '\n')
        filtered = bsc_filter(original)

        removed = len(original) - len(filtered)
        dst_name = f'{week}_{stem}_bsc.md'

        if args.dry_run:
            print(f'=== {dst_name} (+{removed} kar eltávolítva) ===')
            print(filtered)
        else:
            dst = clean_dir / dst_name
            dst.write_text(filtered, encoding='utf-8')
            print(f'  OK    {dst_name}  ({removed:+d} kar)')
        ok += 1

    print(f'Kész: {ok} fájl feldolgozva.')


if __name__ == '__main__':
    main()
