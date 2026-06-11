---
title: Instructions
type: project_constitution
tags: [meta]
version: 1.2
updated: 2026-06-03
description: Projekt-szintű elvek, jelölések és dokumentációs szabványok.
---

# Instructions

## 1. Cél

Claude-natív tananyagfejlesztési pipeline. Nincs NLM-függőség.
A pipeline az oktató tradicionális munkafolyamatát modellezi Claude segítségével.

## 2. Alapelvek

- Az egyszerűbb megoldás előnyösebb.
- A lapos struktúra érthetőbb, nem szeretjük az ágas-bogas folyamatokat.
- Egy fájl = egy cél.
- Minden információ csak egyetlen kanonikus helyen szerepel.
- A dokumentáció legyen rövid, világos, szabványos.
- A pipeline legyen lehetőleg automatizált, determinisztikus és minimalista.
- A részletek ne ismétlődjenek különböző fájlokban.
- A problémát a gyökérokánál kell kijavítani — tüneti kezelés helyett az ok megszüntetése.
- Adatokon alapuló döntéshozatal az alternatívák megválaszolásában.

## 3. Dokumentációs hierarchia

A lista egyben **tekintély-sorrend**: ütközés esetén a feljebb álló dokumentum írja felül az alatta lévőt. A „mi mire való" funkcionális index: [CLAUDE.md §4](CLAUDE.md).

1. [CLAUDE.md](CLAUDE.md)
2. [Instructions.md](Instructions.md)
3. [.claude/pipeline.md](.claude/pipeline.md)
4. [.claude/project_status.md](.claude/project_status.md)
5. [.claude/skills/](.claude/skills/)
6. [scripts/](scripts/)

## 4. Jelöléstan

### 4.1. Emoji státuszok
- 🔲: TODO
- ✅: KÉSZ / OK
- ⚙️: FÉLKÉSZ / WIP
- ❌: NOK / HIÁNYZIK
- ❔: KÉRDÉS / NYITOTT
- ⚠️: VIGYÁZAT / FONTOS
- 🚦: CHECKPOINT:
    - 🔴: ÁLLJ / STOP
    - 🟡: FELTÉTELESEN TOVÁBB ENGEDVE (feltétel dokumentálásával)
    - 🟢: MEHET
- ⚡: HIBA / inkonzisztencia
- 💬: NOTE
- 💡: IDEA

Ezeket az emoji státuszokat mindig a szöveggel is ki kell egészíteni, pl.: `💡 IDEA: Az ötlet`
Te használhatod őket, de a user szinte soha nem illeszti be azokat, pl.:  `IDEA: Az ötlet`

### 4.2. Szerepkörök

| Jelölés | Szerep | Használat |
|---|---|---|
| 😎 | Felhasználó | Manuális döntés, jóváhagyás, checkpoint |
| 🤖 | Claude | Pipeline-lépések, dokumentumfrissítés |
| 🐍 | Python script | Konverzió, audit, tömeges feldolgozás |
| 💻 | Terminál / shell | Fájlműveletek, script futtatás |

## 5. Nevezéktan

### 5.1. Fájlnév konvenció

- Meta-, skill- és script-fájlok neve: angol.
- Meta- és skillfájlok tartalma: magyar (esetleges angol kifejezésekkel).
- Szóköz tilos. Alulvonás használható.
- Pipeline lépések sorszámozása stabil maradjon
- Scriptek sorszámozása kövesse a Pipeline lépések számát. Allépések esetén dash.

**Script számozási séma** (`scripts/` mappa):

| Típus | Séma | Példa |
|-------|------|-------|
| Egy script egy lépéshez | `NN_name.py` | `05_figure_mapper.py` |
| Több script egy lépéshez | `NN-M_name.py` | `02-1_mineru_pipeline.py` |
| Megosztott segédkönyvtár | `_name.py` | `_citations_util.py` |

- `NN`: pipeline lépés sorszáma (00–13), párhuzamos a skill-számokkal
- `M`: lépésen belüli sorrend (1, 2, ...)
- `_` prefix: nem lépés-specifikus utility — nincs hozzá külön skill

### 5.2. YAML fejléc — `tags` séma

| Scope-tag | Jelentés | Hol |
|---|---|---|
| `meta` | Projekt-infrastruktúra | `.claude/`, gyökér |
| `skill` | Pipeline-lépés protokollja | `.claude/skills/` |
| `test` | Teszt-tananyag | `test_outputs/` |
| `prod` | Éles tantárgyi tananyag | tantárgy-mappa |

## 6. Mappastruktúra

```text
claude_course/
├── CLAUDE.md
├── Instructions.md
├── .claude/
│   ├── pipeline.md
│   ├── project_status.md
│   ├── skill_template.md
│   └── skills/
│       └── NN_skill.md
├── scripts/
├── templates/
│   └── assets/
└── {tantargy}/
    └── {N_het}/
        ├── 1_raw_inputs/
        ├── 2_clean_inputs/
        ├── 3_mindmap/
        ├── 4_wip_outputs/
        └── 5_clean_outputs/
        └── 6_asset_outputs/
```

