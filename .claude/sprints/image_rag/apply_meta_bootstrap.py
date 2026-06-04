"""
Block 4 pilot — image_rag meta-mezők (visual_content, text_context, keywords)
feltöltése a figure_catalog.json (v4) bejegyzéseihez. Stable key:
(source_file, fájlnév-utolsó-komponens) — NEM fig_id.

Pilot scope (2026-06-04, atg/1_het):
  chattopadhyay2013_paper (3 ábra) + tavakoli2004_paper (5 ábra) = 8 entry.

A 02b skill protokollja: .claude/skills/02b_figure_enricher.md
Sprint kontextus: .claude/sprints/image_rag/image_rag_plan.md

A script csak null/üres mezőket tölti — idempotens. A caption_verified
mezőhöz NEM nyúl (az 02b enricher feladata: a 02b kiszedi a semantic
mezőket, a 😎 állítja true-ra a caption_verified-et). HA azonban a
caption már user-által verified (apply_caption_fixes.py után), a
visual_content kitöltés után a _status: 'verified' marad.

Futtatás: python .claude/sprints/image_rag/apply_meta_bootstrap.py
"""
import json
from datetime import date
from pathlib import Path

CATALOG = Path("test_outputs/atg/1_het/2_clean_inputs/figure_catalog.json")

META: dict[tuple[str, str], dict] = {
    # ─── chattopadhyay2013_paper.pdf ─────────────────────────────────────────
    ("chattopadhyay2013_paper.pdf", "p002_fig001.png"): {
        "visual_content": "Hierarchikus fa-diagram. Gyökér: 'Compressor Instability'. "
            "Két fő ág: Linear / Non Linear. A Non Linear alatt 'Fluid Dynamic Instability' "
            "(Stall: Incipient/Fully Developed; Surge: Mild/Classical/Modified/Deep) és "
            "'Aero Elastic Instability' (Blade/Stall/Surge Flutter). Stall és Surge "
            "frekvencia-tartomány zárójelben (>25 Hz, ill. <25 Hz).",
        "text_context": "A paper bevezető szekciójának vége, közvetlenül a 'Instability and "
            "Its Causes' alfejezet előtt. A szerző itt taxonómiát ad a kompresszor "
            "instabilitások típusairól, mielőtt az okokra tér. Hivatkozás: p3 "
            "'tree diagram above (Figure 1)'.",
        "keywords": ["compressor instability", "taxonomy", "stall", "surge",
                     "flutter", "fluid dynamic instability", "aeroelastic"],
    },
    ("chattopadhyay2013_paper.pdf", "p003_fig001.png"): {
        "visual_content": "Fa-diagram. Gyökér: 'PREVENTION METHODS (As Tactical plan)'. "
            "Három ág: AVOIDANCE (Unload by opening throttle / changing operating point), "
            "CONTROL (Regulate or refresh), SUPPRESSION (Energize the flow). A CONTROL "
            "tovább osztva: ACTIVE (Open Loop / Close Loop / Flow Control) és PASSIVE "
            "(Compressor Casing Treatment).",
        "text_context": "A 'Control or Mitigation of Instability' szekció kezdetén. "
            "A diagram a megelőzési stratégiák magas-szintű kategorizálását adja. "
            "Hivatkozás: p4 'following tree diagram (Figure 2)'.",
        "keywords": ["prevention", "control strategy", "avoidance", "suppression",
                     "active control", "passive control", "casing treatment"],
    },
    ("chattopadhyay2013_paper.pdf", "p004_fig001.png"): {
        "visual_content": "Fa-diagram. Gyökér: 'Control'. Négy ág: Approach (Single sided / "
            "Double sided injection), Technique ('Safe game' / 'Shift the boundary'), "
            "Vary operating control (Bleed valve / Engine control), Method "
            "(Atmospheric air injection / Downstream compressed air).",
        "text_context": "A 'Control Strategy' szekció zárása. Két fő stratégia: "
            "'safe game' (üzemvonal a surge alatt) és 'shift dangerous boundary' "
            "(surge vonal feljebb tolása). Hivatkozás: p4 'following tree diagram (Figure 3)'.",
        "keywords": ["stall control", "safe game strategy", "boundary shifting",
                     "injection control", "bleed valve", "FADEC"],
    },

    # ─── tavakoli2004_paper.pdf ──────────────────────────────────────────────
    ("tavakoli2004_paper.pdf", "p002_fig001.png"): {
        "visual_content": "Kompresszor-jelleggörbe (PR vs Mass flow). Felső görbe a stabil "
            "(unstalled) működés; 'A' pont a stabil görbén, függőleges nyíllal lefelé mutat "
            "egy 'B' pontba a 'Stalled' jelölésű alsó görbén. A rotating stall belépését szemlélteti.",
        "text_context": "A '2. ROTATING STALL' szekció vége. A szerző leírja, hogy a "
            "rotating stall belépésekor az üzempont az AB egyenes mentén ugrik át a "
            "stalled karakterisztikára. Hivatkozás: p2 'Figure 1 shows a typical "
            "rotating stall pattern'.",
        "keywords": ["rotating stall", "compressor map", "stalled characteristic",
                     "operating point jump", "pressure ratio"],
    },
    ("tavakoli2004_paper.pdf", "p002_fig002.png"): {
        "visual_content": "Kompresszor-jelleggörbe (PR vs Mass flow), zárt deep surge "
            "ciklust ábrázol. Négy pont az óramutatóval ellentétes irányú hurkon: A, B, C, D. "
            "A görbe az A→B→C→D→A teljes deep surge ciklust mutatja.",
        "text_context": "A '3. FUNDAMENTALS OF SURGE' szekció. A szerző tárgyalja, "
            "hogyan alakul ki a surge oscillation: hirtelen pressure ratio drop, "
            "reverse flow, recovery, vissza A-ra. Hivatkozás: p3 'large amplitude "
            "limit cycle oscillations'.",
        "keywords": ["deep surge", "surge cycle", "limit cycle oscillation",
                     "reverse flow", "compressor map"],
    },
    ("tavakoli2004_paper.pdf", "p003_fig001.png"): {
        "visual_content": "Kompresszor-jelleggörbe (PR vs Mass flow). Több speed-line, "
            "mindegyik csúcs-pontjait összekötő 'Surge line' a bal oldalon. Nyíl jelöli a "
            "'Speed' növekedési irányt.",
        "text_context": "A '4. SURGE LINE' szekció eleje. A szerző bevezeti a surge "
            "line fogalmát mint a stabil és instabil tartomány határát. Hivatkozás: "
            "p3 'a barrier that separates the stable and unstable regions'.",
        "keywords": ["surge line", "speed lines", "compressor map", "stability boundary",
                     "characteristic slope"],
    },
    ("tavakoli2004_paper.pdf", "p003_fig002.png"): {
        "visual_content": "Kompresszor-jelleggörbe (PR vs Mass flow). Speed-line családok "
            "egymást keresztező görbékkel, efficiency contour-okkal. 'Surge line', "
            "'Efficiency' és 'Constant efficiency regions' feliratok.",
        "text_context": "A SURGE LINE szekció második fele. A kompresszor map teljes "
            "ábrázolása efficiency contour-okkal, demonstrálva a peak performance régió "
            "viszonyát a surge line-hoz.",
        "keywords": ["compressor map", "efficiency contours", "surge line",
                     "peak efficiency", "performance map"],
    },
    ("tavakoli2004_paper.pdf", "p003_fig003.png"): {
        "visual_content": "Kompresszor-jelleggörbe (PR vs Mass flow). Két párhuzamos görbe "
            "a bal oldalon: 'Surge line' (belső) és 'Surge avoidance line' (külső, jobbra "
            "tolva). A köztük lévő távolság a surge margin.",
        "text_context": "A 'SURGE MARGIN' szekció. A surge avoidance stratégia: a "
            "kompresszor üzemeltetését a surge line-tól eltolt avoidance vonalon belül "
            "kell tartani.",
        "keywords": ["surge avoidance", "surge margin", "safety boundary",
                     "compressor map", "control strategy"],
    },
}


