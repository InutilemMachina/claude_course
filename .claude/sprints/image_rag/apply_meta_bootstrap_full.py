"""
apply_meta_bootstrap_full.py — atg/1_het maradék entry-k meta-feltöltése (image_rag_OCR sprint).

Bővíti az apply_meta_bootstrap.py 8 entry-jét (chattopadhyay+tavakoli) a következő
forrás-csoportokkal:
  - wikipedia2024_webpage.pdf (3)  → demonstration scope (jelen session)
  - hari2025_slides.pptx     (8)  → demonstration scope (jelen session)
  - gravdahl1999_chapter.pdf (17) → Backlog (külön session)
  - nagyi2013_eloadas.pdf    (31) → Backlog (külön session)

Stable lookup-kulcs: (source_file, Path(path).name) — fig_NNN nem stabil.
Idempotens: csak null/üres mezőket tölt; caption_verified-hez NEM nyúl.

Futtatás:
    python .claude/sprints/image_rag/apply_meta_bootstrap_full.py
"""
import json
from datetime import date
from pathlib import Path

CATALOG = Path("test_outputs/atg/1_het/2_clean_inputs/figure_catalog.json")

META: dict[tuple[str, str], dict] = {

    # ─── wikipedia2024_webpage.pdf ───────────────────────────────────────────
    # Mind a 3 entry caption-ok státuszban → visual_content + text_context + keywords kell.
    ("wikipedia2024_webpage.pdf", "p001_fig001.png"): {
        "visual_content": "Két stilizált sugárhajtómű-bemenet keresztmetszete egymás "
            "alatt. Felül 'Normal inlet airflow' egyenletes párhuzamos kék nyilakkal a "
            "kompresszorlapátok közé; alul 'Distorted inlet airflow' szögelt, "
            "szabálytalan nyilakkal — szemlélteti, hogy ferde / örvénylő beáramlás "
            "milyen aszimmetrikus terhelést okoz a kompresszorszekciónak.",
        "text_context": "A Wikipedia 'Compressor stall' szócikk bevezető szekciója — "
            "a distortion mint az instabilitások egyik kiváltó oka. Hivatkozás: p1 "
            "képszöveg + főszöveg ('inlet distortion').",
        "keywords": ["inlet distortion", "compressor stall", "airflow", "wikipedia",
                     "schematic", "comparison"],
    },
    ("wikipedia2024_webpage.pdf", "p001_fig002.png"): {
        "visual_content": "Animált 3D render axiális kompresszorról — világoskék "
            "rotor- és statorlapát-sorok, izometrikus nézet. Stilizált szemléltetés a "
            "rotor és stator viszonyáról.",
        "text_context": "Wikipedia compressor stall szócikk háttér-magyarázat: "
            "az axiális kompresszor alapfelépítése a stall jelenség kontextusához.",
        "keywords": ["axial compressor", "rotor", "stator", "3D illustration",
                     "wikipedia", "animation"],
    },
    ("wikipedia2024_webpage.pdf", "p003_fig001.png"): {
        "visual_content": "Fotó: Sukhoi Su-57 prototípus sugárhajtóműve a MAKS 2011 "
            "kiállításon, hátsó hajtómű-fúvókából érzékelhető láng kiáramlása — "
            "kompresszor stall okozta utóégetés-jellegű effektus a take-off során.",
        "text_context": "Wikipedia compressor stall szócikk 'Notable incidents' "
            "szekciójához tartozó illusztráció — valós eseménnyel demonstrálja a "
            "stall vizuális megjelenését.",
        "keywords": ["compressor stall", "Sukhoi Su-57", "MAKS 2011", "flame-out",
                     "real-world incident", "wikipedia"],
    },

    # ─── hari2025_slides.pptx (8 db) ─────────────────────────────────────────
    # Magyar nyelvű rezgésdiagnosztika oktatóanyag (DLI / 3N akadémia).
    # Tipikus tartalom: kompresszor / szivattyú / ventilátor lapát-elhaladási
    # frekvenciás spektrumok, magyarázó ábrákkal.
    ("hari2025_slides.pptx", "p003_fig001.png"): {
        "visual_content": "Sematikus spektrum-diagram (Amplitúdó vs Order szám). Csúcsok: "
            "1X (alapharmonikus), BP (blade pass — lapátelhaladási frekvencia, ~8. order), "
            "2BP (~16. order) Radiális jelöléssel. Jobb oldalon stilizált radiális ventilátor "
            "járókerék 7 lapáttal. A BP csúcs a lapátszám × forgási frekvencia eredménye.",
        "text_context": "A hari2025 dia bevezetése a lapát-elhaladási frekvencia (BP) "
            "fogalmához ventilátoroknál. A spektrumcsúcs BP és többszörösei azonosítják "
            "a lapátszámot.",
        "keywords": ["blade pass frequency", "BP", "spektrum", "ventilátor",
                     "rezgésdiagnosztika", "harmonikus", "radiális"],
    },
    ("hari2025_slides.pptx", "p004_fig001.png"): {
        "visual_content": "Részletes rezgésspektrum (mm/s rms vs Orders, 0–10). Felirat "
            "tetején: 1X, 2X, MFB, PV, 5X–8X order-jelölésekkel; jobbra fent timestamp "
            "'2005.04.06. 2985 RPM' és 'Radial' jelölés. A PV (Pump Vane, ~4X) a "
            "domináns csúcs ~1.0 mm/s; MFB (~3X) szintén kiemelkedő. Linear range.",
        "text_context": "Valós mérési spektrum centrifugális szivattyú radiális irányában. "
            "A PV (Pump Vane = lapátszám × fordulatszám) és MFB csúcsok elemzése.",
        "keywords": ["PV", "Pump Vane", "MFB", "centrifugális szivattyú",
                     "spektrum", "mérési adat", "radial", "rezgésdiagnosztika"],
    },
    ("hari2025_slides.pptx", "p005_fig001.png"): {
        "visual_content": "Sematikus spektrum (Amplitúdó vs Order szám, 0–40). Két "
            "tiszta csúcs: 1X (alapharmonikus) és VP (~8X, vane pass). Jobbra "
            "stilizált centrifugális járókerék 7 ívelt lapáttal. A 16–40 order-tartományban "
            "alacsony amplitúdójú zaj-szőnyeg.",
        "text_context": "Sematikus illusztráció centrifugális szivattyú spektrumáról — "
            "VP csúcs azonosítása az ívelt-lapátos járókerékkel.",
        "keywords": ["VP", "vane pass", "centrifugális járókerék", "spektrum",
                     "sematikus", "szivattyú"],
    },
    ("hari2025_slides.pptx", "p006_fig001.png"): {
        "visual_content": "Magas-tartományú rezgésspektrum (mm/s rms vs High range orders, "
            "0–100). Időjelölés '2005.04.12. 2985 RPM' Radial. Bal oldali tüskés "
            "alacsony-order zóna (1–20 order, MB jelöléssel), majd a 60–80 order között "
            "széles, dombszerű kavitáció-jelű spektrum-jel ~0.4 mm/s amplitudóval.",
        "text_context": "Centrifugális szivattyú spektrum kavitációs jellel — a magas "
            "frekvenciás 'fehér zaj'-szerű spektrum-dudor a kavitáció buborék-összeroppanás "
            "indikátora.",
        "keywords": ["kavitáció", "fehér zaj", "high range", "spektrum", "szivattyú",
                     "diagnosztika"],
    },
    ("hari2025_slides.pptx", "p007_fig001.png"): {
        "visual_content": "Sematikus spektrum (Amplitúdó vs Order szám, 0–5). Bal alsó "
            "sarkban dupla alacsony-amplitúdójú csúcs (~0.5X tartomány), és egy domináns "
            "1X csúcs. Jobbra stilizált 8-lapátos radiális járókerék. Az 1X alatti "
            "alharmonikus jellemző mechanikai eredetű hibák jele.",
        "text_context": "Sematikus illusztráció rezgésspektrum 1X alapharmonikusáról — "
            "alharmonikus zónát is jelöl, ami pl. olajfilm-instabilitás vagy hézagosság jele.",
        "keywords": ["1X", "alapharmonikus", "alharmonikus", "spektrum",
                     "ventilátor", "sematikus"],
    },
    ("hari2025_slides.pptx", "p008_fig001.png"): {
        "visual_content": "Részletes rezgésspektrum (mm/s rms 0–0.2 vs Orders 0–10). "
            "Tetején order-jelölések 1X-9X + MFB, PV. Időjelölés '2005.05.05. 2973 RPM' "
            "Radial. Sok alacsony amplitúdójú csúcs, MFB (~4X) a legmagasabb (~0.06), "
            "1X kb. 0.1. Tipikus 'jó' kompresszor / szivattyú spektrum, sok small peak.",
        "text_context": "Mérési spektrum — alacsony rezgésszint, MFB és 1X csúcsok "
            "egyensúlya, jó gépállapot referencia.",
        "keywords": ["MFB", "PV", "rezgésspektrum", "low amplitude", "referencia",
                     "diagnosztika"],
    },
    ("hari2025_slides.pptx", "p009_fig001.png"): {
        "visual_content": "Sematikus order-spektrum: csak PV-többszörösei csúcsokkal "
            "(PV, 2PV, 3PV, 4PV, és egy elkülönült 8PV). A csúcsok egyenletes "
            "távolságúak, ami tisztán a lapát-elhaladási frekvencia harmonikus sorozata.",
        "text_context": "Sematikus illusztráció: a Pump Vane frekvencia és felharmonikusai "
            "a spektrumban — ideális esetben csak PV-többszörösei jelennek meg.",
        "keywords": ["PV", "2PV", "harmonikus sorozat", "sematikus", "spektrum",
                     "szivattyú"],
    },
    ("hari2025_slides.pptx", "p016_fig001.png"): {
        "visual_content": "Részletes rezgésspektrum (mm/s rms 0–0.3 vs Low range orders 0–10). "
            "Tetején order-jelölések: 1XM, 1XI, 2XM, 2XI, 1XC, FC, 2XC. Időjelölés "
            "'2005.04.19. 2992 RPM' Radial. A 2XM/2XI (~2X) csúcs a domináns (~0.28), "
            "az 1XM/1XI (~1X) kb. 0.13. Index 'M' (motor) és 'I' (impeller) megkülönbözteti "
            "a motorhoz és járókerékhez tartozó harmonikusokat egy összekapcsolt rendszerben.",
        "text_context": "Motorral közvetlen kapcsolt szivattyú-rendszer spektruma — a "
            "motor-oldali (M) és impeller-oldali (I) harmonikusok elkülönített jelölése "
            "lehetővé teszi a hiba forrásának azonosítását.",
        "keywords": ["1XM", "2XM", "motor harmonikus", "impeller harmonikus", "spektrum",
                     "kapcsolt rendszer", "rezgésdiagnosztika"],
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
        caption_ok = bool(entry.get("caption_verified"))
        has_meta   = bool(entry.get("visual_content"))
        if   caption_ok and has_meta: entry["_status"] = "complete"
        elif caption_ok:              entry["_status"] = "caption-ok"
        elif has_meta:                entry["_status"] = "draft"
        else:                         entry["_status"] = "un-processed"

    catalog.setdefault("_meta", {})["last_updated"] = date.today().isoformat()
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2),
                       encoding="utf-8")
    print(f"Entries modified: {changed}  |  Already filled (skipped): {skipped}  |  "
          f"Fields written: {filled}  |  Untouched: {untouched}")


if __name__ == "__main__":
    main()
