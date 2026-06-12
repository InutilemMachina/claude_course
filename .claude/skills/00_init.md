---
name: 00_init
title: 00_INIT — Tantárgy inicializálás és mappastruktúra
type: skill
tags: [meta, skill]
role: 🐍
status: active
version: 1.3
updated: 2026-06-12
description: Új tantárgy mappastruktúrájának és subject_status.md-jének létrehozása; használd a pipeline legelején, amikor új tantárgyat (vagy annak heti bontását) indítasz.
---

# 00_INIT

## 1. Cél

Új tantárgy esetén létrehozza a tantárgy mappastruktúráját, és a sablonból bemásolja a
`subject_status.md` tervező/státusz lapot, hogy a downstream lépések egységes útvonalakon
dolgozzanak, Claude pedig session elején beolvashassa a tantárgy állapotát.

**Input:** Tantárgy mappanév, hetek száma (CLI argumentumok).
**Output:** `<tantárgy>/subject_status.md` + `<tantárgy>/{N}_het/` mappák (5 almappa).

## 2. Bemenetek

| Adat | Forrás | Tartalom |
|:-----|:-------|:---------|
| `--subject` | Felhasználó | tantárgy mappanév, pl. `Surge-Choke-Stall...` |
| `--weeks` | Felhasználó | hetek száma (egész, default `1`) |
| `--root` | Felhasználó | gyökér mappa (default `test_outputs`; éles tantárgyhoz `.`) |

A célok, stílus **nem CLI-argumentum** — ezeket a generált
`subject_status.md`-ben tölti ki a felhasználó.

**Előfeltétel:** A `templates/subject_status_template.md` sablon létezik; a gyökér írható.

## 3. Eljárás 🐍

### 3.1. Futtatás

```powershell
# Próbafuttatás (semmit nem ír ki)
python scripts/00_init_course.py --subject "Surge-Choke-Stall_Aramlastechnikai_berendezesekben" --weeks 1 --dry-run

# Éles futtatás (teszt: test_outputs alá)
python scripts/00_init_course.py --subject "Surge-Choke-Stall_Aramlastechnikai_berendezesekben" --weeks 1
```

A script **idempotens**: meglévő `subject_status.md`-t és mappákat nem ír felül, csak kihagy.

### 3.2. Mappastruktúra (hetenként)

```
<root>/<tantárgy>/
  subject_status.md
  {N}_het/
    1_raw_inputs/
    2_clean_inputs/
    3_mindmap/
    4_wip_outputs/
    5_asset_outputs/
    6_clean_outputs/
```

### 3.3. subject_status.md kitöltése

A futás után **töltsd ki** a `subject_status.md` §1 (alapadatok), §4 (célok),
§5 (stílusirányelvek) szekcióit, mielőtt a `01_source_collector`-ra lépsz.

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `<tantárgy>/subject_status.md` | Tantárgy-szintű terv + heti pipeline-státusz (sablonból) |
| `<tantárgy>/{N}_het/1_raw_inputs/` | Üres — forrásgyűjtésre vár (`01`) |
| `<tantárgy>/{N}_het/3_mindmap/` | Üres — `03_mindmap_builder`-nek |
| `<tantárgy>/{N}_het/5_asset_outputs/` | Üres — 12/13 gazdagítás (regiszter + overlay) |
| `<tantárgy>/{N}_het/6_clean_outputs/` | Üres — camera-ready végleges outputoknak |

## 5. Teszt

- **Fixture (bemenet):** nincs forrás-fixture (ez az első lépés); bemenet a CLI: `--subject smoke --weeks 2`.
- **Akció:** `python scripts/00_init_course.py --subject smoke --weeks 2`
- **Várt kimenet:** `test_outputs/smoke/subject_status.md` (frontmatter: `subject: smoke`, `weeks: 2`, `tags: [test]`) + `1_het/`…`2_het/` mind az 5 almappával; a script `Kész: 11 létrehozva` sorral zárul.
- **Eval:** `--dry-run` ugyanezt jelzi módosítás nélkül; idempotens újrafuttatás → `0 létrehozva, 11 kihagyva`; a §2 státusz-tábla 2 hét-oszloppal generálódik.

## 6. Ellenőrzés

- [ ] `subject_status.md` létrejött a tantárgy gyökerében
- [ ] Minden hétre (`1` … `N`) létrejött mind az **5** almappa
- [ ] `3_mindmap/` jelen van minden hétnél
- [ ] A script naplója `Kész: … létrehozva` sorral zárul, hiba nélkül

## 7. Hibakezelés

<!-- SZABÁLY: Minden felfedezett hibát ÉS megoldást ide kell dokumentálni azonnal. -->

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `HIBA: nincs sablon: …` | Hiányzó `subject_status_template.md` | Ellenőrizd a `templates/` mappát |
| Semmi sem jön létre újra | Idempotencia — már inicializált | Normál; töröld manuálisan, ha újra kell |
| Rossz helyre kerül a tantárgy | `--root` alapértelmezés `test_outputs` | Éles tantárgyhoz add meg: `--root .` |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- upstream: — (első lépés) · downstream: [01_source_collector.md](01_source_collector.md)
- [subject_status_template.md](../../templates/subject_status_template.md) — a másolt sablon

## 9. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva |
| 2026-06-02 | 1.1 | Skill a script valóságához igazítva: `context.json` → `subject_status.md`, helyes argumentumok, 5 almappa, idempotencia |
| 2026-06-03 | 1.2 | Sablonhoz igazítva: `role: 🐍`, triggerelő `description`, §5 Teszt (verifikált), upstream/downstream linkek; őszinte idempotencia-napló (a heti mappákat is számolja) |
| 2026-06-12 | 1.3 | Mappa-migráció (P2.2): 6 almappa — `5_clean_outputs` → `5_asset_outputs` (12/13) + `6_clean_outputs` (camera-ready); §3.2 mappafa + §4 kimenetek frissítve; `PIPELINE_STEPS` `11 bsc_export` → `11 docx_export`. |
