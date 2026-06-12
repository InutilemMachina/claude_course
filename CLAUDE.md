---
title: CLAUDE.md
type: entry_point
tags: [meta]
version: 1.0
updated: 2026-06-02
description: Belépési pont és index a claude_course pipeline-hoz.
---

# CLAUDE.md — claude_course

## 1. Mi ez a projekt?

`claude_course` — Claude-natív tananyagfejlesztési pipeline.

- **NLM nem szükséges.** Claude tölti be az „elmetérkép" szerepét.
- **Mindmap:** a megértés diktálja a struktúrát, nem a fejezetek, de a fejezetekből is lehet mindmap.
- **Vizuálisan gazdag:** Mermaid diagramok, valódi ábrák, MARP prezentáció.
- Archív referencia: [`claude_play`](../claude_play/) (NLM-alapú előd)

## 2. Indulás

Minden session elején ezt a két fájlt olvasd be:

1. [Instructions.md](Instructions.md)
2. [.claude/pipeline.md](.claude/pipeline.md)

**Tantárgyon dolgozva** (ha a feladat egy konkrét `test_outputs/<tárgy>/` vagy `<tárgy>/` alá esik):

3. Olvasd be a tárgy `subject_status.md` §2 tábláját, hogy lásd a heti pipeline állapotát — ebből veszed fel a fonalat.
4. A tábla **mérföldkő-granularitású** (checkpoint, **nem lépésenként**): a `(mérföldkő, hét)` cellát a fázis elérésekor frissítsd — `⚙️` amikor a fázis elkezdődik, `✅` amikor lezárul. A két 🚦-gate (Elmetérkép/03, Publikálható/08) cellája `✅`-t **csak 😎-jóváhagyás után** kap. A köztes lépéseket nem kell cellánként vezetni; a részletes lépés-protokoll a skillek §3-ában van. Ez a szabály felülírja a skillek saját §3 tábla-frissítését.

## 3. Olvasási szabály

Más fájlt csak akkor olvass be, ha a feladat ezt közvetlenül igényli.

- Skill fájl: ha az adott pipeline-lépést futtatod. **Hibakezelés a skill §6-jában van.**
- [.claude/project_status.md](.claude/project_status.md): ha állapotot kell frissíteni.
- [scripts/](scripts/): ha végrehajtó logikára van szükség.

## 4. Fájlkatalógus

Funkcionális index (mi mire való). Elvek és dokumentációs tekintély-sorrend: [Instructions.md](Instructions.md) (§2, §3).

- [Instructions.md](Instructions.md) — projekt-alkotmány: elvek, jelöléstan, szabványok
- [meta_working_method.md](meta_working_method.md) — a pipeline FEJLESZTÉSÉNEK módszertana (refaktor/review session során kövesd)
- [subject_working_method.md](subject_working_method.md) — a tananyag GYÁRTÁSÁNAK végrehajtási módszertana (tantárgyon dolgozva)
- [.claude/pipeline.md](.claude/pipeline.md) — pipeline-gráf, lépések, függőségek
- [.claude/project_status.md](.claude/project_status.md) — futási állapot + Backlog
- [.claude/skill_template.md](.claude/skill_template.md) — skill-sablon
- [.claude/skills/](.claude/skills/) — pipeline-lépések protokolljai (00–13)
- [scripts/](scripts/) — végrehajtó automatizmusok (Python)
- [templates/](templates/) — DUE DOCX/PPTX sablonok és építő scriptek
- `test_sources/`, `test_outputs/` — lépésteszt be-/kimenetek (git-ignorált)

## 5. Kommunikáció

- Tömör, egyszerű, redundanciamentes.
- Ne ismételd meg a globális szabályokat.
- Ha valami nem egyértelmű, a megfelelő kanonikus fájlra hivatkozz.

## 6. Visszajelzések
✅ Link-audit (2026-06-11, F1.5): a doksi összes relatív hivatkozása ellenőrizve (161 link / 33 fájl); a fantom/hibás linkek javítva.