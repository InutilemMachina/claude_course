---
title: META_WORKING_METHOD — A pipeline fejlesztésének módszertana
type: meta
tags: [meta]
status: active
version: 2.0
updated: 2026-06-12
description: A „módszertanok módszertana" — hogyan FEJLESZTJÜK/refaktoráljuk magát a pipeline-t. Kövesd minden review/refaktor session során. (A tananyag GYÁRTÁSÁNAK módszertana → subject_working_method.md.)
---

# META_WORKING_METHOD

A „módszertanok módszertana": **hogyan dolgozunk a pipeline fejlesztésén** (nem a tananyag-pipeline maga — az → [Instructions.md](Instructions.md), [pipeline.md](.claude/pipeline.md)).
Ezt a fájlt követem minden átnézési/refaktor session során. A **tananyag-gyártás** végrehajtási
módszertana külön: [subject_working_method.md](subject_working_method.md).

## 1. Vezérelvek

A már kodifikált elveket nem ismétlem, csak megerősítem (kanonikus hely zárójelben):

- **A kevesebb néha több** — általában hard-cap, néha soft-cap: ne bokrosodjon; helyi javítás > új fájl (Instructions §10).
- **Cél-orientált** - a beszélgetések a célra tartsanak, ne a bokrosodás irányába.
- **Tisztaság és egyértelműség** — rövid, világos, szabványos (Instructions §2).
- **Egy fájl = egy cél; egy információ egy kanonikus helyen** (Instructions §2).
- **Interfész-központúság** — minden lépésnek explicit be- és kimenete van.
- **Cselekedj lokálisan, gondolkodj globálisan**  — Minden lépés kihatással lehet a pipeline más részeire.
- **Fixture-ből absztrahálj** — a `test_outputs/<tárgy>/` csak fixture; a **termék a skill/script**.
  Egy konkrét megfigyelésből (egy tananyag hibája/igénye) mindig az **általános erejű szabályt** vond
  ki, és azt kodifikáld. A domain-specifikum *teszteli* és *kiváltja* a szabályt, de nem szivároghat a
  kanonikus rétegbe: a skill-példák is absztrakt placeholderrel íródnak (`Főtéma`, `Eq.X.Y`), nem a
  fixture fogalmaival. (Egy eset → szabály, nem egy eset → toldás.)
- **Kerüljük a terv bokrosítását**, minden hozzáadott fájl és logikai kapu erősen indokolt esetben lehetséges, a user-t erre figyelmeztetni kell. 
- Előre fele haladva dolgozunk a tananyag-pipeline-on, ezért:
  - későbbi lépések lehet, hogy nem lesznek már adekvátak
  - vagy korábbi lépésekeket is javítunk
így **fontos, hogy re-usable és világos absztrahált megoldásokat találjunk**
- **Best practice elsőként** — Anthropic skill-elvek + skill_template.md + ha van references.
- **NLM-mentesség** — a `claude_play` maradványait felismerjük és irtjuk.
- **A feladathoz illő Claude agent-ek** - terveidbe vedd bele, hogy milyen szintű agent-ekre van szükség milyen feladatokhoz, hogy a tokenekkel takarékoskodjunk. A kognitív feladatok erősebb agent-eket kívánnak, míg egyszerűbb feladatok olcsóbb modelleket.

## 2. Az állomás-túra (a review-ciklus)

Lépésről lépésre a belépési ponttól: `CLAUDE.md → Instructions.md → pipeline.md → skills 00–13 (+ scriptek) → templates`.
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
- **Nincs shortcut — a lépést végig kell futtatni.** Egy pipeline-lépést tilos csendben megkerülni
  vagy pótmegoldással helyettesíteni (pl. új forrás felvétele a **02-feldolgozás** — képkinyerés +
  `figure_catalog` — nélkül, vagy valódi forrásábra helyett Mermaid-„helyettesítő", vagy kép nélküli
  sovány forrás-PDF). A vizuálisan gazdag kimenet **vezérelv** (Instructions §7): a forrás képeinek
  ténylegesen be kell kerülniük a `2_clean_inputs/`-ba. Ha egy lépés *kényszerből* kimarad (pl. hiányzó
  conda-env), azt **explicit jelezni** kell 😎-nak (és backlogba tenni) — nem csendben pótolni. A
  „működik a teszthez" nem cél; a **lépés helyes lefutása** a cél.

## 5. Munkamenet-szokások

- Bátran kérdezz **tartalmilag is**, ne csak strukturálisan — bármikor.
- **Globális strukturális kérdés** bármikor felvethető.
- **Commit** tiszta egységenként, beszédes üzenettel; **push csak kérésre**.
- **Git-tanító mód (😎 a git-et tanulja):** minden git-művelet előtt/közben a Bash-parancsokat
  **tanító jelleggel** ki kell írni 😎-nak — a parancs + egy mondat, hogy *mit csinál és miért*
  (pl. `git switch main` → „átváltunk a fő ágra, ide olvasztjuk be a branchet"). A cél, hogy 😎 a
  művelet menetét kövesse és tanulja, ne csak az eredményt lássa.
- Nyitott szálakat ne ejts el → project_status.md (backlog / nyitott kérdés).

## 6. Hivatkozások

A fejlesztés ezekre a kanonikus forrásokra épül:

- [Instructions.md](Instructions.md) — alkotmány (elvek, jelöléstan, §12 skill-fejlesztési ciklus)
- [.claude/pipeline.md](.claude/pipeline.md) — futási gráf + HITL-modell
- [.claude/skill_template.md](.claude/skill_template.md) — a skillek sablonja
- [.claude/project_status.md](.claude/project_status.md) — állapot, backlog, nyitott kérdések
- [subject_working_method.md](subject_working_method.md) — a tananyag-gyártás végrehajtási módszertana

## 7. Változásjegyzék

<!-- Konvenció (Instructions): a legfrissebb változás LEGALUL (kronológiai, növekvő sorrend). -->

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-03 | 1.0 | Létrehozva — a session módszertani inputjaiból |
| 2026-06-06 | 1.1 | §1 új vezérelv: „Fixture-ből absztrahálj" — konkrét esetből általános szabályt kodifikálunk; a domain-specifikum nem szivárog a skill/script kanonikus rétegébe. |
| 2026-06-07 | 1.2 | §4 új megállapodás: **„Nincs shortcut — a lépést végig kell futtatni"** (forrás 02-feldolgozása kötelező, valódi ábra > Mermaid-helyettesítő, kényszerű kihagyást explicit jelezni). `quality_review_test` tanulság. |
| 2026-06-07 | 1.3 | §5 új szokás: **Git-tanító mód** — minden git-művelet Bash-parancsait tanító jelleggel (parancs + mit/miért) kiírjuk 😎-nak, mert 😎 a git-et tanulja. |
| 2026-06-12 | 2.0 | **Szétbontás (P2.10, 15. döntés):** `working_method.md` → `meta_working_method.md` (fejlesztés) + új `subject_working_method.md` (gyártás). §2 „skills 00–10" → „00–13"; §6 valódi markdown-linkek + a `[ ]` TODO feloldva; cím/description a fejlesztési fókuszra élesítve. |