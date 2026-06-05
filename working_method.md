---
title: WORKING_METHOD — A pipeline fejlesztésének módszertana
type: meta
tags: [meta]
status: active
version: 1.0
updated: 2026-06-03
description: A „módszertanok módszertana" — hogyan fejlesztjük/refaktoráljuk magát a pipeline-t. Kövesd minden review/refaktor session során.
---

# WORKING_METHOD

A „módszertanok módszertana": **hogyan dolgozunk a pipeline fejlesztésén** (nem a tananyag-pipeline maga — az → Instructions.md, pipeline.md).
Ezt a fájlt követem minden átnézési/refaktor session során.

## 1. Vezérelvek

A már kodifikált elveket nem ismétlem, csak megerősítem (kanonikus hely zárójelben):

- **A kevesebb néha több** — soft-cap, ne bokrosodjon; helyi javítás > új fájl (Instructions §10).
- **Cél-orientált** - a beszélgetések a célra tartsanak, ne a bokrosodás irányába.
- **Tisztaság és egyértelműség** — rövid, világos, szabványos (Instructions §2).
- **Egy fájl = egy cél; egy információ egy kanonikus helyen** (Instructions §2).
- **Interfész-központúság** — minden lépésnek explicit be- és kimenete van.
- **Cselekedj lokálisan, gondolkodj globálisan**  — Minden lépés kihatással lehet a pipeline más részeire.
- (Előre fele haladva dolgozunk a tananyag-pipeline-on ezért későbbi lépések lehet, hogy nem lesznek már adekvátak)
- **NLM-mentesség** — a `claude_play` maradványait felismerjük és irtjuk.
- **Best practice elsőként** — Anthropic skill-elvek + skill_template.md + ha van references.

## 2. Az állomás-túra (a review-ciklus)

Lépésről lépésre a belépési ponttól: `CLAUDE.md → Instructions.md → pipeline.md → skills 00–10 (+ scriptek) → templates`.
Nyugodt, szisztematikus tempó. Minden állomáson:

0. **Cél-tisztázás** — ismertesd a jelenlegi forgatókönyvet (mit tud/csinál a skill most), majd kérdezd meg: „Mi lenne az elképzelésed / szándékod?" Ne feltételezd, hogy a jelenlegi állapot a kívánt.
1. **Olvasás tetőtől talpig** — a skill ÉS a hozzá tartozó script(ek) együtt.
2. **Audit** — felesleg / redundancia / ellentmondás / hiányzó hibakezelés / fantom-hivatkozás.
3. **Teszt** — valódi fixture-ön (`atg` = sok kis forrás, `dft` = 1 könyv).
4. **Fix + visszajelzés**, majd **commit** tiszta egységként.
5. **Iteráció** — ugyanazt a fájlt finomítjuk, amíg elég jó nem lesz.

## 3. A kérdések, amiket minden lépésnél felteszünk

- **Mi a cél?** (ha nem egyértelmű → kérdezz, ne találgass)
- **Hol van felesleg / redundancia / ellentmondás?**
- **Tényleg kell-e** minden mező / szekció / fájl?
- **Mi a be- és kimenet?** Koherens-e **upstream ÉS downstream**?
- **Követi-e a best practice-t** (Anthropic + skill_template + references)?
- **Tesztelhető-e? Le van-e tesztelve** valódi adaton?
- **YAML header, globális értelmesség, a fájl szerepe és kontextusa** rendben?
- **A linkek valódi, létező fájlra mutatnak?** (relatív útvonal-mélység is)
- **Erősség / gyengeség** — támogatja-e a származó munkát helyesen és logikusan?

## 4. Munkamódszer-megállapodások (session-döntések)

- **Sablon ott él, ahova példányosodik** — subject_status_template → templates/; skill_template → .claude/.
- **Frontmatter gépi, törzs emberi** (ahol értelmes); felelős-jelzés: 🐍 script · 🤖 Claude · 😎 ember.
- **Triggerelő `description`** (mi + mikor), nem „blurb".
- **Igazított, olvasható táblák** — ember és gép számára is; a pipeline.md a kettős master-doc.
- **Őszinte napló** — a riport pontosan tükrözze a valóságot.
- **Minden skillnek legyen §Teszt** — fixture → akció → várt kimenet → eval, atg/dft-re.
- **Mindent a maga idejében** — ami most nem aktuális, jegyezd fel (backlog / nyitott kérdés).

## 5. Munkamenet-szokások

- Bátran kérdezz **tartalmilag is**, ne csak strukturálisan — bármikor.
- **Globális strukturális kérdés** bármikor felvethető.
- **Commit** tiszta egységenként, beszédes üzenettel; **push csak kérésre**.
- Nyitott szálakat ne ejts el → project_status.md (backlog / nyitott kérdés).

## 6. Hivatkozások

- Instructions.md — alkotmány (elvek, jelöléstan, §12 skill-fejlesztési ciklus)
- pipeline.md — futási gráf
- skill_template.md — a skillek sablonja
- project_status.md — állapot, backlog, nyitott kérdések

## 7. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-03 | 1.0 | Létrehozva — a session módszertani inputjaiból |