---
name: 09_question_bank
title: 09_QUESTION_BANK — Moodle-kompatibilis MCQ kérdésbank
type: skill
tags: [meta, skill]
role: 🤖
status: active
version: 1.3
updated: 2026-06-07
description: Mindmap L1 ágankénti bontásban MCQ kérdésbank generálása a végleges Jegyzet alapján. L1 áganként min. 10 kérdés, (2)–(5) mélységrendszer, BSc/MSc szintjelzéssel. Moodle-export: 09b_moodle_export.
---

# 09_QUESTION_BANK

## 1. Cél

A végleges Jegyzet és az approved mindmap alapján Moodle-kompatibilis MCQ kérdésbankot generál,
mindmap L1 ágankénti bontásban, (2)–(5) mélység-taggel és BSc/MSc szintjelzéssel.

**A kérdések forrása kizárólag a Jegyzet** (`N_Jegyzet.md`) — amit a hallgató megkap, azt kérdezzük. Ami nincs benne, nem kérdezhető.

**Input:** `4_wip_outputs/N_Jegyzet.md` + `3_mindmap/mindmap.md`
**Output:** `4_wip_outputs/N_Kerdesbank.md`
**Moodle XML:** → `09b_moodle_export` script

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 08_quality_reviewer | Publikálható minőségű Jegyzet — **ez az egyetlen forrásigazság** |
| `3_mindmap/mindmap.md` | 03_mindmap_builder | Approved mindmap — L1 ágak adják a szekció-bontást |

**Előfeltétel:** `08_quality_reviewer` döntése `PUBLIKÁLHATÓ`; mindmap `status: approved`.

### 2.1 Mélységrendszer

Minden kérdés pontosan egy `(2)`–`(5)` mélység-taggel rendelkezik:

| Tag | Osztályzat | Definíció |
|:----|:-----------|:----------|
| `(2)` | megfelelt | Megválaszolható kizárólag a `🗺️ Fejezet összefoglalása` blokkok alapján |
| `(3)` | közepes | Megválaszolható a `💡 Összegzés` + `🗺️` blokkok alapján |
| `(4)` | jól megfelelt | Megválaszolható a Jegyzet teljes főszövegének elolvasásával |
| `(5)` | kiválóan megfelelt | Csak mélyebb összefüggések, tervezési/elemzési kérdések — MSc-tipikus |

### 2.2 BSc/MSc szintjelzés

| Tag | Kinek tananyaga |
|:----|:----------------|
| `(BSc)` | BSc-jelölt és MSc-jelölt is tanulhatja |
| `(MSc)` | Csak MSc-jelölt tananyaga |

**Export-szabály:** BSc-export = csak `(BSc)` kérdések; MSc-export = `(BSc)` + `(MSc)` kérdések.

## 3. Eljárás

### 3.1 Kérdések generálása

Claude elolvassa a teljes Jegyzetet és a mindmapet, majd L1 ágankénti bontásban generál.

**Kötelező minimumok L1 áganként:**
- Legalább **10 MCQ kérdés** (BSc és MSc együtt)
- Legalább **2 `(2)` és 2 `(3)` szintű** kérdés — garantálni kell, hogy az összefoglalókra támaszkodó hallgató is tud válaszolni
- Legalább **1 számítási feladat** — ha a Jegyzetben van konkrét képlet/számérték; ha nincs, elméleti kérdéssel helyettesíthető

**Mélység-elosztás irányszám L1 áganként:**

| (2) | (3) | (4) | (5) |
|-----|-----|-----|-----|
| 2–3 | 2–3 | 3–4 | 1–2 |

**MSc kérdések:** jellemzően `(4)`–`(5)` mélységű; `<!-- MSc --> … <!-- /MSc -->` blokkban, az adott L1 szekció végén.

**Megengedett opciók:** „Mindegyik helyes" és „Egyik sem helyes" választható — ha a tartalom indokolja.

### 3.2 MCQ formátum