## 7. Vizuális gazdagítás — kötelező szabály

Minden tananyag-output "képnehéz": vizuálisan erősen támogatott.

| Réteg | Szabály |
|-------|---------|
| Navigátor mindmap | Minden output tetején link; MARP 2. diája |
| Szekciós diagram | Minden mindmap-csomóponthoz, ha ≥3 fogalom összefügg |
| Valódi ábra | MinerU-kinyert PNG; különben `<!-- FIGURE: ... -->` placeholder |
| MARP vizuális | Minden dián 1 Mermaid VAGY ábra — kötelező |

Diagram-típus döntési fa:
- Jegyzetek és álló lapformátum esetén → `flowchart TD`
- Slide-ok és fekvő lapformátum esetén → `flowchart LR`
- Időbeli lefolyás → `sequenceDiagram`
- Összehasonlítás → Markdown table
- Összegzés (`##` alfejezet végén) → `> 💡 **Összegzés — …**` blockquote (kulcsgondolat + kulcsfogalmak + képletek)
- Fejezet-szintű összefoglalás (`#` fejezet zárásánál) → `> 🗺️ **Fejezet összegfoglalása — …**` blockquote (fő üzenet + mit tudsz most + kulcsképletek + kapcsolódás)
  [ ] TODO: Saját technikai adósság: sehol nincs rögzítve, hogy mi a Fejezet, Szakasz, Alszakasz és Al-Alaszakasz, illetve, hogy ezek markdown-ban hányadrendű `#`-vel rendelkeznek. Javaslatom:alább
  ```markdown
  # **Cím Camelcase Vastag**
  ## 1. Fejezet
  ### 1.1. Szakasz
  #### 1.1.1. Alszakasz
  ##### 1.1.1.1. Al-Alszakasz
  ```
  ebben az esetben pedig: 
  - Összegzés minden másodrendű szakasz (`###`) után → `> 💡 **Szakasz összegzése — …**` blockquote (kulcsgondolat + kulcsfogalmak + képletek)
  - Fejezet-szintű összefoglalás (`##`) után → `> 🗺️ **Fejezet összegfoglalása — …**` blockquote
  TODO vége
A két blokk kanonikus formátuma: [.claude/skills/06_summarize_box_injector.md](.claude/skills/06_summarize_box_injector.md) §3.1–3.2.

### 7.1. Ábra- és táblázatfelirat-konvenció

Minden ábra és táblázat **számozott, önálló koherens feliratot** kap. „Önálló koherens" =
a kép/tábla a feliratával együtt a szövegből kiemelve is megérthető (a felirat nem csak címke,
hanem rövid, magyarázó mondat).

| Elem | Felirat helye | Séma |
|------|---------------|------|
| Ábra (kép) | a kép **alatt** | `i. ábra. Feliratszöveg. [forrás / saját szerk.]` |
| Saját ábra: Mermaid-diagram, flowchart | a diagram **alatt** | `i. ábra. Feliratszöveg. [saját szerk.]` |
| Táblázat | a tábla **fölött** | `i. táblázat. Feliratszöveg. [forrás / saját szerk.]` |

- **Számozás:** dokumentumon belül folytonos, az ábrák és a táblázatok **külön** sorozata
  (`1. ábra`, `2. ábra`, … és `1. táblázat`, `2. táblázat`, …), előfordulási sorrendben.
- **A beszúrt Mermaid-diagramokat / flowchartokat is számozni kell** — ezek „saját szerkesztésű"
  ábrák, így saját feliratot kapnak (`[saját szerk.]`).
- **Forrás:** IEEE-hivatkozással (`[N]`, opc. oldalszám) idegen forrásnál; saját készítésű
  vizuálnál `[saját szerk.]`.

## 8. Hivatkozási szabály

- IEEE forrásjegyzék (`## Hivatkozásjegyzék`) kötelező MINDEN 4_wip_outputs és 5_clean_outputs termékben.
- Szövegbeli hivatkozás és lista is `[1]`, `[1,2]`, `[1-3]`, `[1,3,6]`, … (IEEE-szabvány).
- Forrás: `1_raw_inputs/citations.json`; a listát a `_ieee_renderer.py` rendereli `type` szerint:

| `type` | IEEE-formátum |
|--------|---------------|
| `paper` / `slides` | `[N] Szerző, "Cím," *Forrás*, Év.` |
| `book` | `[N] Szerző, *Cím*, Kiadó, Év.` |
| `chapter` | `[N] Szerző, "Cím," in *Könyv*, Év.` |
| `report` | `[N] Szerző, "Cím," *Intézmény*, tech. rep., Év.` |
| `thesis` | `[N] Szerző, "Cím," Ph.D. dissertation, *Intézmény*, Év.` |
| `webpage` | `[N] Szerző, "Cím," *Forrás*. [Online]. Available: URL.` |

