---
name: 00_init
title: 00_INIT — Tantárgy inicializálás és mappastruktúra
type: skill
tags: [meta, skill]
status: active
version: 1.1
updated: 2026-06-02
description: Új tantárgy pipeline-jának inicializálása — subject_status.md és heti mappastruktúra létrehozása.
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

A szint (BSc/MSc), célok, stílus **nem CLI-argumentum** — ezeket a generált
`subject_status.md`-ben tölti ki a felhasználó.

**Előfeltétel:** A `templates/subject_status_template.md` sablon létezik; a gyökér írható.

## 3. Eljárás

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
    5_clean_outputs/
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
| `<tantárgy>/{N}_het/5_clean_outputs/` | Üres — végleges outputoknak |

## 5. Ellenőrzés

- [ ] `subject_status.md` létrejött a tantárgy gyökerében
- [ ] Minden hétre (`1` … `N`) létrejött mind az **5** almappa
- [ ] `3_mindmap/` jelen van minden hétnél
- [ ] A script naplója `Kész: … létrehozva` sorral zárul, hiba nélkül

## 6. Hibakezelés

<!-- SZABÁLY: Minden felfedezett hibát ÉS megoldást ide kell dokumentálni azonnal. -->

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| `HIBA: nincs sablon: …` | Hiányzó `subject_status_template.md` | Ellenőrizd a `templates/` mappát |
| Semmi sem jön létre újra | Idempotencia — már inicializált | Normál; töröld manuálisan, ha újra kell |
| Rossz helyre kerül a tantárgy | `--root` alapértelmezés `test_outputs` | Éles tantárgyhoz add meg: `--root .` |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [01_source_collector.md](01_source_collector.md) — következő lépés
- [subject_status_template.md](../../templates/subject_status_template.md) — a másolt sablon

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva |
| 2026-06-02 | 1.1 | Skill a script valóságához igazítva: `context.json` → `subject_status.md`, helyes argumentumok, 5 almappa, idempotencia |
