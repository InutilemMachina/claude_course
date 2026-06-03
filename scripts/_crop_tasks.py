"""
_crop_tasks.py — Crop-feladatlista generálás és checkbox→catalog szinkron.

Standalone utility; a 02_source_extractor.py dynamikusan tölti be.

Funkciók:
    generate_crop_tasks(week_dir)  — figure_catalog.json → _crop_tasks.md
    sync_crop_tasks(week_dir)      — [x] jelölések → catalog needs_crop: false
"""

import json
import re
from datetime import date
from pathlib import Path


# ── Belső segédek ──────────────────────────────────────────────────────────────

def _load_catalog(clean_in: Path) -> list:
    cat_path = clean_in / "figure_catalog.json"
    if not cat_path.exists():
        raise FileNotFoundError(f"Nem található: {cat_path}")
    return json.loads(cat_path.read_text(encoding="utf-8"))


def _save_catalog(catalog: list, clean_in: Path) -> None:
    cat_path = clean_in / "figure_catalog.json"
    cat_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2),
                        encoding="utf-8")


def _cit_key(source_file: str, catalog: list) -> str:
    """A forráshoz tartozó citation_key (az első bejegyzésből)."""
    for e in catalog:
        if e.get("source_file") == source_file:
            return str(e.get("citation_key", "?"))
    return "?"


def _week_label(week_dir: Path) -> str:
    """'atg/1_het' stílusú label a week_dir abszolút útjából."""
    parts = week_dir.parts
    if len(parts) >= 2:
        return f"{parts[-2]}/{parts[-1]}"
    return week_dir.name


# ── Publikus API ───────────────────────────────────────────────────────────────

def generate_crop_tasks(week_dir: Path) -> None:
    """
    Beolvassa a figure_catalog.json-t és kiírja a _crop_tasks.md-t.
    Csak needs_crop: true bejegyzések kerülnek bele, forrás szerint
    csoportosítva (ABC sorrendben).
    """
    week_dir = Path(week_dir).resolve()
    clean_in = week_dir / "2_clean_inputs"
    md_path  = clean_in / "_crop_tasks.md"

    catalog = _load_catalog(clean_in)
    pending = [e for e in catalog if e.get("needs_crop")]

    if not pending:
        md_path.write_text("# Crop tasks\n\nNincs függő crop.\n",
                           encoding="utf-8")
        print(f"  _crop_tasks.md: nincs függő crop → üres fájl írva")
        return

    # Források gyűjtése ABC sorrendben
    sources_ordered = sorted({e["source_file"] for e in pending})
    today = date.today().isoformat()
    label = _week_label(week_dir)

    lines = []
    lines.append(f"# Crop tasks — {label}")
    lines.append(f"_{len(pending)} vár | Frissítve: {today}_")
    lines.append("")
    lines.append("---")

    for src_file in sources_ordered:
        entries = [e for e in pending if e["source_file"] == src_file]
        cit_k = _cit_key(src_file, catalog)
        lines.append("")
        lines.append(f"## {src_file}  [cit:{cit_k}]")
        for e in entries:
            fig_id    = e["id"]
            filename  = Path(e["filename"]).name          # csak a fájlnév
            rel_path  = e["filename"]                     # relatív a week_dir-hez
            page      = e.get("page", "?")
            lines.append(
                f"- [ ] <!-- {fig_id} --> `{filename}`  · oldal {page}"
                f"  · `{rel_path}`"
            )

    lines.append("")   # záró newline

    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  _crop_tasks.md: {len(pending)} bejegyzés írva → {md_path}")


def sync_crop_tasks(week_dir: Path) -> int:
    """
    Beolvassa a _crop_tasks.md-t, megkeresi a kész ([x]) sorokat,
    frissíti a catalog-ban needs_crop: false-ra, majd regenerálja
    a _crop_tasks.md-t (kész elemek eltűnnek).

    Visszatérés: frissített bejegyzések száma.
    """
    week_dir = Path(week_dir).resolve()
    clean_in = week_dir / "2_clean_inputs"
    md_path  = clean_in / "_crop_tasks.md"

    if not md_path.exists():
        print(f"  WARN: nem található: {md_path} — sync kihagyva", flush=True)
        return 0

    text = md_path.read_text(encoding="utf-8")

    # Kész sorok: - [x] <!-- fig_NNN -->
    done_ids = re.findall(r"-\s*\[x\]\s*<!--\s*(fig_\w+)\s*-->", text,
                          flags=re.IGNORECASE)

    if not done_ids:
        print("  sync: nincs [x] jelölt sor — semmi teendő")
        return 0

    catalog = _load_catalog(clean_in)
    updated = 0
    id_set = set(done_ids)

    for entry in catalog:
        if entry["id"] in id_set and entry.get("needs_crop"):
            entry["needs_crop"] = False
            updated += 1

    if updated:
        _save_catalog(catalog, clean_in)
        print(f"  sync: {updated} bejegyzés frissítve (needs_crop → false)")
        generate_crop_tasks(week_dir)   # regenerálás, kész elemek nélkül
    else:
        print("  sync: a jelölt fig_id-k nem találhatók a catalog-ban "
              "(talán már szinkronizálva)")

    return updated
