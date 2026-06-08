"""
_latex_png.py -- LaTeX math → átlátszó hátterű PNG konverter.

Használja: 10_pptx_gyarto.py (és bármely más script, amely képként
szeretne beágyazni matematikai képleteket).

Matplotlib mathtext motorját használja — NEM igényel rendszer-LaTeX
vagy dvipng telepítést. A `text.usetex` False marad.
"""

import hashlib
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend — must be set before pyplot import
import matplotlib.pyplot as plt


def _normalize(latex: str) -> str:
    """Collapse whitespace and strip surrounding dollar signs."""
    text = latex.strip()
    # strip leading/trailing single or double dollar signs
    text = re.sub(r"^\$+|\$+$", "", text)
    # join multi-line expressions; collapse internal whitespace
    text = " ".join(text.split())
    return text


def _cache_name(latex: str, fontsize: int, dpi: int, color: str) -> str:
    key = repr((latex, fontsize, dpi, color)).encode()
    h = hashlib.md5(key).hexdigest()[:10]
    return f"eq_{h}.png"


def render_latex_png(
    latex: str,
    out_dir,
    *,
    fontsize: int = 28,
    dpi: int = 200,
    color: str = "#1A1A2E",
) -> "Path | None":
    """Render egy LaTeX math stringet átlátszó hátterű PNG-vé, és visszaadja az elérési útját.

    - latex: a math tartalom $$ nélkül (a hívó hámozza le). Lehet
      többsoros; a sorok szóközzel egyesülnek, whitespace összeomlik.
    - out_dir: cache könyvtár (létrehozza, ha hiányzik). Fájlnév =
      (latex, fontsize, dpi, color) stabil hash-e → ismételt hívás
      cache-ből szolgál ki (nem rendereli újra, ha a fájl létezik).
    - Visszaadja a PNG Path-t, vagy None-t hiba esetén (soha nem dob kivételt).
    """
    try:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        norm = _normalize(latex)
        fname = _cache_name(norm, fontsize, dpi, color)
        out_path = out_dir / fname

        if out_path.exists() and out_path.stat().st_size > 0:
            return out_path

        fig = plt.figure(figsize=(6, 1.5))
        fig.text(
            0.5,
            0.5,
            f"${norm}$",
            fontsize=fontsize,
            color=color,
            ha="center",
            va="center",
        )
        fig.savefig(
            out_path,
            dpi=dpi,
            transparent=True,
            bbox_inches="tight",
            pad_inches=0.05,
        )
        plt.close(fig)
        return out_path

    except Exception as exc:  # noqa: BLE001
        print(f"⚠️  render_latex_png failed for {latex!r}: {exc}", file=sys.stderr)
        return None


if __name__ == "__main__":
    # CLI: python scripts/_latex_png.py "<latex>" [out_dir]
    if len(sys.argv) < 2:
        print("Usage: python scripts/_latex_png.py \"<latex>\" [out_dir]")
        sys.exit(1)

    latex_arg = sys.argv[1]
    out_dir_arg = sys.argv[2] if len(sys.argv) >= 3 else "./_latex_test"

    result = render_latex_png(latex_arg, out_dir_arg)
    if result is None:
        print("❌  Rendering failed.")
        sys.exit(1)
    print(result)