## 9. Szerkesztési szabályok
TODO: Ez mehet az alapelvekbe, de ugyanúgy érvényes a tananygra is?
- Csak a szükséges részt módosítsd.
- Kerüld a teljes fájlok fölösleges újragenerálását.
- A redundancia csökkentése elsődleges szempont. 

## 10. Változtatási rend

### 10.1. Soft-cap — a projekt ne bokrosodjon
TODO: Tananyag esetében (test/prod) ez nem igaz. De a projektre fejlesztésére határozottan igaz. És akkor a fenti alapelvek miatt a 10.1 ahogy van, nem is szükséges.
Irányelv, nem szigorú szabály: **a kevesebb néha több.** Törekedj a meglévő fájlok *helyi* javítására ahelyett, hogy újabb és újabb fájlok jönnének létre.

- Először a meglévő fájlt javítsd; új fájl csak akkor, ha tényleg nem fér el sehol.
- Új skill: indokold, miért nem fér el meglévőben.
- Időnként nézd át, mi vonható össze vagy törölhető.

Tájékoztató mérce: `python scripts/_backlog_index.py`.

## 11. Visszajelzések protokoll
TODO: ennek egyértelműnek kellene lennie §4.1 alapján.
A szimbólumok jelentése: §4.1. A bejegyzések helye:

- **Skill-specifikus** megfigyelés/TODO/kérdés → az adott skill `§8 Visszajelzések`.
TODO: De látható, hogy a usernek egyszerűbb a fájlokban a megfelelő környékre illeszteni a megjegyzéseit, ezért a gépi TODO/NOTE azt a Claude vezeti magának.
**Inline TODO/NOTE a szövegtörzsben TILOS** — minden bejegyzés a dedikált szekcióba kerül.
- **Projekt-szintű** → [project_status.md](.claude/project_status.md) (Backlog / Nyitott kérdések).

## 12. Skill-fejlesztési módszertan

**Fejlesztési ciklus:** `draft skill → lépésteszt → eval → fix → commit`
TODO: ezt mintha részletesebben tárgyalná a working_method.md, de a lényeg itt van fent egyetlen sorban.
1. Skill draft a `skill_template.md` alapján (vagy `/skill-creator`)
2. Teszt: 1-2 forrás, 1 fejezet — egyszerű bemenet
3. Eval: `08_quality_check.py` + Claude Explore review
4. Gap-azonosítás: mi hiányzik, mi rossz formátumú?
5. Fix: skill `§3 Eljárás` + `§6 Hibakezelés` frissítése
6. Commit: hard-cap ellenőrzés
TODO: lám-lám itt már hard-cap van. Én azt mondom, hogy mostly hard-cap.

## 13. Nyitott pontok

→ Backlog kezelése: [project_status.md](.claude/project_status.md).

[ ] Minden clean outputs-nak legyen majd egy fejléce és lábléce, de azt még meg kell tervezni
[ ] Nagyon komoly architekturális kérdés, hogy jelen fájl mire vonatkozik? A tervezésre vagy a tananyaggyártásra? Mert kicsit mindkettő az egyben. De persze ha később majd production tananyagot gyártunk, akkor példáula kommunikációs szabályok fontosak. A working_method nagy részét tisztázza a pipeline fejlesztésnek. Lehetne a neve meta_working_method.md és a tantárgyspecifikus munkákra pedig subject_working_method.md
[ ] C:\Users\lasz\.claude\projects\C--Users-lasz-claude-course\memory-ban van négy fájl. egy része már elavult, amit be kell dokumentálni a neki megfelelő backlog-ba. Más részeket pedig át kell ültetni a meta upstream dokumentumokba, hiszen a kevesebb néha több. 
[ ] van hogy egy-egy sprinthez hapsz külső kutatási anyagokat, amik a sprint végén az archive-ba kerülnek. lásd: .claude\archive\Automated Document Image Extraction Pipeline.md és .claude\sprints\image_rag. De ilyen input is például a Kutatási Útmutató Témák Feldolgozásához.md, amivel a tananyagot író skill-jeidet élesítettük. Sajnos akkor nem volt kimondva hogy sprint, de volt hozzá egy megfelelő branch. 
[ ] Valahogy a jelen szakasz "12. Skill-fejlesztési módszertan" és a working_method.md meg a tényleges eljárásaink nem mindig harmonikusak. Maga a pipeline fejlesztést éppen élőben csináljuk, mégse tartjuk be a szabályainkat, módszertanainkat. A branch-en fejlesztés az például egy jó gyakorlat és siker esetén a branch merge, az ág törlése nélkül.
[ ] Egyes sprintek és ágak után azonban marad némi szemét, lásd: .claude\sprints Mert nincs kialakult gyakorlatunk a módszertant illetően. Volt egyszer, hogy 4 ágens 4 Worktree-n dolgozott, csak hát sehol nem látja az ember a szigorú módszertan nyomát.Hát menet közben tanulunk meg járni.