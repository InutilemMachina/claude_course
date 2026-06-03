---
name: 09_question_bank
title: 09_QUESTION_BANK — Moodle-kompatibilis MCQ kérdésbank
type: skill
tags: [meta, skill]
role: 🤖
status: active
version: 1.1
updated: 2026-06-03
description: Mindmap L1 ágankénti bontásban MCQ kérdésbank generálása BSc (20+ kérdés) és MSc szinteken.
---

# 09_QUESTION_BANK

## 1. Cél

A végleges jegyzet és az approved mindmap alapján Moodle-kompatibilis MCQ kérdésbankot generál,
mindmap L1 ágankénti bontásban, BSc és MSc szintű kérdésekkel.

**Input:** `4_wip_outputs/N_Jegyzet.md` + `3_mindmap/mindmap.md`
**Output:** `4_wip_outputs/N_Kerdesbank.md`

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 08_quality_reviewer | Publikálható minőségű jegyzet |
| `3_mindmap/mindmap.md` | 03_mindmap_builder | Approved mindmap, L1 ágak |

**Előfeltétel:** `08_quality_reviewer` döntése `PUBLIKÁLHATÓ`; mindmap `status: approved`.

## 3. Eljárás

### 3.1. Kérdések generálása

Claude elolvassa a teljes notes-t és mindmap-et, majd mindmap L1 ágankénti bontásban generál:

**BSc kérdések (kötelező minimumok):**
- Összesen legalább **20 elméleti MCQ** kérdés
- Legalább **5 számítási feladat** (számot, képletet igénylő)
- L1 áganként legalább 3 kérdés

**MSc kérdések:**
- `<!-- MSc -->` blokkban, az adott L1 szekció végén
- Mélyebb analízis, tervezési kérdések, határesetek

### 3.2. MCQ formátum

```markdown
## {L1 Ág neve}

**K{szám}.** {Kérdés szövege?}

A) {Válasz A}
B) {Válasz B}
C) {Válasz C}
D) {Válasz D}

> *Helyes: {X} — {1-2 mondatos magyarázat, miért helyes és miért nem a többi}*

---

<!-- MSc -->
**K{szám}-MSc.** {Mélyebb kérdés?}

A) ...
B) ...
C) ...
D) ...

> *Helyes: {X} — {magyarázat}*
<!-- /MSc -->
```

**Szabályok:**
- Pontosan **1 helyes válasz** per kérdés (`✓` jelölés a magyarázatban is)
- Zavaró válaszok tartalmilag közeliek, de egyértelműen tévesek
- Számítási feladatoknál konkrét számpélda, helyes számítás a magyarázatban
- Kerüld: `mindegyik helyes`, `egyik sem helyes` opciókat

### 3.3. Mentés

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
calculation_count: {szám}
created: YYYY-MM-DD
---
```

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Kerdesbank.md` | MCQ kérdésbank, L1 ágankénti bontásban, BSc+MSc |

## 5. Ellenőrzés

- [ ] Legalább 20 BSc MCQ kérdés
- [ ] Legalább 5 számítási feladat
- [ ] Minden L1 ághoz legalább 3 kérdés
- [ ] `<!-- MSc -->` blokkok zárottak (`<!-- /MSc -->`)
- [ ] Minden kérdésnél pontosan 1 helyes válasz jelölve
- [ ] Magyarázatok tartalmasak (nem csak „mert ez a helyes")

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| Kevesebb mint 20 kérdés | Mindmap kevés L1 ággal | Még 2-3 L2 csomópontból is generálni |
| Több helyes válasz egy kérdésnél | Nem egyértelmű zavaró opciók | Zavaró opciókat konkretizálni |
| MSc blokk nem zárt | `<!-- /MSc -->` hiányzik | Manuálisan hozzáadni |
| Számítási feladatnál hibás szám | Számítás-ellenőrzés kihagyva | Képleteket manuálisan ellenőrizni |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [08_quality_reviewer.md](08_quality_reviewer.md) — upstream
- [03_mindmap_builder.md](03_mindmap_builder.md) — L1 ágak forrása

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (mint 08_question_bank) |
| 2026-06-03 | 1.1 | Átszámozva 08→09 |
