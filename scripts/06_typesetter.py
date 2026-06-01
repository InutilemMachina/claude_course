"""
11_typesetter.py -- Markdown linter for NLM pipeline output.

Phase 1 (bullet-to-prose) removed: NLM --response-length longer already produces prose.
Phase 2: Whitespace/formatting linting (rules A, C, D, E, F, H).

Usage:
    python 11_typesetter.py <path_to_N_Jegyzet.md>
"""

import re
import sys
from pathlib import Path
try:
    from _encoding_fix import fix_stdout as _fix_stdout
    _fix_stdout()
except ImportError:
    pass


# ---- File I/O ----

def load_md(path: Path) -> str:
    """Read Markdown, handling BOM and CRLF (PowerShell Out-File artifacts)."""
    return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def save_md(path: Path, text: str):
    """Write Markdown as UTF-8 without BOM."""
    path.write_text(text, encoding="utf-8")


# ---- Linting rules ----

def rule_a_sup_paragraph_break(text: str) -> tuple[str, int]:
    """
    Rule A: Insert blank line after </sup>. before new sentence starting with
    a capital (Hungarian) letter.
    """
    pattern = re.compile(r"(</sup>\.)([ \t]*)([A-ZÁÉÍÓÖŐÚÜŰ])")
    count = len(pattern.findall(text))
    text = pattern.sub(r"\1\n\n\3", text)
    return text, count


def rule_c_image_spacing(text: str) -> tuple[str, int]:
    """Rule C: Ensure a blank line before every ![ image reference."""
    pattern = re.compile(r"([^\n])\n(!\[)")
    count = len(pattern.findall(text))
    text = pattern.sub(r"\1\n\n\2", text)
    return text, count


def rule_d_blockquote_spacing(text: str) -> tuple[str, int]:
    """Rule D: Ensure a blank line before every > blockquote line."""
    pattern = re.compile(r"([^\n>])\n(> )")
    count = len(pattern.findall(text))
    text = pattern.sub(r"\1\n\n\2", text)
    return text, count


def rule_b_bullet_whitespace(text: str) -> tuple[str, int]:
    """Rule B: Collapse extra spaces after bullet marker (* or -).
    Fixes NLM output artifact: '* ' or '-  ' with multiple spaces.
    """
    pattern = re.compile(r"^(\s*[*-])\s{2,}", re.MULTILINE)
    count = len(pattern.findall(text))
    text = pattern.sub(r"\1 ", text)
    return text, count


def rule_e_hr_dedup(text: str) -> tuple[str, int]:
    """Rule E: Collapse consecutive --- separators into one."""
    pattern = re.compile(r"---\n+---")
    count = len(pattern.findall(text))
    text = pattern.sub("---", text)
    return text, count


def rule_f_latex_check(text: str) -> list[str]:
    """
    Rule F: Check for unpaired LaTeX delimiters.
    Returns a list of warning strings (empty = OK).
    Does NOT modify text.
    """
    warnings = []
    # Inline $: match $ not preceded or followed by another $
    singles = re.findall(r"(?<!\$)\$(?!\$)", text)
    if len(singles) % 2 != 0:
        warnings.append(f"Unpaired inline $ (count={len(singles)})")
    # Display $$
    doubles = re.findall(r"\$\$", text)
    if len(doubles) % 2 != 0:
        warnings.append(f"Unpaired display $$ (count={len(doubles)})")
    return warnings


