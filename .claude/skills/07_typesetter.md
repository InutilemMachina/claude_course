---
name: 07_typesetter
title: 07_TYPESETTER — Lint és tipográfiai normalizálás
type: skill
tags: [meta, skill]
role: 🐍
status: active
version: 1.4
updated: 2026-06-11
description: Tipográfiai szabályok alkalmazása, fejezet- és ábra/táblázatfelirat-számozás a WIP jegyzeten (07-1 lint + 07-2 heading + 07-3 figure numberer).
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
python scripts/07-1_typesetter.py --week-dir test_outputs/<tárgy>/N_het
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
python scripts/07-2_heading_numberer.py test_outputs/<tárgy>/N_het/4_wip_outputs/N_Jegyzet.md
```

- `#` → számozatlan (cím marad)
- `##` → `1.`, `2.`, `3.` ...
- `###` → `1.1.`, `1.2.` ...
- Számozatlan függelékek (`UNNUMBERED`): Tartalomjegyzék, Hivatkozásjegyzék, **🔑 Megoldókulcs**, Függelék — emoji-prefix is tolerálva.
- Meglévő számozás felülírása (idempotens)

### 3.3. Ábra-/táblázatfelirat-számozó

```powershell
python scripts/07-3_figure_numberer.py --week-dir test_outputs/<tárgy>/N_het
```

- `*N. ábra. …*` és `*N. táblázat. …*` feliratok **folytonos, külön sorozatú** újraszámozása
  előfordulási sorrendben (Instructions §7.1). Beszúrás/törlés után a kaszkádot determinisztikusan
  rendezi — kézi átszámozás helyett. Idempotens; kódblokkon belül nem nyúl semmihez.
- **Feltétel:** a jegyzetben **nincs szövegközi ábrahivatkozás** (csak feliratok) — lásd
  [04 §8](04_content_synthesizer.md). Ha ez megváltozik, a 07-3-at ref-frissítéssel bővíteni kell.

### 3.4. Manuális ellenőrzés

Claude vizuálisan átnézi a diff-et (git diff):
- Terminológia-egységesítés helyes volt-e?
- LaTeX flagelt sorok javítása

## 4. Kimenetek

| Fájl | Tartalom |
|:-----|:---------|
| `4_wip_outputs/N_Jegyzet.md` | Tipográfiailag normalizált, számozott fejezetek |

## 5. Teszt

- **Fixture:** `test_outputs/atg/1_het` — `1_Jegyzet.md`.
- **Akció:** `07-2_heading_numberer.py` + `07-3_figure_numberer.py` (a 07-1 lint Fázis 2-ben törlődik).
- **Várt kimenet:** Számozott fejezetek (`1.`/`1.1.`), folytonos külön ábra/tábla-sorozat.
- **Eval:** §6 ellenőrzőlista + `git diff` (nincs nem szándékos változás).

## 6. Ellenőrzés

- [ ] Nincs páratlan `$` jel (LaTeX párosítás OK)
- [ ] Fejezetek `1.` `1.1.` formában számozottak
- [ ] Tábla szeparátorok egységesek
- [ ] Magyar idézőjelek (`„"`) használtak
- [ ] `git diff` áttekintve — nincs nem szándékos változás

## 7. Hibakezelés

| Tünet | Ok | Megoldás |
|:------|:---|:---------|
| LaTeX képlet megváltoztatva | Terminológia regex túl általános | Regex szűkítése; `<!-- NOFIX -->` komment |
| Fejezetek kétszer számozva | `heading_numberer` kétszer futott | Idempotens: újrafuttatás felülírja |
| Tábla szeparátor felülírta a jobb-igazítást | Script nem kezeli `--:` mintát | Script javítása: `--:` és `:--:` megtartása |
| Terminológia hibás egységesítés | Kontextus-érzéketlen regex | `subject_status.md §5` terminológia listát pontosítani |

## 8. Hivatkozások

- [pipeline.md](../pipeline.md)
- [06_summarize_box_injector.md](06_summarize_box_injector.md) — upstream
- [08_quality_reviewer.md](08_quality_reviewer.md) — downstream

## 9. Visszajelzések

<!-- Tesztelés során felmerülő megfigyelések, TODO-k, kérdések. -->
- ✅ Rule H gyökérhiba javítva: korábban az en-dash tartományt (`1–35`→`1, 35`), a `---` HR-t (`, -`) és a GFM tábla-szeparátort is elrontotta. Mostantól csak ASCII `--`-t cserél vesszőre; `–`/`—`, HR- és tábla-sorok érintetlenek. (project_status B-11)
- ✅ CLI doc-drift JAVÍTVA (2026-06-07): a §3.1/§3.2 most a tényleges `--week-dir` / pozicionális fájl-formát mutatja (korábban hibás `--week/--subject`).
- ⚡ CRLF/sortörés gyökérhiba JAVÍTVA (2026-06-07): a `07-3` korábban `read_bytes().decode()` után `splitlines(keepends=True)`-zal megőrizte a `\r\n`-t, a `write_text` OS-fordítása pedig `\r\r\n`-t gyártott; egy következő univerzális-newline olvasás ezt `\n\n`-re tágította → **minden üres sor megduplázódott** (a jegyzet 616→1232 sor). **Szabály minden md-író scriptre:** olvasáskor normalizálj LF-re (`.replace("\r\n","\n").replace("\r","\n")`, mint a `07-1`), és ne írj újra már `\r\n`-t tartalmazó stringet OS-fordítással. (atg/1_het: helyreállítva a newline-futamok felezésével.)
- ✅ `07-2` Megoldókulcs-számozás JAVÍTVA (2026-06-07): a `## 🔑 Megoldókulcs` függeléket korábban `## 7.`-ként számozta, mert (a) `megoldokulcs` nem volt az `UNNUMBERED`-ben, és (b) a `_normalize` nem tűrte a vezető `🔑` emojit. Most az `UNNUMBERED` bővült (`megoldokulcs`, `fuggelek`), a `_normalize` pedig minden nem-alfanumerikus jelet (emoji is) eldob.

## 10. Változásjegyzék

| Dátum | Verzió | Leírás |
|-------|--------|--------|
| 2026-06-01 | 1.0 | Létrehozva (mint 06_typesetter) |
| 2026-06-03 | 1.1 | Átszámozva 06→07 (05 szétválása miatt); script-hivatkozások 07-1/07-2 |
| 2026-06-06 | 1.2 | `07-1` Rule H gyökérjavítás: csak ASCII `--` kezelése; en/em-dash, HR és tábla-sorok védve (adatromlás megszüntetve) |
| 2026-06-07 | 1.3 | Új **07-3_figure_numberer.py** (§3.3): ábra/táblázatfelirat folytonos újraszámozása beszúrás után. §3.1/§3.2 CLI doc-fix (`--week-dir`). `07-2` javítás: `🔑 Megoldókulcs`/`Függelék` számozatlan (emoji-tűrő `_normalize`). `07-3` CRLF-gyökérhiba javítva (olvasás-normalizálás). Frontmatter-verzió szinkronizálva. |
| 2026-06-11 | 1.4 | §Teszt pótolva (atg/1_het); §5→§10 átszámozva (sablon-konform). |
