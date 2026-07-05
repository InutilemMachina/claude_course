---
name: 08_quality_reviewer
title: 08_QUALITY_REVIEWER — Minőségellenőrzés és publikálhatóság
type: skill
tags: [meta, skill]
role: 😎+🤖
status: active
version: 1.9
updated: 2026-06-13
description: Script-alapú lint + Claude Explore review (6 szempont, köztük Biggs constructive alignment); publikálhatóság ≥3/5 esetén 09-13 indul, különben vissza 04-hez. A 🚦-checkpointon a 😎 célzott revíziót kérhet a Review §6 csatornán (meglévő/új forrás routing).
---

# 08_QUALITY_REVIEWER

## 1. Cél

Automatizált script és Claude review kombináció alapján meghatározza, hogy a WIP jegyzet
publikálható-e, vagy vissza kell küldeni a content synthesizer lépéshez.

**Input:** `4_wip_outputs/N_Jegyzet.md`
**Output:** `4_wip_outputs/N_Review.md` + publikálhatósági döntés

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 07_typesetter | Tipográfiailag normalizált jegyzet |
| `3_mindmap/mindmap.md` | 03_mindmap_builder | Approved mindmap (fedettség-ellenőrzéshez) |

**Előfeltétel:** `07_typesetter` lefutott; `mindmap.md` `status: approved`.

## 3. Eljárás

### 3.1. Automatizált quality check

```powershell
python scripts/08_quality_check.py --week-dir test_outputs/<tárgy>/N_het
# több-fejezetes heti anyagnál a ### szakasz-küszöb felülírható:
python scripts/08_quality_check.py --week-dir test_outputs/<tárgy>/N_het --chapters 6
```

> ℹ️ A `### szakaszok` gazdagság-küszöbe (ajánlott 5–12) **egy kompakt, egyfejezetes**
> dokumentumra van kalibrálva. Több-fejezetes heti anyagnál a magasabb szakaszszám
> természetes: a script a felső határt a **`##` fejezetek számával arányosan** tágítja
> (`max(12, fejezetek × 4)`). A `--chapters N` a várt fejezetszámot explicit felülírja
> (pl. hiányzó/rendhagyó `##` tagolásnál).

Ellenőrzési szempontok:
- Fejezet-fedettség: minden mindmap L1 ág jelen van-e?
- Minimum terjedelem: `##` fejezetek legalább 3 bekezdéssel?
- LaTeX hiány: egyetlen képlet sem jelenik meg egy képletintenzív témában?
- Hivatkozások: a `citations.json` bejegyzések `[1]`, `[2]` formában megjelennek-e?
- Összegző blokkok: minden `###` szakasz végén van-e `> 💡 Összegzés` blokk, és minden `##` fejezet zárásánál `> 🗺️ Fejezet összegfoglalása` blokk? (formátum: [06_summarize_box_injector](06_summarize_box_injector.md) §3.1–3.2)

### 3.2. Claude Explore review

Claude értékeli az alábbi 6 szempont szerint (1–5 skálán):

| Szempont | Leírás |
|:---------|:-------|
| **Teljesség** | Minden mindmap L1 ág lefedett? |
| **Mélység** | A magyarázat mélysége elegendő a célcsoportnak? Képletek, példák jelen? |
| **Koherencia** | Fejezetek logikusan következnek egymásból? |
| **Forrásintegráció** | Hivatkozások beépítve, nem csak felsorolva? |
| **Olvashatóság** | Tipográfia, tagolás, összegzők rendben? |
| **Konstruktív illeszkedés** (Biggs) | Cél ⇄ tevékenység ⇄ értékelés egy vonalban? |

A **Konstruktív illeszkedés** mérhető al-kérdései:
- Van-e minden `##` fejezethez azonosítható, Bloom-szintű tanulási cél (a `🎯 Cél` blokk, 04 §3.2)?
- A `❔ Ellenőrizd magad` kérdések és a 09 kérdésbank lefedik-e a fejezet céljait?

