---
title: Project Status — claude_course
type: project_status
tags: [meta]
updated: 2026-06-12
---

# Project Status — claude_course

## Aktuális fázis

**End-to-end átfésülés folyamatban** — a belépési ponttól lépésről lépésre, `atg` + `dft` teszttárgyakon.
Kész: meta-réteg (CLAUDE/Instructions/pipeline) + `00_init` + `01_source_collector` (citáció-rendszerrel).

**Haladás (skill-tesztelési kör):**
1. ✅ `skill_template.md` best-practice overhaul → B-07 részben.
2. ✅ Skillek tesztje: `00_init` + `01_source_collector` + `02_image_extraction` — mind sablon-konform, verifikált → B-08 kész.
3. ✅ `03_mindmap_builder` tesztelve: skill spec javítva (v1.1), mindmap draft generálva `atg/1_het` — checkpoint vár.

**02_image_extraction — lezárt fejlesztések (2026-06-03):**
- Átnevezés: `02_source_extractor` → `02_image_extraction` (skill + script + összes hivatkozás)
- Vektoros ábra detektálás born-digital PDF-eknél (`get_drawings()` + false positive szűrő)
- Wikipedia false positive javítás (vízszintes elválasztók + apró elemek kizárva)
- `_crop_tasks.md`: caption mező hozzáadva szkennelt oldalakhoz
- Kettős tördelés kezelése: straddle oldal félbevágása PyMuPDF `show_pdf_page(clip=...)` segítségével
- PDF darabolás multi-week forráshoz (`hesselmann1983_ch01/02/03.pdf`)
- Tesztfutás: `atg/1_het` → 36 kép; `dft` 3 het → 23 kép; mind `needs_crop: true` ahol várható
- Skill + Instructions + Backlog frissítve (kettős tördelés, front matter, gyökérok-elv, TOC-alapú határdetektálás ötlet)

## Elkészült (✅)

- ✅ Repo struktúra (`claude_course/`)
- ✅ `CLAUDE.md`, `Instructions.md`, `pipeline.md`
- ✅ `skill_template.md`
- ✅ Skills 00–13: 00–11 kész (03 + 04 sarokkövek), 12–13 tervezett stub (youtube/jupyter)
- ✅ Scripts: portolva, refaktorálva, átnevezve az `NN-M_name` sémára
- ✅ Script számozási séma alkotmányosan rögzítve (`Instructions.md §5.1`)
- ✅ Meta-fájlok deduplikálva — "egy utasítás egy helyen" elv érvényesítve
- ✅ `00_init_course.py`: `WEEK_SUBDIRS` javítva (`3_raw_outputs` → `3_mindmap`)
- ✅ `15_backlog_index.py` → `_backlog_index.py` (utility, nem pipeline-lépés)
- ✅ `08_ieee_renderer.py` → `_ieee_renderer.py` (utility, nem lépés-specifikus)
- ✅ `startswith('#')` bug javítva a `_backlog_index.py`-ban
- ✅ Meta-réteg átfésülve: CLAUDE.md index, soft-cap, vertikális Mermaid, D1/D2 deduplikáció
- ✅ `00_init` állomás: `context.json` fikció → `subject_status.md` (frontmatter gépi, törzs emberi); sablon NLM-mentes; tábla auto-generált, igazított

## Backlog (🔲)

