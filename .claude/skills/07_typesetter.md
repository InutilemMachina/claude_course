---
name: 07_typesetter
title: 07_TYPESETTER — Lint és tipográfiai normalizálás
type: skill
tags: [meta, skill]
role: 🐍
status: active
version: 1.1
updated: 2026-06-03
description: Tipográfiai szabályok alkalmazása és fejezetek automatikus számozása a WIP jegyzeten.
---

# 07_TYPESETTER

## 1. Cél

A `4_wip_outputs/N_Jegyzet.md` tipográfiáját normalizálja: dash cleanup, LaTeX párosítás,
terminológia-egységesítés, tábla szeparátor javítás, majd automatikus fejezetszámozás.

**Input:** `4_wip_outputs/N_Jegyzet.md`
**Output:** `4_wip_outputs/N_Jegyzet.md` (normalizálva, in-place)

## 2. Bemenetek

| Fájl | Honnan | Tartalom |
|:-----|:-------|:---------|
| `4_wip_outputs/N_Jegyzet.md` | 06_summarize_box_injector | Gazdagított WIP jegyzet |

**Előfeltétel:** `06_summarize_box_injector` lefutott.

## 3. Eljárás

### 3.1. Tipográfiai normalizáló

```powershell
python scripts/07-1_typesetter.py --week N --subject "Jelatvitel"
```

**Alkalmazott szabályok:**

| Szabály | Minta | Javítás |
|:--------|:------|:--------|
| Dash cleanup | `--`, `—` (rossz kontextus) | `–` (en-dash) vagy `—` (em-dash) egységesen |
| LaTeX párosítás | páratlan `$` jelek | párosítás ellenőrzése, hibás sorok flagelése |
| Terminológia | `digitális jel feldolgozás` | `digitális jelfeldolgozás` (subject_status.md §5 terminológia) |
| Tábla szeparátor | `|---|` `|:--|` vegyes | `|:---|` egységes bal-igazítás |
| Whitespace | trailing space, dupla üres sor | törlés |
| Idézőjel | `"szó"` | `„szó"` (magyar) |

### 3.2. Fejezet-számozó

```powershell
python scripts/07-2_heading_numberer.py --week N --subject "Jelatvitel"
```

- `#` → számozatlan (cím marad)
- `##` → `1.`, `2.`, `3.` ...
- `###` → `1.1.`, `1.2.` ...
- Meglévő számozás felülírása (idempotens)

### 3.3. Manuális ellenőrzés

Claude vizuálisan átnézi a diff-et (git diff):
- Terminológia-egységesítés helyes volt-e?
- LaTeX flagelt sorok javítása

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Jegyzet.md` | Tipográfiailag normalizált, számozott fejezetek |

## 5. Ellenőrzés

- [ ] Nincs páratlan `$` jel (LaTeX párosítás OK)
- [ ] Fejezetek `1.` `1.1.` formában számozottak
- [ ] Tábla szeparátorok egységesek
- [ ] Magyar idézőjelek (`„"`) használtak
- [ ] `git diff` áttekintve — nincs nem szándékos változás

## 6. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| LaTeX képlet megváltoztatva | Terminológia regex túl általános | Regex szűkítése; `<!-- NOFIX -->` komment |
| Fejezetek kétszer számozva | `heading_numberer` kétszer futott | Idempotens: újrafuttatás felülírja |
| Tábla szeparátor felülírta a jobb-igazítást | Script nem kezeli `--:` mintát | Script javítása: `--:` és `:--:` megtartása |
| Terminológia hibás egységesítés | Kontextus-érzéketlen regex | `subject_status.md §5` terminológia listát pontosítani |

## 7. Hivatkozások

- [pipeline.md](../pipeline.md)
- [06_summarize_box_injector.md](06_summarize_box_injector.md) — upstream
- [08_quality_reviewer.md](08_quality_reviewer.md) — downstream

## 8. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->

## 9. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (mint 06_typesetter) |
| 2026-06-03 | 1.1 | Átszámozva 06→07 (05 szétválása miatt); script-hivatkozások 07-1/07-2 |
