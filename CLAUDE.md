---
title: CLAUDE.md
type: entry_point
tags: [meta]
version: 1.0
updated: 2026-06-01
---

# CLAUDE.md — claude_course

## 1. Indulás

Minden session elején ezt a két fájlt olvasd be:

1. [`Instructions.md`](Instructions.md)
2. [`.claude/pipeline.md`](.claude/pipeline.md)

## 2. Olvasási szabály

Más fájlt csak akkor olvass be, ha a feladat ezt közvetlenül igényli.

- Skill fájl: ha az adott pipeline-lépést futtatod. **Hibakezelés a skill §6-jában van.**
- `project_status.md`: ha állapotot kell frissíteni.
- `scripts/*.py`: ha végrehajtó logikára van szükség.

## 3. Elvek

→ Lásd [Instructions.md](Instructions.md).

## 4. Fájlkatalógus

- [Instructions.md](Instructions.md) — projekt-alkotmány
- [.claude/pipeline.md](.claude/pipeline.md) — pipeline és függőségek
- [.claude/project_status.md](.claude/project_status.md) — futási állapot + Backlog
- [.claude/skill_template.md](.claude/skill_template.md) — skill-sablon
- [.claude/skills/](.claude/skills/) — pipeline-lépések
- [scripts/](scripts/) — automatizmusok
- [.claude/archive/](.claude/archive/) — elavult skillek, naplók

## 5. Kommunikáció

- Tömör, egyértelmű, redundanciamentes.
- Ne ismételd meg a globális szabályokat.
- Ha valami nem egyértelmű, a megfelelő kanonikus fájlra hivatkozz.

## 6. Mi ez a projekt?

`claude_course` — Claude-natív tananyagfejlesztési pipeline.

- **NLM nem szükséges.** Claude tölti be az „elmetérkép" szerepét.
- **Mindmap-first:** a megértés diktálja a struktúrát, nem a fejezetek.
- **Vizuálisan gazdag:** Mermaid diagramok, valódi ábrák, MARP prezentáció.
- Archív referencia: [`claude_play`](../claude_play/) (NLM-alapú előd)