Eredmény: **átlag pontszám** (1–5) a **6 szempontból**, szöveges indoklással.

### 3.3. Döntési logika

```
Átlag (6 szempont) ≥ 3.0 → Publikálható → 09_question_bank + 10_presentation_maker + 11_docx_export
                                            (+ 12_youtube_finder, 13_jupyter_catalogizer opcionális) indul
Átlag (6 szempont) < 3.0 → Visszaküldés → 04_content_synthesizer kap revision note-ot
PUBLIKÁLHATÓ, DE 😎 a checkpointon célzott revíziót kér → §3.5 csatorna → 04 (vagy 01) → 07 → 08 újra
```

A harmadik ág a gyakori, életszerű eset: a metrikák és az átlag rendben (≥ 3.0), a jegyzet
elvileg publikálható, **de** a szakértő 😎 a 🚦-checkpointon tartalmi hiányt jelez. Ez **nem**
„visszaküldés < 3.0 miatt", hanem **célzott, 😎-vezérelt revízió** — a kezelése a §3.5 csatornán
történik, nem a globális revision note-tal.

### 3.4. Review mentése

```
4_wip_outputs/N_Review.md
```

Tartalom: script kimenet + Claude értékelés + döntés + revision note (ha <3.0).

### 3.5. Felhasználói revíziós csatorna (😎 checkpoint)

A `08_quality_check.py` és a Claude-review a **belső** minőséget méri, de a 🚦-checkpointon a
szakértő 😎 olyan tartalmi hiányt jelezhet, amit egyetlen automatikus metrika sem fog meg
(pl. „hiányos egy fogalom kifejtése", „hiányzik egy géptípus"). Ennek **dedikált bemeneti helye**
a `N_Review.md` `## 6. Felhasználói revíziós kérések (😎)` szekciója:

```markdown
## 6. Felhasználói revíziós kérések (😎 checkpoint)

| # | 😎 kérés | Forrás-stratégia | 🤖 revision note → cél-lépés | Státusz |
|---|----------|------------------|------------------------------|---------|
| R1 | „<a 😎 szó szerinti kérése>" | meglévő | <konkrét, végrehajtható utasítás> → 04 | ⚙️ / ✅ |
| R2 | „<…>" | új forrás | <…> → 01 → 02 → 04 | ⚙️ / ✅ |
```

- **A szekció 😎-tulajdonú és „ragadós":** a 08 újrafuttatásakor a 🤖 **nem törli** — csak a
  `Státusz` oszlopot frissíti (⚙️ → ✅), és új sort csak 😎-kérésre vesz fel.
- **Forrás-stratégia routing:**
  - `meglévő` → a kérés a [`04_content_synthesizer`](04_content_synthesizer.md)-be megy közvetlenül
    (a `2_clean_inputs/` már feldolgozott forrásaiból bővítünk).
  - `új forrás` → előbb [`01_source_collector`](01_source_collector.md) (új forrás + `citations.json`),
    majd [`02_mineru_to_catalog`](02_image_extraction.md) (kinyerés), végül `04`.
- **A 🤖 minden 😎-kérést** önálló, ellenőrizhető revision note-tá fordít (mit, hol, melyik
  forrásból, milyen vizuállal), és a revízió végrehajtása után a `Státuszt` ✅-re állítja.
