"""
_ocr_lab_runner.py — Komparatív OCR backend runner (image_rag_OCR sprint).

Bemenet:  test_outputs/_ocr_lab/atg_1_het/input_manifest.json  (15 oldal × 4 forrás)
Kimenet:  test_outputs/_ocr_lab/atg_1_het/<backend>/<src>/...
          test_outputs/_ocr_lab/atg_1_het/metrics.json   (idő, hiba, char count)

Backendek (egyenként try/except — egy elhasalása nem rontja a többit):
  tesseract     — pytesseract + Tesseract binary
  pymupdf4llm   — pip install pymupdf4llm   (csak born-digital, kontrol)
  mineru        — conda run -n mineru mineru -p <pdf> -o <out> --page-range
  marker        — opcionális (marker-venv külön)
  doctr         — opcionális
  claude_read   — NEM hív API-t. A runner csak a placeholder mappákat hozza létre
                  + a végén megméri, mit talált. A populálást a session/skill végzi.

Futás:
  python scripts/_ocr_lab_runner.py --backend tesseract
  python scripts/_ocr_lab_runner.py --backend mineru
  python scripts/_ocr_lab_runner.py --backend all
  python scripts/_ocr_lab_runner.py --report          # csak újrameri a metrics.json-t
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

try:
    from _encoding_fix import fix_stdout as _fix_stdout
    _fix_stdout()
except ImportError:
    pass

# ── Konfiguráció ──────────────────────────────────────────────────────────────
LAB_ROOT     = Path("test_outputs/_ocr_lab/atg_1_het")
WEEK_RAW_DIR = Path("test_outputs/atg/1_het/1_raw_inputs")
MANIFEST     = LAB_ROOT / "input_manifest.json"
METRICS      = LAB_ROOT / "metrics.json"
RENDER_DPI   = 200      # OCR-hez magasabb DPI mint a 02 (150) — gyenge szkennen jobb
OCR_LANGS    = "eng+hun"
MINERU_ENV   = "mineru"

# Tesseract Windows-specifikus fallback útvonalak (ha nincs PATH-ban)
import os
TESSERACT_CANDIDATES = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Users\lasz\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
]
# User-writable tessdata directory (hun.traineddata letöltve ide, mert
# C:\Program Files admin jogot igényel)
TESSDATA_USER_DIR = Path.home() / ".tessdata"
if TESSDATA_USER_DIR.exists():
    os.environ.setdefault("TESSDATA_PREFIX", str(TESSDATA_USER_DIR))
BACKENDS_ALL = ["tesseract", "pymupdf4llm", "mineru", "marker", "doctr", "claude_read"]


# ── Helper: PDF oldal-renderelés (PNG bytes) ──────────────────────────────────

def render_page_png(pdf_path: Path, page_num: int, dpi: int = RENDER_DPI) -> bytes:
    """Egy PDF oldal renderelése PNG byte-okká (1-based page_num)."""
    import fitz  # PyMuPDF
    doc = fitz.open(str(pdf_path))
    try:
        page = doc[page_num - 1]
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        return pix.tobytes("png")
    finally:
        doc.close()


def write_page_render(pdf_path: Path, page_num: int, out_png: Path) -> None:
    """Ha nincs PNG cache az oldalról, készítsünk egyet — Vision/docTR/Tesseract inputja."""
    if out_png.exists() and out_png.stat().st_size > 0:
        return
    out_png.parent.mkdir(parents=True, exist_ok=True)
    out_png.write_bytes(render_page_png(pdf_path, page_num))


# ── Manifest ─────────────────────────────────────────────────────────────────

def load_manifest() -> list[dict]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return data["pages"]


def group_by_source(entries: list[dict]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for e in entries:
        out.setdefault(e["source"], []).append(e)
    return out


# ── Backend: Tesseract ────────────────────────────────────────────────────────

def run_tesseract(entries: list[dict]) -> dict:
    """pytesseract per page — eredmény: text/pNNN.txt minden oldalra.

    A runner egy közös 'page-renders/' cache-ben tartja a PNG-ket, hogy ne kelljen
    minden backend külön renderelni.
    """
    out_root = LAB_ROOT / "tesseract"
    times: dict[str, float] = {}
    errors: dict[str, str] = {}
    char_counts: dict[str, int] = {}

    try:
        import pytesseract
        from PIL import Image
        from io import BytesIO
    except ImportError as e:
        return {"available": False, "error": f"missing dep: {e}"}

    # Próbáljuk meg a PATH-os tesseract-ot, ha nincs, fallback a candidate listára
    try:
        ver = str(pytesseract.get_tesseract_version())
    except Exception:
        for cand in TESSERACT_CANDIDATES:
            if Path(cand).exists():
                pytesseract.pytesseract.tesseract_cmd = cand
                try:
                    ver = str(pytesseract.get_tesseract_version())
                    break
                except Exception:
                    continue
        else:
            return {"available": False, "error": "tesseract binary not found in PATH or candidates"}

    for e in entries:
        pdf = WEEK_RAW_DIR / e["source"]
        page_id = e["id"]
        src_stem = Path(e["source"]).stem
        out_txt = out_root / src_stem / "text" / f"p{e['page']:03d}.txt"

        try:
            t0 = time.perf_counter()
            png_bytes = render_page_png(pdf, e["page"])
            img = Image.open(BytesIO(png_bytes))
            text = pytesseract.image_to_string(img, lang=OCR_LANGS)
            t1 = time.perf_counter()
            out_txt.parent.mkdir(parents=True, exist_ok=True)
            out_txt.write_text(text, encoding="utf-8")
            times[page_id] = round(t1 - t0, 3)
            char_counts[page_id] = len(text)
        except Exception as ex:
            errors[page_id] = f"{type(ex).__name__}: {ex}"

    return {
        "available": True,
        "version": ver,
        "times_per_page": times,
        "char_counts": char_counts,
        "errors": errors,
        "n_ok": len(times),
        "n_err": len(errors),
        "total_time_s": round(sum(times.values()), 3),
        "avg_time_per_page_s": round(sum(times.values()) / max(len(times), 1), 3),
    }


# ── Backend: PyMuPDF4LLM (born-digital baseline) ─────────────────────────────

def run_pymupdf4llm(entries: list[dict]) -> dict:
    """PyMuPDF4LLM forrásonként egy markdown — szkennelten haszontalan."""
    out_root = LAB_ROOT / "pymupdf4llm"
    times: dict[str, float] = {}
    errors: dict[str, str] = {}
    char_counts: dict[str, int] = {}

    try:
        import pymupdf4llm
    except ImportError as e:
        return {"available": False, "error": f"missing dep: {e}. pip install pymupdf4llm"}

    by_src = group_by_source(entries)
    for src, src_entries in by_src.items():
        pdf = WEEK_RAW_DIR / src
        src_stem = Path(src).stem
        out_md = out_root / f"{src_stem}.md"
        try:
            t0 = time.perf_counter()
            pages_0idx = [e["page"] - 1 for e in src_entries]
            md = pymupdf4llm.to_markdown(str(pdf), pages=pages_0idx)
            t1 = time.perf_counter()
            out_md.parent.mkdir(parents=True, exist_ok=True)
            out_md.write_text(md, encoding="utf-8")
            elapsed = round(t1 - t0, 3)
            # Idő egyenletesen elosztva, mert PyMuPDF4LLM batch
            per_page = elapsed / max(len(src_entries), 1)
            for e in src_entries:
                times[e["id"]] = round(per_page, 3)
                char_counts[e["id"]] = len(md) // max(len(src_entries), 1)
        except Exception as ex:
            for e in src_entries:
                errors[e["id"]] = f"{type(ex).__name__}: {ex}"

    return {
        "available": True,
        "times_per_page": times,
        "char_counts": char_counts,
        "errors": errors,
        "n_ok": len(times),
        "n_err": len(errors),
        "total_time_s": round(sum(times.values()), 3),
        "avg_time_per_page_s": round(sum(times.values()) / max(len(times), 1), 3),
    }


# ── Backend: MinerU ───────────────────────────────────────────────────────────

def run_mineru(entries: list[dict]) -> dict:
    """conda run -n mineru mineru ... — forrásonként egy futás, --start-page-id/--end-page-id-val.

    NB: mineru CLI nem támogat tetszőleges page-listát, csak range-et. Egyszerűbb a teljes
    fájlt futtatni és a kapott markdownból kivenni amit kell. De pilothoz a teljes futás
    túl lassú lehet (gravdahl 62 oldal). Köztes út: kiszámolunk egy minimális összefüggő
    range-et a manifest oldalakból.
    """
    out_root = LAB_ROOT / "mineru"
    out_root.mkdir(parents=True, exist_ok=True)
    times: dict[str, float] = {}
    errors: dict[str, str] = {}
    notes: dict[str, str] = {}

    # MinerU sanity
    sanity = subprocess.run(
        ["conda", "run", "-n", MINERU_ENV, "--no-capture-output", "mineru", "--version"],
        capture_output=True, text=True, timeout=60,
    )
    if sanity.returncode != 0:
        return {"available": False, "error": f"mineru sanity failed: {sanity.stderr or sanity.stdout}"}
    version = (sanity.stdout or sanity.stderr).strip().splitlines()[-1]

    by_src = group_by_source(entries)
    for src, src_entries in by_src.items():
        pdf = WEEK_RAW_DIR / src
        src_stem = Path(src).stem
        pages = sorted(e["page"] for e in src_entries)
        start_page, end_page = pages[0], pages[-1]
        # MinerU 2.7.6: -l nem tud "hun"-t, csak "latin"-t magyarra (+"en" angolra)
        lang = "en"
        if any(e.get("lang", "").startswith("hu") for e in src_entries):
            lang = "latin"
        # 0-indexű range a -s/-e flagekkel
        cmd = [
            "conda", "run", "-n", MINERU_ENV, "--no-capture-output",
            "mineru", "-p", str(pdf), "-o", str(out_root),
            "-m", "auto", "-b", "pipeline", "-l", lang,
            "-s", str(start_page - 1),
            "-e", str(end_page - 1),
        ]
        try:
            t0 = time.perf_counter()
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
            t1 = time.perf_counter()
            elapsed = round(t1 - t0, 3)
            if proc.returncode != 0:
                tail = (proc.stderr or proc.stdout).splitlines()[-5:]
                for e in src_entries:
                    errors[e["id"]] = "mineru exit != 0: " + " | ".join(tail)
                continue
            # Idő egyenletesen elosztva oldalak között
            n_pages_in_range = end_page - start_page + 1
            per_page = elapsed / max(n_pages_in_range, 1)
            for e in src_entries:
                times[e["id"]] = round(per_page, 3)
                notes[e["id"]] = f"page range {start_page}-{end_page} ({n_pages_in_range} pages)"
        except subprocess.TimeoutExpired:
            for e in src_entries:
                errors[e["id"]] = "mineru timeout > 1200s"
        except Exception as ex:
            for e in src_entries:
                errors[e["id"]] = f"{type(ex).__name__}: {ex}"

    return {
        "available": True,
        "version": version,
        "times_per_page": times,
        "errors": errors,
        "notes": notes,
        "n_ok": len(times),
        "n_err": len(errors),
        "total_time_s": round(sum(times.values()), 3),
        "avg_time_per_page_s": round(sum(times.values()) / max(len(times), 1), 3),
    }


# ── Backend: Marker (opcionális) ──────────────────────────────────────────────

def run_marker(entries: list[dict]) -> dict:
    """marker-pdf — opcionális, csak ha installálva van."""
    try:
        import marker  # noqa: F401
    except ImportError as e:
        return {"available": False, "error": f"marker not installed: {e}. pip install marker-pdf"}
    # TODO: tényleges futás. Placeholder, hogy a runner ne dőljön el.
    return {"available": True, "note": "TODO implementation pending pilot install"}


# ── Backend: docTR (opcionális) ───────────────────────────────────────────────

def run_doctr(entries: list[dict]) -> dict:
    try:
        from doctr.models import ocr_predictor  # noqa: F401
    except ImportError as e:
        return {"available": False, "error": f"docTR not installed: {e}. pip install python-doctr[torch]"}
    return {"available": True, "note": "TODO implementation pending pilot install"}


# ── Backend: Claude Read placeholder ──────────────────────────────────────────

def run_claude_read(entries: list[dict]) -> dict:
    """A runner csak a page-rendereket gyártja le (claude_read/<src>/page-renders/pNNN.png),
    a tényleges szöveg-kinyerést a session/skill végzi a Read tool-lal és Write-tal.
    Eredmény mérése: char_count a meglévő text/pNNN.txt-kből (ha a session már populálta)."""
    out_root = LAB_ROOT / "claude_read"
    char_counts: dict[str, int] = {}
    missing: list[str] = []

    for e in entries:
        pdf = WEEK_RAW_DIR / e["source"]
        src_stem = Path(e["source"]).stem
        png = out_root / src_stem / "page-renders" / f"p{e['page']:03d}.png"
        write_page_render(pdf, e["page"], png)
        txt = out_root / src_stem / "text" / f"p{e['page']:03d}.txt"
        if txt.exists() and txt.stat().st_size > 0:
            char_counts[e["id"]] = len(txt.read_text(encoding="utf-8"))
        else:
            missing.append(e["id"])

    return {
        "available": True,
        "note": "Page-renders ready. Populate text/pNNN.txt via session Read+Write to complete.",
        "char_counts": char_counts,
        "missing_text_files": missing,
        "n_populated": len(char_counts),
        "n_missing": len(missing),
    }


# ── Runner orchestration ─────────────────────────────────────────────────────

BACKEND_FNS = {
    "tesseract":   run_tesseract,
    "pymupdf4llm": run_pymupdf4llm,
    "mineru":      run_mineru,
    "marker":      run_marker,
    "doctr":       run_doctr,
    "claude_read": run_claude_read,
}


def load_existing_metrics() -> dict:
    if METRICS.exists():
        try:
            return json.loads(METRICS.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_metrics(data: dict) -> None:
    METRICS.parent.mkdir(parents=True, exist_ok=True)
    METRICS.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="OCR Lab komparatív runner")
    parser.add_argument("--backend", choices=BACKENDS_ALL + ["all"], default="all",
                        help="Melyik backend(et) futtassa. 'all' = mind, try/except-tel.")
    parser.add_argument("--report", action="store_true",
                        help="Csak újrameri a meglévő output-okat, nem futtat semmit.")
    args = parser.parse_args()

    if not MANIFEST.exists():
        sys.exit(f"HIBA: nincs manifest: {MANIFEST}")

    entries = load_manifest()
    print(f"Manifest: {len(entries)} oldal, {len(set(e['source'] for e in entries))} forrás")

    metrics = load_existing_metrics()
    metrics.setdefault("_meta", {})
    metrics["_meta"]["last_run"] = datetime.now().isoformat(timespec="seconds")
    metrics["_meta"]["manifest_n_pages"] = len(entries)

    backends = BACKENDS_ALL if args.backend == "all" else [args.backend]

    if args.report:
        # Csak claude_read és cache-elt fájlokra: mérjük újra a char count-okat
        result = run_claude_read(entries)
        metrics.setdefault("claude_read", {}).update(result)
        save_metrics(metrics)
        print(f"\nReport kész → {METRICS}")
        return 0

    for backend in backends:
        fn = BACKEND_FNS[backend]
        print(f"\n=== Backend: {backend} ===")
        try:
            result = fn(entries)
        except Exception:
            result = {"available": False, "error": traceback.format_exc()}
        metrics[backend] = result
        save_metrics(metrics)  # incrementally persist
        if result.get("available"):
            print(f"  ✓ {result.get('n_ok', '-')} OK, {result.get('n_err', '-')} hiba, "
                  f"avg {result.get('avg_time_per_page_s', '-')} s/page")
        else:
            print(f"  ✗ skip: {result.get('error', 'unknown')}")

    print(f"\nKész → {METRICS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