def _is_empty(val) -> bool:
    if val is None:
        return True
    if isinstance(val, (str, list, dict)) and not val:
        return True
    return False


def _all_figures(catalog):
    for src_data in catalog["sources"].values():
        yield from src_data["figures"]


def main():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    changed = filled = untouched = skipped = 0

    for src_name, src_data in catalog["sources"].items():
        for entry in src_data["figures"]:
            fname = Path(entry.get("path", "")).name
            key = (src_name, fname)
            meta = META.get(key)
            if meta is None:
                continue
            modified = False
            for field, value in meta.items():
                if _is_empty(entry.get(field)):
                    entry[field] = value
                    filled += 1
                    modified = True
                else:
                    untouched += 1
            if modified:
                changed += 1
            else:
                skipped += 1

    # _status újraszámolás
    for entry in _all_figures(catalog):
        if entry.get("caption_verified"):
            entry["_status"] = "verified"
        elif entry.get("visual_content"):
            entry["_status"] = "draft"
        else:
            entry["_status"] = "un-processed"

    catalog.setdefault("_meta", {})["last_updated"] = date.today().isoformat()
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2),
                       encoding="utf-8")
    print(f"Entries modified: {changed}  |  Already filled: {skipped}  |  "
          f"Fields written: {filled}  |  Untouched: {untouched}")


if __name__ == "__main__":
    main()