- 🔲 B-01: `atg` pipeline lépésteszt (01 → 10, megállva minden checkpointnál)
- 🔲 B-02: `dft` pipeline lépésteszt (1 könyvfejezet feldolgozása)
- ✅ B-03: Citáció-rendszer egységesítve — egyetlen `citations.json` (`type`-alapú IEEE), `[1]` jelölés, NLM-kód törölve, `_ieee_renderer` tesztelve — **kész**
- ✅ B-04: `00_init_course.py` tesztelve (`3_mindmap/` + subject_status generálás) — **kész**
- ⚙️ B-05: Jupyter szemléltetés — `13_jupyter_catalogizer` v1.1: **didaktikai metaprompt előtöltve** (POE 3-cella, magyarázat-visszatartás, rugalmas horgony). Hátravan: **regiszter-mechanika** (külön táblázatos regiszter, fájlnév-konvenció, csatolmány stabil hivatkozása). `status: planned` marad.
- ⚙️ B-06: YouTube/médialink — `12_youtube_finder` v1.1: **didaktikai metaprompt előtöltve** (rugalmas horgony, keresési spec, „Nézd és elemezd" CTML + time-stamp). Hátravan: **regiszter-mechanika** (külön táblázatos regiszter, csatolmány-szintaxis, a videólista bővülés/szűkülés kezelése). `status: planned` marad.
  - **Skill-elvárás (2026-06-08):** ideálisan minden bekezdéshez (értsd: minden `###` alfejezet szövegbekezdéséhez) legalább egy videó találandó. A skill ne csak egyetlen kiemelt bekezdést keressen, hanem végigmenjen a teljes fejezeten és minden bekezdéshez jelöljön ki jelöltet — még ha végül nem mindegyikhez lesz releváns találat.
- 🔲 B-07: `skill_template.md` best-practice felülvizsgálata — felépítés + hol éljen (`.claude/` vs `templates/`)
- ✅ B-08: 00, 01, 02 skillek tesztelve és sablon-konformra hozva — **kész**
- 🔲 B-09: `_ieee_renderer` — ismeretlen évnél `é.n..` dupla pont (kozmetikai); a fallback paper-formátum trailing pontját rendezni
- 🔲 B-10: `05_figure_mapper.py` **inkompatibilis a v4 katalógussal** — a beágyazott `_meta`+`sources` sémát laposként olvassa (`catalog.values()`), nem talál `keywords`-öt, és valójában nem szúr be képet (csak `inserted_after_paragraph`-ot ír). Átírandó: v4 séma bejárása + `<!-- FIGURE: source/fig_id -->` placeholder-feloldás `![]()`-re a jegyzetben. (atg/1_het: a placeholder-feloldást most Claude végezte kézzel a skill §3.3 szerint.)
- ✅ B-11: `07-1_typesetter.py` Rule H **adatromlást okozott** (en-dash tartomány `1–35`→`1, 35`, `---` HR → `, -`, GFM tábla-szeparátor → `|:, , -|`, kanonikus `💡 Összegzés —` → `Összegzés,`). **Javítva:** Rule H mostantól csak ASCII `--`-t kezel; `–`/`—`, HR-sorok és tábla-sorok (`|`) érintetlenek. — **kész**
- ✅ B-12: `08_quality_check.py` citáció-metrika drift — **javítva** (2026-06-07): a számláló `\[\d+\]`-re bővítve, a kanonikus `[N]` (Instructions §8) ÉS a régi `<sup>[N]</sup>` jelölést is lefedi (a `\[\d+\]` a `<sup>…</sup>`-on belüli `[N]`-t is megtalálja). Kulcs `sup_citations`→`citations`. atg/1_het: a false negatív „0" helyett valós 102 citáció. — **kész**
- 🔲 B-13: **12/13 regiszter-mechanika** — a videó- és notebook-csatolmányok külön, bővíthető regiszterének (táblázatos fájl) megtervezése: fájlnév-konvenció, csatolmány stabil hivatkozása a jegyzetben/preziben, lista bővülés/szűkülés kezelése. (A didaktikai metaprompt már kész — B-05/B-06.)
- ✅ B-15: **MARP Mermaid-renderelés** — megoldva: `scripts/10-1_mermaid_render.py` a `_prezi_assets/*.mmd`-t PNG-vé alakítja (mermaid-cli `cli.js` + `chrome-headless-shell`, puppeteer-config forward-slash `executablePath` + `--no-sandbox`). Szakaszonkénti algráf-bontás (`navigator.mmd` + `secK.mmd`). Tesztelve: `atg/1_het` → 7/7 PNG. Egyszeri env-setup: `npx puppeteer browsers install chrome-headless-shell` + `PUPPETEER_SKIP_DOWNLOAD=true npm i @mermaid-js/mermaid-cli` (a `test_outputs/_tools/`-ba). **Hátravan (opc.):** a `10_pptx_gyarto.py`-ba auto-hívás + a markdown ```` ```mermaid ```` blokkjainak közvetlen kinyerése (most a `.mmd`-t kézzel írjuk). Skill: [10_presentation_maker §3.1a](skills/10_presentation_maker.md).
- ✅ B-16: **Hiányzó 😎-revíziós csatorna a 08-checkpointon** — a `N_Review.md`-nek nem volt dedikált bemeneti helye a szakértői (metrikán túli) tartalmi revíziós kéréshez. **Megoldva** (2026-06-07, generalizáltan): 08 §3.5 + Review `## 6` ragadós csatorna (😎-tulajdonú, meglévő/új forrás routing); 04 §3.10 + 01 §3.8 re-entry-szabály (stabil hivatkozás-kulcsok, csak az érintett szekció módosítása); pipeline.md §3 checkpoint-routing. A `quality_review_test` branch validálja. — **kész**
- ✅ B-17: **Ábra/táblázatfelirat-kaszkád** — beszúráskor a kézi feliratszámozás elcsúszik. **Megoldva** (2026-06-07): új `scripts/07-3_figure_numberer.py` (determinista, idempotens, külön ábra/tábla-sorozat, előfordulási sorrend). Feltétel: nincs szövegközi ábrahivatkozás (lásd [04 §8] megfigyelés). 07 skill §3.3 + pipeline §2. — **kész**
- ✅ B-18: **CRLF sortörés-duplázódás md-író scriptekben** — a `07-3` `read_bytes().decode()` + `splitlines(keepends=True)` + `write_text` kombinációja `\r\r\n`-t gyártott, amit egy univerzális-newline olvasás `\n\n`-re tágított → a jegyzet üres sorai megduplázódtak (616→1232). **Megoldva** (2026-06-07): olvasás-normalizálás LF-re (mint `07-1`); a sérült fájl helyreállítva a newline-futamok felezésével. **Generalizált szabály** (07 §8): minden md-író script normalizáljon LF-re olvasáskor. — **kész**
- ✅ B-19: **Forrásgyűjtési elvek (01)** — (1) több jelölt + 😎-egyeztetés (ne az első/sovány forrást ragadd meg); (2) 😎 saját fájlt is betehet a `1_raw_inputs/`-ba (retroaktív kezelés); (3) **weblap→PDF képekkel**: a *general* megoldás a **headless Chromium `--print-to-pdf`** (csak böngésző-bináris kell — Edge/Chrome/chrome-headless-shell; nincs Python-csomag, nincs site-API). A Wikipedia REST endpoint és a sovány szöveg-PDF **nem** általános — kizárva. Edge headless-szel bizonyítva (10 oldal, 9 kép). 01 §3.3–3.4. — **kész**
- ✅ B-20: **BSc/MSc szintszétválasztás** — **Megoldva** (2026-06-12, P2.1): a BSc/MSc szintfogalom teljesen kivezetésre került; a tananyag szint-semleges, nincs `[MSc]` tagelés, nincs BSc-szűrés; `11_bsc_export` → `11_docx_export` (egyetlen output). — **kész**
- 🔲 B-14: **`#`/`##` elnevezési csúszás** — a `06_summarize_box_injector` `#`-et nevez „fejezetnek", a `04` viszont `##`-et; a `🗺️` per-`#` (egy db) vs `💡`/`❓` per-`##`. A tényleges struktúrában `#` = dokumentumcím, `##` = fejezet. Tisztázni a terminológiát a 04/06/Instructions §7 között (kozmetikai, de zavaró). Opcionális.

## Ötletek — jövőbeni megfontolásra (💡)

- 💡 **Natív egyenletek (OMML / Cambria Math) a teljes kimeneti rétegben — közös `_omml.py`.**
  A 10-es lépésben bevált a LaTeX→MathML→**OMML** lánc ([`_omml.py`](../scripts/_omml.py)):
  `$...$` szövegközi, `$$...$$` block, **szerkeszthető** natív egyenletként (nem kép). Ez **kihat
  a camera-ready DOCX-re (11_docx_export) is**:
  - A WordprocessingML a `m:oMath`-ot **közvetlenül** a bekezdésbe ágyazza (egyszerűbb, mint a
    DrawingML `a14:m` wrapper a PPTX-ben) — a `_omml.py` `tex_to_omath()` változatlanul használható.
  - A **pandoc** (11-2) a `$...$`/`$$...$$`-t alapból **natív Word-egyenletté** (OMML) konvertálja,
    így a DOCX-ben is Cambria Math, szerkeszthető — nem PNG. Ezt a 11 skillben rögzíteni, és a
    pandoc-hívásnál ellenőrizni (`--mathml`/alapért. OMML).
  - **Egy forrás-konvenció** (`$...$` / `$$...$$` a jegyzetben) → három kimenet (PPTX natív OMML,
    DOCX natív OMML, MARP-preview), egységes matematikai megjelenítés. Gyökér-elv: a képletek
    SOHA nem képek, hanem natív, szerkeszthető egyenletek.

- 💡 **Mindmap mint retrieval-index — háttér-RAG (2. sprint, `mindmap_rag` branch):** a MinerU-ból
  már sok strukturált többletinformációt nyerünk (`text_context`, `caption`, `keywords`, oldalszám,
  Fig/Eq-azonosítók a `figure_catalog.json`-ban). Ötlet két lépcsőben:
  1. **Láthatatlan metaadat a mindmapben:** a 03 mindmap minden node-jához egy strukturált, *nem
     renderelt* blokk (a jelenlegi `<!-- ÁBRAHIVATKOZÁSOK -->` gépileg lekérdezhető kiterjesztése —
     pl. node-id → {forrás, oldal, chunk-id, Fig/Eq, keywords}). A renderelt mindmap tiszta marad,
     a node-ok mégis horgonyt kapnak a forrásrészletekhez.
  2. **Háttér-RAG index:** ebből a node→forrás-chunk leképezésből egy lekérdezhető index épül.
     Haszon: a `04_content_synthesizer` és a `09_question_bank` célzottan a releváns forrás-chunkra
     hivatkozhat a teljes PDF újraolvasása helyett — gyorsabb, olcsóbb, pontosabb citálás.
  - **Gyökér-elv:** a mindmap nemcsak vizuális vázlat, hanem a forrásokhoz vezető retrieval-index is.
  - Kapcsolódó skill-hely: [03_mindmap_builder §3.3.1 + §8](skills/03_mindmap_builder.md).

- 💡 **Automatikus fejezethatár-detektálás kettős tördelésű PDF-eknél — TOC-alapú megközelítés:** a tartalomjegyzék oldalait OCR-ezve közvetlenül megkapjuk a fejezet → könyvoldal-szám leképezést. Ebből a PDF-oldal index és az oldalpáritás (páros/páratlan könyvoldal = bal/jobb fél) pontosan kiszámítható — anélkül, hogy minden oldalt végig kellene szkennelni. Csak 1-2 TOC oldalt kell feldolgozni. Ez a gyökér-megközelítés: a könyv saját struktúráját használjuk a struktúra feltárásához.


- 💡 **Range-alapú shared sources:** ha egy forrás több egymást követő hétre vonatkozik, de nem az összesre, a tárgy mappán belül egy tartomány-névvel ellátott shared mappa lehetne megoldás. Pl.:
  ```
  3-6_shared_sources/   ← 3.–6. hét közös forrása
  8-12_shared_sources/  ← 8.–12. hét közös forrása
  ```
  Így az 1 fájl → sok hét (minden hétre) és az 1 fájl → néhány hét (range) eset is lefedett, anélkül hogy a fájlt n-szer kellene másolni. A script keresési sorrendje: `1_raw_inputs/` → `../0_shared_sources/` → `../<tól>-<ig>_shared_sources/` (ahol a hét száma a tartományba esik).

- 🔲 **B-24 [PRIORITÁS]**: **BSc/MSc szintelkülönítés a kérdésbankban** — BSc-exportban csak BSc kérdések, MSc-exportban BSc+MSc kérdések szerepelnek. Strukturális döntés: (1) explicit szintjelzés a `.md`-ben (a jelenlegi `<!-- MSc -->` blokk kiterjesztése: minden kérdésnek legyen `<!-- BSc -->` / `<!-- MSc -->` jelölője); (2) a `09_moodle_export.py` `--level bsc|msc` paramétere szűr; (3) a `subject_status.md §5`-be tantárgyankénti BSc/MSc konfig. Kapcsolódó: `09_question_bank` skill és a tervezett `09_moodle_export.py`.
- ✅ **B-21**: **09 skill + 09b_moodle_export spec** — kész (2026-06-07): 09_question_bank v1.3 (Jegyzet-first, L1 min. 10, mélységrendszer (2)–(5), BSc/MSc tag, fejezethivatkozás kötelező, „mindegyik/egyik sem" engedélyezett); 09b_moodle_export v1.0 (markdown→XML spec, heti+aggregált, --level, --no-explanation, --math-format). ❔ Nyitott: Moodle képlet-renderelés (Q1 a 09b §8-ban).
- ❔ B-25: **„Sok kép / sok szöveg" dia-redesign — strukturális tervezési elv.** A 10-es prezi-diák hagyományosan zsúfoltak (sok kép + sok szöveg egy dián). Elv a továbbiakra: **egy gondolat / dia** (Mayer-féle coherence + segmenting), a content-igényes részek (k/n) többrészes diákra bontva (lásd 10 skill §3.1c-bis). Folyamatos finomítás, nem egyszeri javítás.
- 🔲 **B-22**: **Moodle képlet-renderelés tisztázása** — melyik math-motort konfigurálja az intézményi Moodle (MathJax / TeX-filter / MathML)? Addig a képletes kérdések XML-exportja kockázatos. Megoldás: `--math-format` paraméter a `09-1_moodle_export.py`-ban (`latex` default, `mathjax`, `tex-filter`, `strip`). Prioritás: export-script megírása előtt tisztázni. — a skill és a Moodle-export script teljeskörű specifikációja a fenti döntések alapján: (1) L1 áganként min. 10 MCQ (volt: 3); (2) „mindegyik helyes" / „egyik sem helyes" engedélyezett; (3) mélységrendszer `(2)`–`(5)` taggel minden kérdésen; (4) magyarázat + `[N]` hivatkozás a megfelelő fejezetszakaszra (review miatt); (5) számítási feladatok az MCQ részei; (6) `09-1_moodle_export.py` markdown-first konverzió, `--no-explanation` kapcsolóval, heti és aggregált módban.

- 🔲 B-23: **Új DUE template-ek** — a jelenlegi `due_jegyzet_template.docx` és `due_presentation_template.pptx` ideiglenes placeholderek. Amikor az intézményi arculati template-ek elkészülnek, cseréld le:
  - `templates/due_jegyzet_template.docx` — Jegyzet DOCX (11_docx_export használja)
  - `templates/due_presentation_template_default.potx` — Prezentáció default variáns (10_presentation_maker)
  - `templates/due_presentation_template_mindmap.potx` — Prezentáció mindmap variáns (10_presentation_maker)
  Az új template-ek bevezetésekor a `10_pptx_gyarto.py --variant` és `11-2_pandoc_export.py` `find_template()` keresési logikáját is frissíteni kell.

## Nyitott kérdések (❔)

- ❔ Q-01: DUE template DOCX portolása — `templates/` mappába szükséges-e?
- ❔ Q-02: A `subject_status.md` (sablon: `subject_status_template.md`) mikor és ki által töltődik ki — különösen a §5 kérdésbank-beállítás a `09_question_bank` skill véglegesítése után? (😎 induláskor vagy 🤖 a 09 konfigjából?)
- ❔ Q-03 (B-07-hez): A `.claude/skills/` lépés-dokumentumok maradjanak protokoll-doksik, vagy váljanak valódi, hívható Claude-skillekké (`SKILL.md` + `name`/`description`)? — Mindent a maga idejében; a B-07/B-08 keretében döntjük el.
- ❔ Q-04 (B-05/B-06/B-13-hoz): A 12_youtube_finder (`📎▶`) és 13_jupyter_catalogizer (`📎🧪`) a kimeneti fázisban, **a jegyzet/prezi elkészülte UTÁN** futnak — hogyan lehet a csatolmányokat **visszamenőlegesen** beregisztrálni a már kész wip ÉS clean outputokba? Megválaszolandó: (1) a wip `4_wip_outputs/N_Jegyzet.md` / `N_Prezentacio.md` újraírása-e a horgony beszúrásához, vagy külön overlay/regiszter-fájl; (2) a már legenerált clean outputok (`5_clean_outputs/` .docx/.pptx) frissítése — újragenerálás a wip-ből vagy utólagos patch; (3) idempotencia és a bővülő/szűkülő videó-/notebook-lista kezelése a stabil `[link]` hivatkozással. Kapcsolódó kötött jelölés: `📎▶` / `📎🧪` (12/13 §3.1).
  - **Konkrét tünet (2026-06-08, atg/1_het):** a YouTube visszaregisztráció csak `4_wip_outputs/1_Jegyzet.md`-be történt meg. Hiányzik még (feladat):
    - `4_wip_outputs/1_Prezentacio_default.md`
    - `4_wip_outputs/1_Prezentacio_mindmap.md`
    - `6_clean_outputs/1_Jegyzet.docx` *(utólagos python-docx patch — részleges kísérlet volt, ellenőrizni)*
    - `6_clean_outputs/1_Prezentacio.pptx`
    - `6_clean_outputs/1_Prezentacio_mindmap.pptx`
  - **Notebook visszaregisztrálás (2026-06-08, atg/1_het):** a `📎🧪` csatolmány bekerült `4_wip_outputs/1_Jegyzet.md`-be (2. Kompresszortérkép összegzés után), de hiányzik (feladat — ugyanaz a lista mint YouTube-nál):
    - `4_wip_outputs/1_Prezentacio_default.md`
    - `4_wip_outputs/1_Prezentacio_mindmap.md`
    - `6_clean_outputs/1_Jegyzet.docx`
    - `6_clean_outputs/1_Prezentacio.pptx`, `1_Prezentacio_mindmap.pptx`
  - **6_assets mappa-konvenció (döntés, 2026-06-08):** notebookok (`📎🧪`) és regiszterek (YouTube + notebook lista) a `<hét>/6_assets/` mappában laknak — ez a 12/13 lépések kimeneti helye. YouTube regiszter is heti szintű, ugyanitt. A `6_assets/` a mappastruktúra új, 6. eleme (lásd Instructions §6).

## Változásjegyzék

| Dátum | Esemény |
|-------|---------|
| 2026-06-01 | Repo inicializálva; CLAUDE.md, Instructions.md, pipeline.md, 03+04 skill kész |
| 2026-06-01 | Scripts refactor: subn, modul regex, resolve_week centralizálva, 3_mindmap fix |
| 2026-06-01 | Meta-fájlok deduplikálva; "egy utasítás egy helyen" elv érvényesítve |
| 2026-06-01 | Script számozási séma: NN-M_name séma bevezetve, fájlok átnevezve |
| 2026-06-02 | E2E átfésülés indul: meta-réteg rendberakva (soft-cap, vertikális diagram, dedup) |
| 2026-06-02 | `00_init`: `context` → `subject_status.md`, NLM-mentes sablon, auto-kitöltött frontmatter + igazított státusz-tábla |
| 2026-06-02 | Citáció-rendszer: egyetlen `citations.json` (`type`-alapú), `[1]` jelölés, halott NLM-kód törölve `_citations_util`-ból, `_ieee_renderer` út+mező javítva és tesztelve |
| 2026-06-03 | `02_image_extraction`: átnevezés, vektoros detektálás, false positive fix, kettős tördelés kezelés, PDF-split, dft+atg tesztfutás lezárva |
| 2026-06-03 | `03_mindmap_builder`: skill spec v1.1 (input: `1_raw_inputs/` direkt PDF-olvasás, nem `2_clean_inputs/*.md`); mindmap draft: `atg/1_het/3_mindmap/mindmap.md` |
| 2026-06-03 | Pipeline átszámozás: 05 szétvált (05_figure_integrator + 06_summarize_box_injector), 06–10 → 07–11 (skillek + scriptek), 12_youtube_finder + 13_jupyter_catalogizer beillesztve a kimeneti fázisba; meta-dokumentumok frissítve |
| 2026-06-03 | `06_summarize_box_injector` v2.0: egyszintű `📦 Összegző` (per `##` fejezet) helyett kétszintű séma — `💡 Összegzés` minden `##` alfejezet végén, `🗺️ Fejezet összegfoglalása` minden `#` fejezet zárásánál; 04/08 skillek, Instructions §7, pipeline.md §4, `08_quality_check.py` count-minták és címkék frissítve |
| 2026-06-06 | **Didaktikai metapromptok** (branch `teaching_prompts`): 04 v1.3 (🔭 Epitome + 🧱 Előfeltételek + MSc worked example), 06 v2.1 (❓ Ellenőrizd magad + 🔑 Megoldókulcs retrieval), 10 v1.2 (szillogizmus + Bloom-igék + rugalmas Mayer-tömörség), 08 v1.3 (6. szempont: Biggs constructive alignment), 12/13 v1.1 (videó CTML-horgony, notebook POE — metaprompt előtöltve, regiszter backlog). Forrás: `Kutatási Útmutató Témák Feldolgozásához.md`. A/B teszt: `atg/1_het` (`_old` ↔ regenerált). |
| 2026-06-07 | **08_quality_reviewer futtatása `atg/1_het`-en**: B-12 javítva (citáció-számláló `\[\d+\]`; 0→102); skill v1.4 (§3.1 CLI doc-fix `--week-dir`); `1_Review.md` v1.3-konformra hozva (6. Biggs-szempont + frissített §1 metrikák; átlag 4,4→4,5). 🚦 08-checkpoint 😎 jóváhagyásra vár. |
| 2026-06-07 | **`quality_review_test` branch — revíziós-hurok teszt**: 😎 célzott revíziót kért a 08-checkpointon → B-16 megoldva (generalizált 😎-revíziós csatorna). Meta-rétegbe absztrahálva: 08 §3.5 (csatorna) + §3.3 (3. ág), 04 §3.10 + 01 §3.8 (re-entry, stabil kulcsok), pipeline.md §3 (forrás-routing). Instancia: `atg/1_het` Review §6 (R1 jelleggörbe=meglévő forrás, R2 áramlástechnikai gépek=új forrás). |
| 2026-06-07 | **Revízió végrehajtva + emergens tanulságok**: R1 (jelleggörbe, [2] Fig 1.10) és R2 (turbógép-család, **új [8]** Wikipedia *Turbomachinery*) integrálva a jegyzetbe; 08 újrafutott (113 citáció, 13 kép, nincs kritikus hiba). Generalizált: B-17 (07-3 felirat-számozó), B-18 (CRLF-gyökérhiba + szabály), B-19 (01 forrásgyűjtési elvek, weblap→PDF képekkel). |
