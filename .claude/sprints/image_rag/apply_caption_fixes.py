"""
Block 1 — caption-javítás + needs_crop sync a katalógusban (v4 séma).

Stable key: (source_file, fájlnév-utolsó-komponens) — NEM fig_id.
Forráscsere esetén a fig_id-k eltolódnak, a stable key marad.

A captionek a user `_crop_tasks.md` NOTE-jaiból + a forrás-PDF-ek
ellenőrzéséből származnak (atg/1_het 2026-06-04 review). Mivel
😎-jóváhagyott szöveg, a script `caption_verified:true`-ra állítja.

Futtatás: python .claude/sprints/image_rag/apply_caption_fixes.py
"""
import json
from datetime import date
from pathlib import Path

CATALOG = Path("test_outputs/atg/1_het/2_clean_inputs/figure_catalog.json")

# (source_file, fájlnév) → caption-szöveg
CAPTIONS = {
    # chattopadhyay2013_paper.pdf
    ("chattopadhyay2013_paper.pdf", "p002_fig001.png"): "Figure 1: Tree diagram of compressor instability",
    ("chattopadhyay2013_paper.pdf", "p003_fig001.png"): "Figure 2: Tree diagram of prevention method",
    ("chattopadhyay2013_paper.pdf", "p004_fig001.png"): "Figure 3: Tree diagram of stall control.",

    # gravdahl1999_chapter.pdf
    ("gravdahl1999_chapter.pdf", "p004_fig001.png"): "Figure 1.1: Blade rows (Cylindrical cross section).",
    ("gravdahl1999_chapter.pdf", "p005_fig001.png"): "Figure 1.2: One stage of an axial compressor (Axial cross section).",
    ("gravdahl1999_chapter.pdf", "p006_fig001.png"): "Figure 1.3: Diagrammatic sketch of a radially vaned centrifugal compressor. Shown here with a vaned diffuser.",
    ("gravdahl1999_chapter.pdf", "p007_fig001.png"): "Figure 1.4: Diagrammatic sketch of centrifugal compressor fitted with a volute.",
    ("gravdahl1999_chapter.pdf", "p008_fig001.png"): "Figure 1.5: Sketch of simple gas turbine.",
    ("gravdahl1999_chapter.pdf", "p010_fig001.png"): "Figure 1.6: Different types of gas turbine type of engines for aircraft propulsion. a) Turbojet, b) Turboprop, c) Turbofan, d) Turboshaft",
    ("gravdahl1999_chapter.pdf", "p012_fig001.png"): "Figure 1.7: Pipeline compressor powered by gas turbine.",
    ("gravdahl1999_chapter.pdf", "p013_fig001.png"): "Figure 1.8: A turbocharged engine with constant pressure turbocharging.",
    ("gravdahl1999_chapter.pdf", "p015_fig001.png"): "Figure 1.9: Compressor characteristic with deep surge cycle, de Jager (1995).",
    ("gravdahl1999_chapter.pdf", "p016_fig001.png"): "Figure 1.10: Compressor characteristic.",
    ("gravdahl1999_chapter.pdf", "p018_fig001.png"): "Figure 1.11: Physical mechanism for inception of rotating stall, Emmons et.al. (1955).",
    ("gravdahl1999_chapter.pdf", "p020_fig001.png"): "Figure 1.12: Schematic drawing of hysteresis caused by rotating stall. Solid lines represent stable equilibria and dotted lines represent unstable equilibria. The dashed lines are the throttle lines for the onset and clearing of stall.",
    ("gravdahl1999_chapter.pdf", "p022_fig001.png"): "Figure 1.13: Basic compression system",
    ("gravdahl1999_chapter.pdf", "p025_fig001.png"): "Figure 1.14: Statically unstable (A), dynamically unstable (B), and Stable (C) operating points.",
    ("gravdahl1999_chapter.pdf", "p028_fig001.png"): "Figure 1.15: Simulations of the Moore-Greitzer model. All states are plotted versus nondimensional time ξ. The curves to the left are with B = 1, and surge oscillations are seen. The curves to the right are with B = 0.4, and rotating stall is the result.",
    ("gravdahl1999_chapter.pdf", "p037_fig001.png"): "Figure 1.16: Information flow for jet engine model.",
    ("gravdahl1999_chapter.pdf", "p040_fig001.png"): "Figure 1.17: Surge margin",

    # tavakoli2004_paper.pdf
    ("tavakoli2004_paper.pdf", "p002_fig001.png"): "Fig. 1. Compressor map with stalled flow characteristics.",
    ("tavakoli2004_paper.pdf", "p002_fig002.png"): "Fig. 2. Compressor map with deep surge cycle.",
    ("tavakoli2004_paper.pdf", "p003_fig001.png"): "Fig. 3. Compressor map with surge line.",
    ("tavakoli2004_paper.pdf", "p003_fig002.png"): "Fig. 4. Compressor map with efficiency contours.",
    ("tavakoli2004_paper.pdf", "p003_fig003.png"): "Fig. 5. Compressor map with surge avoidance line.",

    # wikipedia2024_webpage.pdf
    ("wikipedia2024_webpage.pdf", "p001_fig001.png"): "Comparison of normal and distorted airflow into the compressor section",
    ("wikipedia2024_webpage.pdf", "p001_fig002.png"): "An animation of an axial compressor showing both the stator blades and the rotor blades",
    ("wikipedia2024_webpage.pdf", "p003_fig001.png"): "Sukhoi Su-57 prototype suffering a compressor stall at MAKS 2011",
}