def rule_h_dash_cleanup(text: str) -> tuple[str, int]:
    """
    Rule H: Remove dashes forbidden in Hungarian academic output.
    Targets: -- (double hyphen), en-dash (U+2013), em-dash (U+2014).
    Strategy: replace with comma + space, unless surrounded by whitespace
    (standalone separator) -- then replace with comma alone.
    Does NOT touch YAML front matter (lines before second ---).
    Does NOT touch code blocks (``` fences).
    """
    count = 0

    # Split off YAML front matter to protect it
    yaml_end = -1
    if text.startswith("---"):
        second = text.find("\n---", 3)
        if second != -1:
            yaml_end = second + 4  # past the closing ---\n

    header = text[:yaml_end] if yaml_end != -1 else ""
    body = text[yaml_end:] if yaml_end != -1 else text

    # Regex: optional spaces + dash(es) + optional spaces (not inside code fences)
    # Replace " -- " / " – " / " — " with ", " (drop surrounding spaces)
    pattern = re.compile(r" *(--|[–—]) *")

    def replacer(m):
        nonlocal count
        count += 1
        return ", "

    # Process line by line to skip ``` code fences
    in_fence = False
    lines = body.split("\n")
    result = []
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
        # Skip code fences, headings, and HTML comments (e.g. <!-- Q:N -->).
        # The <!-- --> comment syntax legitimately contains "--", so Rule H
        # must NOT touch it (otherwise <!-- Q:1 --> becomes <!, Q:1, >).
        if in_fence or line.strip().startswith("#") or line.strip().startswith("<!--"):
            result.append(line)
        else:
            result.append(pattern.sub(replacer, line))
    body = "\n".join(result)

    return header + body, count


def rule_i_table_separator(text: str) -> tuple[str, int]:
    """
    Rule I: Fix malformed GFM table separator rows.
    NLM sometimes generates: | :, - | :, - | :, - |
    Correct GFM:             | :--- | :--- | :--- |
    Also fixes: |---|  -> | :--- |  when alignment prefix detected.
    """
    count = 0

    def fix_sep_row(m):
        nonlocal count
        inner = m.group(1)
        # Check if this looks like a malformed separator
        # Pattern: cells that are ":, -" or ":,-" or similar (comma between : and -)
        if re.search(r':\s*,\s*-', inner):
            # Count columns by splitting on |
            cells = [c.strip() for c in inner.split('|') if c.strip()]
            fixed_cells = []
            for cell in cells:
                # Determine alignment from original cell
                has_left = cell.strip().startswith(':')
                has_right = cell.strip().endswith(':')
                if has_left and has_right:
                    fixed_cells.append(':---:')
                elif has_right:
                    fixed_cells.append('---:')
                elif has_left or ':' in cell:
                    fixed_cells.append(':---')
                else:
                    fixed_cells.append('---')
            count += 1
            return '| ' + ' | '.join(fixed_cells) + ' |'
        return m.group(0)

    # Match table separator rows: lines starting with | and containing - signs
    text = re.sub(
        r'^\|([|\s:,\-]+)\|$',
        fix_sep_row,
        text,
        flags=re.MULTILINE
    )
    return text, count


def rule_c3_pdf_inline_noise(text: str) -> tuple[str, int]:
    """
    Rule C3: Távolítsd el a prózából az inline (fájlnév.pdf/html/docx/pptx) zajt.
    Ezek régi NLM outputokban keletkeztek, ahol a citáció fájlnévként jelent meg.
    Csak egyértelműen fájlnévszerű mintákat töröl (szóköz nélkül, kiterjesztéssel).
    """
    # Pattern: whitespace + (filename.ext) -- no spaces inside, common doc extensions
    pattern = re.compile(r'\s*\([A-Za-z0-9_\-\.]+\.(?:pdf|html|docx|pptx|txt)\)', re.IGNORECASE)
    toc_link_re = re.compile(r'^\s*-\s+\[.*\]\(#.*\)\s*$')
    count = 0
    lines = text.split('\n')
    result = []
    in_fence = False
    for line in lines:
        if line.strip().startswith('```'):
            in_fence = not in_fence
        if (in_fence or line.strip().startswith('#') or line.strip().startswith('<!--')
                or toc_link_re.match(line)):
            result.append(line)
        else:
            new_line, n = pattern.subn('', line)
            count += n
            result.append(new_line)
    return '\n'.join(result), count


