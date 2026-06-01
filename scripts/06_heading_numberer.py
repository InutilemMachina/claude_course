"""
heading_numberer.py -- Auto-number Markdown headings with dotted hierarchy.

Convention:
  # Title Case Title        (document title -- no number)
  # 1. First section        (level-1 content)
  ## 1.1. Subsection        (level-2 content)
  ### 1.1.1. Sub-sub        (level-3 content)

Usage:
  python scripts/heading_numberer.py <file.md> [--dry-run] [--base-level N]
  python scripts/heading_numberer.py --all-in <folder> [--dry-run]
"""
# QUESTION: miért van erre  a sok processzálásra egyáltalán szükség? 

import argparse
import re
import shutil
import sys
from pathlib import Path

# Headings whose normalized name EXACTLY matches one of these stay unnumbered.
UNNUMBERED = {
    'targymutato',
    'forrasjegyzek',
    'valtozasnaplo',
    'valtozasjegyzek',
    'megjegyzes',
    # pipeline-specific unnumbered sections
    'bevezetes',           # ## Bevezetés (assembler Q1 wrapper)
    'tartalomjegyzek',     # ## Tartalomjegyzék (10_notes_collector)
    'tartalom',            # alt short form
    'hivatkozasjegyzek',   # ## Hivatkozásjegyzék (assembler reference list)
}
# QUESTION: hol helyezkednek el ezek egy egyetemi/akademiai jegyzetben? 

def _normalize(s):
    """Lowercase + strip accents + remove spaces, for comparison."""
    s = s.lower().strip()
    for a, b in [('a','a'),('a','a'),('e','e'),('e','e'),('i','i'),
                 ('o','o'),('o','o'),('o','o'),('u','u'),('u','u'),('u','u'),
                 ('á','a'),('é','e'),('í','i'),('ó','o'),
                 ('ö','o'),('ő','o'),('ú','u'),('ü','u'),('ű','u')]:
        s = s.replace(a, b)
    return s.replace(' ', '')

def _strip_num(text):
    """Remove leading dotted number or Roman numeral: '1.2. Foo' / 'II. Foo' -> 'Foo'."""
    # Arabic dotted: 1. / 1.2. / 1.2.3.
    text = re.sub(r'^[\d]+(?:\.[\d]+)*\.?\s+', '', text)
    # Roman numeral prefix: I. / II. / XIV. etc.
    text = re.sub(r'^[IVXLCDM]+\.\s+', '', text)
    return text.strip()

def _is_unnumbered(text):
    """True if this heading should stay without a number."""
    norm = _normalize(_strip_num(text))
    return norm in UNNUMBERED

def _detect_base(lines):
    """Find the minimum heading level used for content (skips title + special)."""
    title_seen = False
    in_yaml = False
    yaml_done = False
    in_code = False
    min_lv = 6
    for line in lines:
        s = line.rstrip('\n')
        if not yaml_done and s == '---':
            if not in_yaml and not title_seen:
                in_yaml = True; continue
            elif in_yaml:
                in_yaml = False; yaml_done = True; continue
        if in_yaml: continue
        if s.startswith('```') or s.startswith('~~~'):
            in_code = not in_code; continue
        if in_code: continue
        m = re.match(r'^(#{1,6})\s+(.+?)$', s)
        if not m: continue
        lv = len(m.group(1))
        content = _strip_num(m.group(2))
        if not title_seen:
            title_seen = True; continue
        if _is_unnumbered(content): continue
        min_lv = min(min_lv, lv)
    return min_lv if min_lv < 6 else 2

def renumber(text, base_level=None):
    """Renumber all headings. Returns (new_text, n_changes)."""
    lines = text.splitlines(keepends=True)
    if base_level is None:
        base_level = _detect_base(lines)

    result = []
    title_seen = False
    in_yaml = False
    yaml_done = False
    in_code = False
    counters = {}
    n = 0

    for line in lines:
        s = line.rstrip('\n')

        # YAML frontmatter
        if not yaml_done and s == '---':
            if not in_yaml and not title_seen:
                in_yaml = True; result.append(line); continue
            elif in_yaml:
                in_yaml = False; yaml_done = True; result.append(line); continue
        if in_yaml:
            result.append(line); continue

        # Code block
        if s.startswith('```') or s.startswith('~~~'):
            in_code = not in_code; result.append(line); continue
        if in_code:
            result.append(line); continue

        # Heading?
        m = re.match(r'^(#{1,6})\s+(.+?)(\s*)$', s)
        if not m:
            result.append(line); continue

        hashes = m.group(1)
        lv = len(hashes)
        content = _strip_num(m.group(2))

        # Document title
        if not title_seen:
            title_seen = True
            new = hashes + ' ' + content + '\n'
            if new != line: n += 1
            result.append(new); continue

        # Special unnumbered section
        if _is_unnumbered(content):
            new = hashes + ' ' + content + '\n'
            if new != line: n += 1
            result.append(new); continue

        # Update counters
        counters[lv] = counters.get(lv, 0) + 1
        for dl in list(counters):
            if dl > lv:
                counters[dl] = 0

        # Build dotted number from base_level..lv
        parts = [str(counters.get(l, 0)) for l in range(base_level, lv + 1)]
        num = '.'.join(parts) + '.'
        new_content = num + ' ' + content
        new = hashes + ' ' + new_content + '\n'
        if new.rstrip('\n') != s: n += 1
        result.append(new)

    return ''.join(result), n

def process(path, dry_run=False, base_level=None):
    try:
        with open(path, encoding='utf-8') as f:
            text = f.read()
    except OSError as e:
        print(f'  ERROR olvasás: {path.name}: {e}', file=sys.stderr)
        return 0
    new_text, n = renumber(text, base_level)
    if n == 0:
        print('  OK (no changes): ' + path.name); return 0
    if dry_run:
        print('  [DRY] ' + str(n) + ' changes: ' + path.name)
        for i, (o, nu) in enumerate(zip(text.splitlines(), new_text.splitlines())):
            if o != nu:
                print('    L' + str(i+1) + ': ' + repr(o) + ' -> ' + repr(nu))
        return n
    try:
        shutil.copy2(str(path), str(path) + '.bak')
        with open(str(path), 'w', encoding='utf-8') as f:
            f.write(new_text)
    except OSError as e:
        print(f'  ERROR írás: {path.name}: {e}', file=sys.stderr)
        return 0
    print('  FIXED (' + str(n) + '): ' + path.name)
    return n

def main():
    p = argparse.ArgumentParser(description='Renumber Markdown headings')
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('file', nargs='?', help='Single .md file')
    g.add_argument('--all-in', metavar='FOLDER', help='All .md in folder')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--base-level', type=int, default=None)
    args = p.parse_args()

    files = [Path(args.file)] if args.file else \
            [f for f in sorted(Path(args.all_in).glob('**/*.md'))
             if not f.name.endswith('.bak')]

    total = sum(process(f, args.dry_run, args.base_level) for f in files if f.exists())
    print('Total: ' + str(total) + ' changes')

if __name__ == '__main__':
    main()
