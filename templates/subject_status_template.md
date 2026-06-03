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

- **Szint:** BSc / MSc / mindkettő
- **Félév:** heti óraszám, struktúra
- **Célcsoport:** szak, évfolyam

## 2. Heti pipeline-státusz 🤖 😎

- 🤖 a státusz-cellákat frissíti futás közben
- 😎 a témákat tölti.

{{STATUS_TABLE}}

❌ TODO · ⚙️ folyamatban · ✅ kész · 🚦 checkpoint (😎 jóváhagyás)

## 3. Célok 😎

- **BSc szint:**
- **MSc szint:**

## 4. Stílusirányelvek 😎

- **Nyelv:** magyar szöveg, kétnyelvű terminológia (pl. „termogram / thermogram")
- **Terminológia-egységesítés** (a [`06 typesetter`]({{ROOT_REL}}/.claude/skills/06_typesetter.md) használja):
- **Jegyzet sablon:** [`due_jegyzet_template.docx`]({{ROOT_REL}}/templates/due_jegyzet_template.docx)
- **Prezentáció sablon:** [`due_prenetation_template.pptx`]({{ROOT_REL}}/templates/due_prenetation_template.pptx)
- **Kérdésbank:** feleletválasztós A/B/C/D, SZINT 2–5

<!-- MINTA-HATÁR: a 00_init innentől NEM másol az instancekba — ez csak a sablon dokumentációja. -->

## Mintatáblázat — így néz ki kitöltve (példa, 3 hét)

| Lépések (↓) / Hetek (→) | 1           | 2           | 3           |
| :---------------------- | :---------- | :---------- | :---------- |
| *Téma*                  | Surge       | Stall       | Aktív szab. |
| 00 init                 | ✅          | ✅          | ✅          |
| 01 source_collector     | ✅          | ✅          | ⚙️          |
| 02 image_extraction     | ✅          | ✅          | ❌          |
| 03 mindmap 🚦           | ✅          | ✅          | ❌          |
| 04 content_synthesizer  | ✅          | ✅          | ❌          |
| 05 visual_enricher      | ✅          | ⚙️          | ❌          |
| 06 typesetter           | ✅          | ❌          | ❌          |
| 07 quality_reviewer 🚦  | ✅          | ❌          | ❌          |
| 08 question_bank        | ✅          | ❌          | ❌          |
| 09 presentation_maker   | ✅          | ❌          | ❌          |
| 10 bsc_export           | ✅          | ❌          | ❌          |