# Ezek a bejegyzések needs_crop:true maradnak (a friss regen full-page rendert
# ad rájuk; user kézi vágás vár):
KEEP_NEEDS_CROP_TRUE: set[tuple[str, str]] = set()


def _all_figures(catalog):
    for src_data in catalog["sources"].values():
        yield from src_data["figures"]


def main():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    cap_changed = verified_changed = crop_changed = 0
    unmatched: list[tuple[str, str]] = []

    for entry in _all_figures(catalog):
        fname = Path(entry.get("path", "")).name
        key = (entry.get("source_file") or "", fname)
        # source_file nincs entry-szinten v4-ben — keressük a parent kulcsból
        # (a _all_figures iterátor nem hozza, ezért kiegészítés szükséges)
        # Ezt rendezzük lent egy második iterációban; itt csak placeholder.
        if key in CAPTIONS:
            pass  # handled below

    # Második menet — kulcs (source_file, fname) parent-source alapján
    for src_name, src_data in catalog["sources"].items():
        for entry in src_data["figures"]:
            fname = Path(entry.get("path", "")).name
            key = (src_name, fname)
            if key not in CAPTIONS:
                unmatched.append(key)
                continue
            new_cap = CAPTIONS[key]
            if entry.get("caption") != new_cap:
                entry["caption"] = new_cap
                cap_changed += 1
            # User-eredetű caption → caption_verified true
            if not entry.get("caption_verified"):
                entry["caption_verified"] = True
                verified_changed += 1
            # needs_crop átállítása csak ahol explicit kérjük (üres set = nincs)
            desired = key in KEEP_NEEDS_CROP_TRUE
            if entry.get("needs_crop", False) != desired:
                entry["needs_crop"] = desired
                crop_changed += 1

    # _status újraszámolás — 4-állapotú logika (Block 9)
    for entry in _all_figures(catalog):
        caption_ok = bool(entry.get("caption_verified"))
        has_meta   = bool(entry.get("visual_content"))
        if caption_ok and has_meta:   entry["_status"] = "complete"
        elif caption_ok:              entry["_status"] = "caption-ok"
        elif has_meta:                entry["_status"] = "draft"
        else:                         entry["_status"] = "un-processed"

    catalog.setdefault("_meta", {})["last_updated"] = date.today().isoformat()
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2),
                       encoding="utf-8")
    print(f"Captions updated:        {cap_changed}")
    print(f"caption_verified→true:   {verified_changed}")
    print(f"needs_crop flipped:      {crop_changed}")
    print(f"Unmatched (no mapping):  {len(unmatched)}")
    if unmatched:
        print(f"  Examples: {unmatched[:5]}")


if __name__ == "__main__":
    main()