```markdown
## {L1 Ág neve}

**K{szám}.** `(BSc)` `(3)` {Kérdés szövege?}
→ *N_Jegyzet: §{fejezetszám} {fejezetcím}*

A) {Válasz A}
B) {Válasz B}
C) {Válasz C}
D) {Válasz D}

> *Helyes: {X} — {1-2 mondatos magyarázat, miért helyes és miért nem a többi}*

---

<!-- MSc -->
**K{szám}-MSc.** `(MSc)` `(5)` {Mélyebb kérdés?}
→ *N_Jegyzet: §{fejezetszám} {fejezetcím}*

A) ...
B) ...
C) ...
D) ...

> *Helyes: {X} — {magyarázat}*
<!-- /MSc -->
```

**Szabályok:**
- Pontosan **1 helyes válasz** per kérdés
- Zavaró válaszok tartalmilag közeliek, de egyértelműen tévesek
- Számítási feladatoknál konkrét számpélda a Jegyzetből, helyes számítás a magyarázatban
- Hivatkozás (`→ *N_Jegyzet: §...*`) kötelező — review-hoz és a magyarázat ellenőrzéséhez

### 3.3 Mentés

```
4_wip_outputs/N_Kerdesbank.md
```

YAML frontmatter:

```yaml
---
title: Kérdésbank — {tantárgy} {N}. hét
type: question_bank
subject: {tantárgy}
week: N
bsc_count: {szám}
msc_count: {szám}
depth_2_count: {szám}
depth_3_count: {szám}
depth_4_count: {szám}
depth_5_count: {szám}
created: YYYY-MM-DD
---
```

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Kerdesbank.md` | MCQ kérdésbank, L1 ágankénti bontás, BSc+MSc, (2)–(5) mélységcímkékkel |

Moodle XML-export: → [`09b_moodle_export.md`](09b_moodle_export.md)

## 5. Ellenőrzés

- [ ] Minden L1 ághoz legalább 10 MCQ kérdés
- [ ] Minden L1 ághoz legalább 2 db `(2)` és 2 db `(3)` szintű kérdés
- [ ] Minden kérdésen pontosan egy `(BSc)` / `(MSc)` tag
- [ ] Minden kérdésen pontosan egy `(2)`–`(5)` mélység-tag
- [ ] Minden kérdésnél `→ *N_Jegyzet: §...*` hivatkozás
- [ ] `<!-- MSc -->` blokkok zárottak (`<!-- /MSc -->`)
- [ ] Minden kérdésnél pontosan 1 helyes válasz jelölve
- [ ] Magyarázatok tartalmasak (nem csak „mert ez a helyes")
- [ ] Frontmatter count-mezők kitöltve

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| Kevesebb mint 10 kérdés L1 áganként | Mindmap kevés L1 ággal vagy vékony szekció | L2 csomópontokból is generálni, mélység-tageket bővíteni |
| `(5)` szintű BSc kérdés | Téves szint-megítélés | `(5)` csak MSc-tipikus kérdéseknél; BSc max `(4)` |
| Számítási feladat, de nincs képlet a Jegyzetben | MinerU-ból átemelt, de a szintézisbe nem kerülő tartalom | Számítási feladat helyett `(4)` elméleti kérdés |
| Hivatkozás hiányzik | Gyors generálás | Minden kérdésnél visszakeresni a megfelelő `##` fejezetet |
| `<!-- MSc -->` blokk nem zárt | `<!-- /MSc -->` hiányzik | Manuálisan hozzáadni |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [09b_moodle_export.md](09b_moodle_export.md) — Moodle XML-export spec
- [08_quality_reviewer.md](08_quality_reviewer.md) — upstream
- [03_mindmap_builder.md](03_mindmap_builder.md) — L1 ágak forrása

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (mint 08_question_bank) |
| 2026-06-03 | 1.1 | Átszámozva 08→09 |
| 2026-06-05 | 1.2 | MinerU-first: §2 MinerU `.md` mint számítási forrás; §3.1 számítási feladat kritérium pontosítva |
| 2026-06-07 | 1.3 | **Alapelv-váltás:** forrásigazság = Jegyzet (nem MinerU); L1 min. 10 MCQ (volt 3); mélységrendszer (2)–(5) minden kérdésen; BSc/MSc szintjelzés + export-szabály; „Mindegyik/Egyik sem helyes" engedélyezett; fejezethivatkozás kötelező review-hoz; Moodle-export → 09b_moodle_export |
