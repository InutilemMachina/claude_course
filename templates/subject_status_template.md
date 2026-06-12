---
title: {{SUBJECT}} — tantárgy-státusz
type: subject_status
tags: [{{TAGS}}]
subject: {{SUBJECT}}
weeks: {{WEEKS}}
created: {{DATE}}
updated: {{DATE}}
description: Tantárgy-szintű terv és pipeline-státusz. Frontmatter gépi (00_init tölti); törzs ember + Claude.
---

# {{SUBJECT}} — tantárgy-státusz

Szerepek: 
- 🐍 script 
- 😎 ember
- 🤖 Claude.

A projekt-szintű `project_status.md` tantárgy-szintű megfelelője.

## 1. Alapadatok 😎

- **Félév:** heti óraszám, struktúra
- **Célcsoport:** szak, évfolyam

## 2. Heti pipeline-státusz 🤖 😎

- 🤖 a státusz-cellákat frissíti futás közben
- 😎 a témákat tölti.

{{STATUS_TABLE}}

❌ TODO · ⚙️ folyamatban · ✅ kész · 🚦 checkpoint (😎 jóváhagyás)

## 3. Célok 😎

- **Tanulási célok:**

## 4. Stílusirányelvek 😎

- **Nyelv:** magyar szöveg, kétnyelvű terminológia (pl. „termogram / thermogram")
- **Terminológia-egységesítés** (a [`07 typesetter`]({{ROOT_REL}}/.claude/skills/07_typesetter.md) használja):
- **Jegyzet sablon:** [`due_jegyzet_template.docx`]({{ROOT_REL}}/templates/due_jegyzet_template.docx)
- **Prezentáció sablonok (2 variáns):** [`due_presentation_default_master.potx`]({{ROOT_REL}}/templates/due_presentation_default_master.potx) (default) · [`due_presentation_mindmap_master.potx`]({{ROOT_REL}}/templates/due_presentation_mindmap_master.potx) (mindmap). Kitöltési minta: [`due_presentation_default_reference.pptx`]({{ROOT_REL}}/templates/due_presentation_default_reference.pptx)
- **Kérdésbank:** feleletválasztós A/B/C/D, SZINT 2–5

<!-- MINTA-HATÁR: a 00_init innentől NEM másol az instancekba — ez csak a sablon dokumentációja. -->

## Mintatáblázat — így néz ki kitöltve (példa, 3 hét)

A tábla **mérföldkő-granularitású** (checkpoint, nem lépésenként): a cellát a fázis elérésekor
frissítjük, a két 🚦-gate `✅`-ját csak 😎-jóváhagyás után (lásd CLAUDE.md §2).

| Mérföldkő (↓) / Hetek (→) | 1     | 2     | 3           |
| :------------------------ | :---- | :---- | :---------- |
| *Téma*                    | Surge | Stall | Aktív szab. |
| Setup (00–01)             | ✅    | ✅    | ⚙️          |
| Feldolgozás (02–02b)      | ✅    | ✅    | ❌          |
| Elmetérkép 🚦 (03)        | ✅    | ✅    | ❌          |
| WIP jegyzet (04–07)       | ✅    | ⚙️    | ❌          |
| Publikálható 🚦 (08)      | ✅    | ❌    | ❌          |
| Kimenetek (09–11)         | ✅    | ❌    | ❌          |
| Gazdagítás (12–13)        | ❌    | ❌    | ❌          |