def rule_c4_citation_dedup(text: str) -> tuple[str, int]:
    """
    Rule C4: Duplikált <sup>[N]</sup>,<sup>[N]</sup> → <sup>[N]</sup> (safety net).
    A 07_citations_renumber.py már végez dedup-ot; ez a typesetter-szintű biztosíték.
    """
    pattern = re.compile(r'(<sup>\[(\d+)\]</sup>)(?:,\s*<sup>\[\2\]</sup>)+')
    orig_count = len(pattern.findall(text))
    new_text = pattern.sub(r'\1', text)
    return new_text, orig_count


def rule_j_terminology(text: str) -> tuple[str, int]:
    """
    Rule J: Normalize Hungarian IR thermography terminology inconsistencies.
    Applied only to body text (not code blocks, YAML, headings).
    """
    # Term pairs: (pattern, canonical_replacement)
    TERM_MAP = [
        (r'\bemissziós tényező\b',         'emisszivitás'),
        (r'\bemittancia\b',                 'emisszivitás'),
        (r'\bsugárzási tényező\b',          'emisszivitás'),
        (r'\blégköri ablak\b',              'atmoszferikus ablak'),
        (r'\blégköri ablakok\b',            'atmoszferikus ablakok'),
        (r'\bszürke test\b',               'szürketest'),
        (r'\bhőkamera\b',                  'IR kamera'),
        (r'\bhőkamerák\b',                 'IR kamerák'),
    ]
    count = 0
    lines = text.split('\n')
    result = []
    in_fence = False
    # ToC link-line pattern: "- [text](#anchor)" -- terminology swap here would
    # break the anchor (e.g. #a-hőkamerák → #a-IR kamerák, space + case mismatch).
    toc_link_re = re.compile(r'^\s*-\s+\[.*\]\(#.*\)\s*$')
    for line in lines:
        if line.strip().startswith('```'):
            in_fence = not in_fence
        # Skip code fences, headings, YAML, HTML comments, and ToC link lines
        if (in_fence or line.strip().startswith('#')
                or line.strip().startswith('<!--')
                or toc_link_re.match(line)):
            result.append(line)
            continue
        new_line = line
        for pattern, replacement in TERM_MAP:
            new_line, n = re.subn(pattern, replacement, new_line)
            count += n
        result.append(new_line)
    return '\n'.join(result), count


def rule_k_numeric_interval(text: str) -> tuple[str, int]:
    """
    Rule K: Numerikus intervallum normalizálás.
    Az NLM output néha tizedes értékeket listává bont (angolból fordítva):
      '1, 5 µm'    -> '1,5 µm'        (tizedes)
      '0, 1, 3 µm' -> '0,1–3 µm'      (intervallum)
    Csak kód-fencen kívül, nem fejléc-sorokban alkalmazva.
    """
    UNITS = (r'(?:µm|nm|mm|cm|km|µs|ns|ms|kHz|MHz|GHz|mV|kV|mW|kW|MW|kPa|MPa'
             r'|m|s|V|W|K|Hz|Pa|%|°C)')
    # Háromtagú sorozat: "0, 1, 3 µm" -> "0,1–3 µm"  (hosszabb minta először)
    pat3 = re.compile(r'\b(\d+),\s+(\d+),\s+(\d+)\s+(' + UNITS + r')\b')
    # Kéttagú tizedes: "1, 5 µm" -> "1,5 µm"
    pat2 = re.compile(r'\b(\d+),\s+(\d+)\s+(' + UNITS + r')\b')

    toc_link_re = re.compile(r'^\s*-\s+\[.*\]\(#.*\)\s*$')
    count = 0
    lines = text.split('\n')
    result = []
    in_fence = False
    for line in lines:
        if line.strip().startswith('```'):
            in_fence = not in_fence
        if (in_fence or line.strip().startswith('#') or line.strip().startswith('<!--')
                or toc_link_re.match(line)):
            result.append(line)
            continue
        new_line, n = pat3.subn(lambda m: (
            f"{m.group(1)},{m.group(2)}–{m.group(3)} {m.group(4)}"
        ), line)
        count += n
        line = new_line
        new_line = pat2.sub(lambda m: f"{m.group(1)},{m.group(2)} {m.group(3)}", line)
        if new_line != line:
            count += 1
        result.append(new_line)
    return '\n'.join(result), count


