"""
11-2_pandoc_export.py -- Camera-ready DOCX export Pandoc-kal.

A 4_wip_outputs/N_Jegyzet.md Markdown fájlt Word DOCX-be konvertálja a
templates/due_jegyzet_template.docx reference-dokumentum stílusaival.

Előfeltétel: pandoc telepítve (https://pandoc.org/installing.html).
  Windows: winget install --id JohnMacFarlane.Pandoc
Ha a pandoc nincs telepítve, a script világos hibaüzenetet ad és kilép (exit 2).

Mermaid-blokkok: a ```mermaid ... ``` blokkok PNG-vé renderelődnek a mermaid-cli
(mmdc) segítségével (ugyanaz az infrastruktúra mint a 10-1_mermaid_render.py).
Ha az mmdc / node nincs elérhető, a blokkok kódként maradnak + figyelmeztetés.

Usage:
    python scripts/11-2_pandoc_export.py --week-dir <path/to/N_het>
    python scripts/11-2_pandoc_export.py --week-dir <path> --no-template
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from _citations_util import resolve_week
except ImportError:
    from scripts._citations_util import resolve_week  # type: ignore

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_REPO = Path(__file__).resolve().parent.parent
_DEFAULT_MMDC = (_REPO / "test_outputs" / "_tools" / "node_modules"
                 / "@mermaid-js" / "mermaid-cli" / "src" / "cli.js")
_RE_MERMAID = re.compile(r'```mermaid\n(.*?)```', re.DOTALL)


# ---------------------------------------------------------------------------
# Pandoc discovery
# ---------------------------------------------------------------------------

def resolve_pandoc(project_root: Path) -> str | None:
    """Find pandoc: PATH > .claude/config.json > winget install glob."""
    p = shutil.which("pandoc")
    if p:
        return p
    cfg = project_root / ".claude" / "config.json"
    if cfg.exists():
        try:
            data = json.loads(cfg.read_bytes().decode("utf-8-sig"))
            cand = data.get("pandoc_path")
            if cand and Path(cand).exists():
                return cand
        except Exception:
            pass
    base = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages"
    if base.is_dir():
        for exe in base.glob("JohnMacFarlane.Pandoc*/pandoc*/pandoc.exe"):
            return str(exe)
    return None


def find_template(project_root: Path) -> Path | None:
    """Locate the Jegyzet reference docx in templates/."""
    cands = [
        project_root / "templates" / "due_jegyzet_template.docx",
        project_root / "templates" / "du_jegyzet_template.docx",
    ]
    for c in cands:
        if c.exists():
            return c
    tdir = project_root / "templates"
    if tdir.is_dir():
        for f in tdir.glob("*jegyzet*.docx"):
            return f
    return None


# ---------------------------------------------------------------------------
# Mermaid rendering
# ---------------------------------------------------------------------------

def _find_chromium() -> str | None:
    cache = Path.home() / ".cache" / "puppeteer" / "chrome-headless-shell"
    if cache.is_dir():
        hits = (list(cache.glob("*/*/chrome-headless-shell.exe"))
                + list(cache.glob("*/*/chrome-headless-shell")))
        if hits:
            return str(hits[0]).replace("\\", "/")
    for edge in [
        r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
        r"C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    ]:
        if Path(edge).exists():
            return edge
    return None


def _write_mmdc_config(work_dir: Path) -> Path | None:
    chromium = _find_chromium()
    if not chromium:
        return None
    cfg = work_dir / "_mmd_pptr.json"
    cfg.write_text(json.dumps({"executablePath": chromium, "args": ["--no-sandbox"]}),
                   encoding="utf-8")
    return cfg


def render_mermaid_blocks(text: str, work_dir: Path) -> tuple[str, list[Path]]:
    """Render ```mermaid blocks to PNG in work_dir; replace blocks with ![](name.png).

    Returns (modified_text, list_of_generated_png_files).
    Falls back gracefully if mmdc / node is unavailable.
    """
    cli_path = Path(os.environ.get("MMDC_CLI", str(_DEFAULT_MMDC)))
    node = shutil.which("node")

    if not cli_path.exists() or not node:
        print("  WARN  mermaid-cli / node nem elérhető — Mermaid-blokkok nem rendereltek")
        return text, []

    cfg = _write_mmdc_config(work_dir)
    if not cfg:
        print("  WARN  headless Chromium nem található — Mermaid-renderelés kihagyva")
        return text, []

    generated: list[Path] = []
    idx = [0]

    def replace(m: re.Match) -> str:
        idx[0] += 1
        mmd_file = work_dir / f"_mmd_{idx[0]:02d}.mmd"
        png_file = work_dir / f"_mmd_{idx[0]:02d}.png"
        mmd_file.write_text(m.group(1), encoding="utf-8")

        cmd = [node, str(cli_path), "-i", str(mmd_file), "-o", str(png_file),
               "-p", str(cfg), "-b", "white", "-s", "2"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        mmd_file.unlink(missing_ok=True)

        if res.returncode == 0 and png_file.exists():
            generated.append(png_file)
            print(f"  Mermaid {idx[0]:02d} -> {png_file.name} ({png_file.stat().st_size} B)")
            return f"![]({png_file.name})"
        else:
            err = (res.stderr or res.stdout).strip()[:120]
            print(f"  WARN  Mermaid {idx[0]:02d} renderelési hiba: {err}")
            return m.group(0)  # keep as code block

    modified = _RE_MERMAID.sub(replace, text)
    cfg.unlink(missing_ok=True)
    return modified, generated


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Camera-ready DOCX export Pandoc-kal")
    parser.add_argument("--week-dir", required=True, type=Path)
    parser.add_argument("--week", default=None, type=int)
    parser.add_argument("--no-template", action="store_true",
                        help="Reference template nélkül (Pandoc alapstílus)")
    parser.add_argument("--no-toc", action="store_true",
                        help="Tartalomjegyzék kihagyása")
    parser.add_argument("--no-mermaid", action="store_true",
                        help="Mermaid-renderelés kihagyása (blokkok kódként maradnak)")
    parser.add_argument("--pdf", action="store_true",
                        help="PDF exportálás is (xelatex, 5_clean_outputs/-ba)")
    args = parser.parse_args()

    week_dir = args.week_dir.resolve()
    project_root = Path(__file__).resolve().parent.parent

    # 1. Pandoc check
    pandoc = resolve_pandoc(project_root)
    if not pandoc:
        print("[HIBA] pandoc nincs telepítve.", file=sys.stderr)
        print("  Telepítés (Windows): winget install --id JohnMacFarlane.Pandoc", file=sys.stderr)
        print("  Vagy: https://pandoc.org/installing.html", file=sys.stderr)
        sys.exit(2)

    week = resolve_week(week_dir, args.week)

    # 2. Input Markdown
    src = week_dir / "4_wip_outputs" / f"{week}_Jegyzet.md"
    if not src.exists():
        sys.exit(f"[HIBA] nem található: {src}")

    # 3. Output
    clean_dir = week_dir / "6_clean_outputs"
    clean_dir.mkdir(parents=True, exist_ok=True)
    out = clean_dir / f"{week}_Jegyzet.docx"

    # 4. Mermaid pre-render (→ módosított szöveg átmeneti fájlba)
    text = src.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
    tmp_md = src.parent / f"_tmp_docx_{week}.md"
    mermaid_pngs: list[Path] = []

    if not args.no_mermaid and _RE_MERMAID.search(text):
        print(f"  Mermaid-blokkok renderelése ...")
        text, mermaid_pngs = render_mermaid_blocks(text, src.parent)
    tmp_md.write_text(text, encoding="utf-8")

    # 5. Template
    template = None if args.no_template else find_template(project_root)
    if template:
        print(f"  Template:   {template}")
    elif not args.no_template:
        print("  WARN  nincs Jegyzet-template a templates/-ben — alapstílus")

    # 6. Pandoc command
    cmd = [pandoc, str(tmp_md), "-o", str(out),
           "--from", "markdown+tex_math_dollars",
           "--standalone"]

    if not args.no_toc:
        cmd += ["--toc", "--toc-depth=3"]

    if template:
        cmd += ["--reference-doc", str(template)]

    # 7. Run
    print(f"  Konvertálás: {src.name} -> {out.name}")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", cwd=str(src.parent))

    # 8. Cleanup
    tmp_md.unlink(missing_ok=True)
    for png in mermaid_pngs:
        png.unlink(missing_ok=True)

    if result.returncode != 0:
        print(f"[HIBA] pandoc rc={result.returncode}", file=sys.stderr)
        if result.stderr:
            print(result.stderr[:500], file=sys.stderr)
        sys.exit(1)

    size_kb = out.stat().st_size // 1024 if out.exists() else 0
    print(f"OK: {out} ({size_kb} KB)")

    if args.pdf:
        _generate_pdf(pandoc, src, clean_dir, week)


def _generate_pdf(pandoc: str, src: Path, clean_dir: Path, week: int):
    """Generate PDF via xelatex. Runs pandoc from src.parent for relative image paths."""
    out_pdf = clean_dir / f"{week}_Jegyzet.pdf"

    text = src.read_text(encoding="utf-8")
    text_clean = re.sub(r'[\U0001F000-\U0001FFFF\U00002600-\U000027BF️]', '', text)
    tmp = src.parent / f"_pdf_tmp_{week}_Jegyzet.md"
    tmp.write_text(text_clean, encoding="utf-8")

    cmd = [pandoc, str(tmp.name), "-o", str(out_pdf.resolve()),
           "--from", "markdown+tex_math_dollars",
           "--standalone", "--pdf-engine=xelatex",
           "-V", "geometry:margin=2cm", "-V", "lang=hu"]

    print(f"  PDF: {tmp.name} -> {out_pdf.name}")
    result = subprocess.run(cmd, capture_output=True, text=True,
                            encoding="utf-8", errors="replace",
                            cwd=str(src.parent))
    tmp.unlink(missing_ok=True)

    if result.returncode != 0:
        print(f"  WARN  PDF generálás sikertelen (rc={result.returncode})", file=sys.stderr)
        if result.stderr:
            errs = [l for l in result.stderr.splitlines() if "Missing character" not in l]
            if errs:
                print('\n'.join(errs[:10]), file=sys.stderr)
    elif out_pdf.exists():
        size_kb = out_pdf.stat().st_size // 1024
        print(f"OK: {out_pdf} ({size_kb} KB)")
    else:
        print("  WARN  PDF fájl nem keletkezett", file=sys.stderr)


if __name__ == "__main__":
    main()