- A célzott revízió után a lánc **07 → 08** újrafut; a `## 1–5` szekciók frissülnek, a `## 6`
  megmarad a nyomvonal kedvéért.

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Review.md` | Részletes minőségi értékelés, döntéssel |

## 5. Teszt

- **Fixture:** `test_outputs/atg/1_het` — `1_Jegyzet.md` + approved `mindmap.md`.
- **Akció:** `08_quality_check.py --week-dir …` + Claude review (6 szempont, 1–5).
- **Várt kimenet:** `1_Review.md` (szempontonkénti pontszám, átlag, döntés ≥3.0).
- **Eval:** Numerikus pontszám minden szempontnál + 🚦 😎 checkpoint.

## 6. Ellenőrzés

- [ ] `N_Review.md` tartalmaz numerikus pontszámot minden szempontnál
- [ ] Döntés egyértelmű: `PUBLIKÁLHATÓ` vagy `VISSZAKÜLDÉS`
- [ ] Ha visszaküldés: konkrét revision note-ok a 04-es lépés számára
- [ ] Script kimenet csatolva a review-hoz

## 7. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| Script `KeyError` a mindmap-nél | Mindmap nem `status: approved` | 03-at lezárni, approved státuszt beállítani |
| Claude pontozás szélsőséges (1-es vagy 5-ös) | Nincs elegendő kontextus | Mindmap és forrásokat is betölteni a reviewhoz |
| `N_Review.md` nem keletkezik | Script crash | Naplót ellenőrizni; manuális review is elfogadható |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- [07_typesetter.md](07_typesetter.md) — upstream
- [04_content_synthesizer.md](04_content_synthesizer.md) — visszaküldési cél
- [09_question_bank.md](09_question_bank.md) — downstream (ha publikálható)

## 9. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->
- ✅ B-12 JAVÍTVA (2026-06-07): a `08_quality_check.py` citáció-számlálója `\[\d+\]`-re bővítve — a kanonikus `[N]` (Instructions §8) ÉS a régi `<sup>[N]</sup>` jelölést is lefedi. (atg/1_het: a korábbi „0 citáció" false negatív helyett valós 102.)

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-07 | 1.5 | §3.3 harmadik döntési ág (PUBLIKÁLHATÓ + 😎 célzott revízió); új §3.5 **felhasználói revíziós csatorna** — a `N_Review.md` `## 6` szekciója a 😎-kérések dedikált, ragadós bemeneti helye, meglévő/új forrás routinggal (04, ill. 01→02→04). A `quality_review_test` branch teszteli. |
| 2026-06-07 | 1.4 | §3.1 CLI-parancs javítva a tényleges scriptre (`--week-dir <path>`, korábban hibás `--week N --subject`); B-12 lezárva (citáció-számláló `\[\d+\]`-re bővítve). |
| 2026-06-06 | 1.3 | **Constructive alignment**: §3.2 új 6. értékelési szempont (Biggs — cél ⇄ tevékenység ⇄ értékelés) mérhető al-kérdésekkel; §3.3 átlag 6 szempontra (küszöb ≥ 3.0 marad). |
| 2026-06-01 | 1.0 | Létrehozva (mint 07_quality_reviewer) |
| 2026-06-03 | 1.1 | Átszámozva 07→08; downstream 09–13, script 08_quality_check.py |
| 2026-06-03 | 1.2 | §3.1 összegző-doboz check átírva a kétszintű sémára (`💡 Összegzés` per `##`, `🗺️ Fejezet összegfoglalása` per `#`) |
| 2026-06-11 | 1.6 | §Teszt pótolva (atg/1_het); §5→§10 átszámozva; §3.2 „5→6 szempont” javítva; role 😎+🤖. |
| 2026-06-11 | 1.7 | MSc-kivezetés: §3.2 Mélység-szempont szint-semlegesre; a BSc/MSc Bloom-alkérdés törölve. |
| 2026-06-12 | 1.8 | Heading-hierarchia (P2.13, B-14): §3.1 összegző-check `💡` per `###` szakasz, `🗺️` per `##` fejezet; a `08_quality_check.py` metrika-címkék (Fejezetek/Szakaszok) + az „5-12" gazdagság-küszöb a `###` szakaszokra igazítva. || 2026-06-13 | 1.9 | `dft_test`: a `### szakaszok` küszöb a `##` fejezetszámmal **arányosan** skálázódik (`max(12, fejezetek×4)`), + `--chapters N` flag a felülíráshoz — megszűnteti a több-fejezetes heti anyag hamis „17 > 12" figyelmeztetését. |