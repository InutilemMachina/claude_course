"""Notebook-cell validátor: a analysis.ipynb minden code-cellájat sorrendben futtatja
egyetlen python folyamatban. Cél: gyors smoke-test, hogy a kód helyes. A plotok
.show() helyett .write_html-be mennek (csak hogy a Plotly object épüljön fel)."""
import json, sys, io
from pathlib import Path

# Force UTF-8 stdout (cp1250 default Windows magyar Python alatt)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

NB = Path(__file__).parent / "analysis.ipynb"
HTML_OUT = Path(__file__).parent / "_validate_charts.html"
nb = json.loads(NB.read_text(encoding="utf-8"))

# Patch: fig.show() → fig.write_html (smoke-only)
ns = {"__name__": "__main__"}
charts_html = ["<!DOCTYPE html><html><head><meta charset='utf-8'><title>OCR Lab charts</title></head><body>"]

for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell["source"])
    # Patch fig.show() to capture to charts list
    src_patched = src.replace(".show()", "._charts_html_buf = True")
    print(f"=== Cell {i} ===")
    try:
        exec(compile(src_patched, f"<cell-{i}>", "exec"), ns)
    except Exception as e:
        print(f"  ✗ FAIL: {type(e).__name__}: {e}")
        sys.exit(1)
    # Ha létrejött plotly Figure, mentsük HTML-be
    for name, obj in ns.items():
        if name.startswith("fig_") and hasattr(obj, "_charts_html_buf"):
            charts_html.append(f"<h2>{name}</h2>")
            charts_html.append(obj.to_html(include_plotlyjs="cdn", full_html=False))
            delattr(obj, "_charts_html_buf")
    print(f"  ✓ OK")

charts_html.append("</body></html>")
HTML_OUT.write_text("\n".join(charts_html), encoding="utf-8")
print(f"\nMinden cella futott. Charts → {HTML_OUT}")
