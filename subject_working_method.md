---
title: SUBJECT_WORKING_METHOD — A tananyag-gyártás módszertana
type: meta
tags: [meta]
status: active
version: 1.0
updated: 2026-06-12
description: Hogyan GYÁRTUNK tananyagot egy tantárgyra a pipeline futtatásával — a 😎 végrehajtási fegyelme (gate-birtoklás, camera-ready, nincs shortcut). A pipeline FEJLESZTÉSÉNEK módszertana → meta_working_method.md.
---

# SUBJECT_WORKING_METHOD

**Hogyan dolgozunk egy tantárgy tananyagán**, amikor a pipeline-t futtatjuk (nem a pipeline
fejlesztése — az → [meta_working_method.md](meta_working_method.md)).

A teljes munkamenet egyszerű nyelven + a gráf: [pipeline.md §0](.claude/pipeline.md). Ez a fájl a
**végrehajtási fegyelmet** rögzíti — azt, amit a 😎-nak minden héten tartania kell.

## 1. A heti ciklus

A `subject_status.md §2` tábla a fonal: minden `(lépés, hét)` cellából látszik, hol tartunk
(❌ TODO · ⚙️ folyamatban · ✅ kész · 🚦 checkpoint). A futtatás belépéskor `⚙️`-t, sikeres
befejezéskor `✅`-t ír a cellába; checkpointnál a `✅` csak 😎-jóváhagyás után (CLAUDE.md §2).

A lépés-sorrend és a két gate: [pipeline.md §0 / §3](.claude/pipeline.md). A skillek `§3 Eljárás`-a
a konkrét végrehajtás.

## 2. A 😎 birtokol két döntést

- **🚦 GATE 1 — elmetérkép (03 után):** a 😎 **birtokolja az elmetérképet** — szkóp, mélység, mit
  metsz. A mindmap a megértés sarokköve; a többi ebből vezetődik le. Ne lépj 04-re jóváhagyás nélkül.
- **🚦 GATE 2 — publikálhatóság (08 után):** a 😎 publikál, vagy **célzott revíziót** kér (a Review
  `## 6` csatornán) → a hurok visszamegy 04-re (új forrásnál 01-re). Lásd [08 §3.5](.claude/skills/08_quality_reviewer.md).

A spot-checkek (02/02b, 04, 05, 06, 07) **könnyű felügyelet**, nem gate-ek — de a 😎 bármikor ránézhet.

## 3. Végrehajtási fegyelem (kötelező)

- **Nincs shortcut — a lépést végig kell futtatni.** Egy pipeline-lépést tilos csendben megkerülni
  vagy pótmegoldással helyettesíteni (pl. forrás felvétele a 02-feldolgozás nélkül, valódi
  forrásábra helyett Mermaid-„helyettesítő", kép nélküli sovány PDF). A vizuálisan gazdag kimenet
  **vezérelv** (Instructions §7). Ha egy lépés *kényszerből* kimarad (pl. hiányzó conda-env), azt
  **explicit jelezni** kell 😎-nak és backlogba tenni — nem csendben pótolni. (Részletes elv:
  [meta_working_method §4](meta_working_method.md).)
- **Camera-ready elv** (Instructions §6.1): a tartalom egyetlen helye a `4_wip_outputs/`; a
  `6_clean_outputs/` a véglegesített wip **tiszta konverziója** — sosem szerkeszted kézzel. Minden
  tartalmi munka a 08-gate előtt, a wip-ben történik.
- **Gazdagítás overlay-ként** (12/13): a 😎 koncepciókat jelöl ki, a 🤖 gyárt; az eredmény a
  `5_asset_outputs/`-regiszterbe + a wip stabil horgonyába kerül, nem a kész fájlokba (12/13 §3.2).
- **Forráshűség és citáció:** minden állítás forráshoz kötve (`[N]`), a `## Hivatkozásjegyzék`
  kötelező a wip és clean termékekben (Instructions §8).

## 4. Hivatkozások

- [.claude/pipeline.md](.claude/pipeline.md) — a teljes munkamenet (§0) + gate-ek (§3)
- [Instructions.md](Instructions.md) — §6.1 camera-ready, §7 vizuális gazdagítás, §8 citáció
- [.claude/skills/](.claude/skills/) — az egyes lépések `§3 Eljárás` protokollja
- [meta_working_method.md](meta_working_method.md) — a pipeline FEJLESZTÉSÉNEK módszertana

## 5. Változásjegyzék

<!-- Konvenció: a legfrissebb változás LEGALUL (kronológiai, növekvő sorrend). -->

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-12 | 1.0 | Létrehozva (P2.10, 15. döntés): a `working_method.md` szétbontásából a gyártás-végrehajtási fegyelem (heti ciklus, 2 gate, nincs shortcut, camera-ready, overlay). |