def phase2_linting(text: str) -> str:
    """Apply rules A–K. Rule G (heading numbering) uses a separate util."""
    print("[Phase 2] Linting...")

    text, n_a = rule_a_sup_paragraph_break(text)
    print(f"  Rule A (sup paragraph breaks): {n_a} fix(es)")

    text, n_b = rule_b_bullet_whitespace(text)
    print(f"  Rule B (bullet whitespace):    {n_b} fix(es)")

    text, n_c = rule_c_image_spacing(text)
    print(f"  Rule C (image blank lines):    {n_c} fix(es)")

    text, n_d = rule_d_blockquote_spacing(text)
    print(f"  Rule D (blockquote spacing):   {n_d} fix(es)")

    text, n_e = rule_e_hr_dedup(text)
    print(f"  Rule E (HR dedup):             {n_e} fix(es)")

    warnings_f = rule_f_latex_check(text)
    if warnings_f:
        print("  Rule F (LaTeX) WARNINGS:")
        for w in warnings_f:
            print(f"    - {w}")
    else:
        print("  Rule F (LaTeX):                OK")

    text, n_h = rule_h_dash_cleanup(text)
    print(f"  Rule H (dash cleanup):         {n_h} fix(es)")

    text, n_i = rule_i_table_separator(text)
    print(f"  Rule I (table separator):      {n_i} fix(es)")

    text, n_j = rule_j_terminology(text)
    print(f"  Rule J (terminology):          {n_j} fix(es)")

    text, n_c3 = rule_c3_pdf_inline_noise(text)
    print(f"  Rule C3 (pdf inline noise):    {n_c3} fix(es)")

    text, n_c4 = rule_c4_citation_dedup(text)
    print(f"  Rule C4 (citation dedup):      {n_c4} fix(es)")

    text, n_k = rule_k_numeric_interval(text)
    print(f"  Rule K (numeric interval):     {n_k} fix(es)")

    print("[Phase 2] Done.")
    return text


# ---- Main ----

def _resolve_md_path(args) -> Path:
    """Resolve the input Markdown path from --week-dir or positional arg."""
    if args.week_dir is not None:
        week_dir = Path(args.week_dir).resolve()
        wip_dir = week_dir / "4_wip_outputs"
        notes = sorted(wip_dir.glob("*_Jegyzet.md"))
        if not notes:
            print(f"ERROR: nincs *_Jegyzet.md a {wip_dir}-ban")
            sys.exit(1)
        return notes[-1]
    if hasattr(args, 'md_path') and args.md_path:
        p = Path(args.md_path)
        if not p.exists():
            print(f"ERROR: File not found: {p}")
            sys.exit(1)
        return p
    print("ERROR: add meg a --week-dir <mappa> paramétert vagy a fájl elérési útját.")
    sys.exit(1)


def main():
    import argparse as _ap
    parser = _ap.ArgumentParser(
        description="Markdown linter for NLM pipeline output (Phase 2)",
        add_help=True
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--week-dir", metavar="DIR",
                       help="Heti mappa (pl. test_outputs/mini3/1_het); "
                            "automatikusan megkeresi a *_Jegyzet.md fájlt")
    group.add_argument("md_path", nargs="?", default=None,
                       help="[DEPRECATED] Direkt fájl elérési út. "
                            "Használd a --week-dir paramétert helyette.")
    args = parser.parse_args()

    if args.md_path:
        print("FIGYELEM: Direkt fájl-arg elavult. Használd: --week-dir <heti_mappa>")

    md_path = _resolve_md_path(args)

    print(f"[11_typesetter] Input: {md_path}")
    text = load_md(md_path)
    original_len = len(text)

    text = phase2_linting(text)
    save_md(md_path, text)
    print(
        f"[11_typesetter] Written back: {md_path} "
        f"({original_len} -> {len(text)} chars)"
    )
    print("[11_typesetter] TIP: Run 11_util_heading_numberer.py for Rule G (heading numbering).")


if __name__ == "__main__":
    main()
