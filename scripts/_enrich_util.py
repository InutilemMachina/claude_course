"""
_enrich_util.py -- 12/13 gazdagítási overlay segéd (utility, nincs külön skill).

Az overlay+regiszter modell (12/13 §3.2) mechanikus magja:
  - parse_register()     : a 5_asset_outputs/enrichment_register.md markdown-tábláját sorokká
  - resolve_anchors()    : a wip `<!-- ENRICH: <id> -->` horgonyt látható `> 📎▶/📎🧪` blokká oldja
  - render_version_log() : a regiszterből `## Verziójegyzék` appendixet generál (verziónként)
  - current_version() / bump_version() : termék-verzió kezelés (MAJOR.MINOR)

A `11-2_pandoc_export.py` / `10_pptx_gyarto.py` `--enrich` ága és a `_republish.py` orchestrator hívja.
"""

from __future__ import annotations

import re
from pathlib import Path

# `<!-- ENRICH: v1 -->` / `<!-- ENRICH: nb2 -->`
_RE_ANCHOR = re.compile(r"<!--\s*ENRICH:\s*([A-Za-z]+\d+)\s*-->")
# `product_version: 1.1` a wip YAML frontmatterben
_RE_PVER = re.compile(r"^product_version:\s*([0-9]+\.[0-9]+)\s*$", re.MULTILINE)
_RE_SEP_CELL = re.compile(r"^:?-+:?$")


# ── Regiszter ─────────────────────────────────────────────────────────────────

def _norm_key(cell: str) -> str:
    """Oszlopfejléc → kulcs az első szóból (pl. 'horgony (wip hely)' → 'horgony')."""
    return cell.strip().lower().split()[0] if cell.strip() else ""


def parse_register(path: Path) -> list[dict]:
    """A enrichment_register.md első markdown-tábláját sor-dict-ekké parse-olja.

    A kulcsok az oszlopfejléc első szavai: id, típus, horgony, koncepció, link, meta,
    verzió, dátum, állapot (a régebbi, verzió/dátum nélküli sémát is elnyeli).
    """
    if not path.exists():
        return []
    header: list[str] | None = None
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if header is None:
            header = [_norm_key(c) for c in cells]
            continue
        if all(_RE_SEP_CELL.match(c) or c == "" for c in cells):
            continue  # `|---|:--|` szeparátor sor
        rows.append({k: v for k, v in zip(header, cells) if k})
    return rows


def _block(row: dict) -> str:
    """Egy regiszter-sorból a látható blockquote (📎▶ videó / 📎🧪 notebook)."""
    tipus = row.get("típus", "📎")
    koncepcio = row.get("koncepció", row.get("id", ""))
    link = row.get("link", "").strip()
    meta = row.get("meta", "").strip()
    head = f"> {tipus} **{koncepcio}**"
    if link and link not in ("…", "-"):
        head += f" — [{link}]({link})"
    lines = [head]
    if meta and meta not in ("…", "-"):
        lines.append(f"> {meta}")
    return "\n".join(lines)


def resolve_anchors(wip_text: str, rows: list[dict]) -> tuple[str, list[str], list[str]]:
    """A `<!-- ENRICH: <id> -->` horgonyokat feloldja a regiszter ✅-állapotú sorai alapján.

    Visszaad: (feloldott_szöveg, feloldott_id-k, feloldatlan_id-k). A nem-✅ vagy hiányzó
    id-jú horgony érintetlen marad (nem tör be vakon).
    """
    by_id = {r.get("id"): r for r in rows if r.get("id")}
    resolved: list[str] = []
    unresolved: list[str] = []

    def _sub(m: re.Match) -> str:
        rid = m.group(1)
        r = by_id.get(rid)
        if not r or "✅" not in r.get("állapot", ""):
            unresolved.append(rid)
            return m.group(0)
        resolved.append(rid)
        return _block(r)

    return _RE_ANCHOR.sub(_sub, wip_text), resolved, unresolved


def render_version_log(rows: list[dict]) -> str:
    """`## Verziójegyzék` markdown a regiszterből, verziónként csoportosítva (újabb felül).

    Minden ✅ sor a saját `verzió`-jánál jelenik meg, a `horgony` helyével és típusával.
    """
    by_ver: dict[str, list[dict]] = {}
    for r in rows:
        if "✅" not in r.get("állapot", ""):
            continue
        by_ver.setdefault(r.get("verzió", "v?"), []).append(r)

    def _vkey(v: str) -> tuple:
        nums = re.findall(r"\d+", v)
        return tuple(int(n) for n in nums) if nums else (0,)

    lines = ["## Verziójegyzék", ""]
    for ver in sorted(by_ver, key=_vkey, reverse=True):
        items = by_ver[ver]
        date = items[0].get("dátum", "")
        vids = [i for i in items if "▶" in i.get("típus", "")]
        nbs = [i for i in items if "🧪" in i.get("típus", "")]
        parts = []
        if vids:
            parts.append(f"+{len(vids)} 📎▶ ({', '.join(i.get('horgony', '?') for i in vids)})")
        if nbs:
            parts.append(f"+{len(nbs)} 📎🧪 ({', '.join(i.get('horgony', '?') for i in nbs)})")
        suffix = (": " + "; ".join(parts)) if parts else ""
        ver_disp = "v" + ver.lstrip("v")
        lines.append(f"- **{ver_disp}** ({date}){suffix}")
    lines.append("- **v1.0** — első kiadás")
    return "\n".join(lines) + "\n"


def stamp_register(path: Path, version: str, date: str, dry_run: bool = False) -> list[str]:
    """A ✅-állapotú, még verzió nélküli regiszter-sorokat megjelöli (`verzió`+`dátum`).

    Visszaad: a megjelölt id-k listája. A markdown-tábla szerkezetét megőrzi (oszlop-index alapján).
    Ha nincs `verzió`/`dátum` oszlop a fejlécben, nem módosít (üres listát ad).
    """
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    keys: list[str] | None = None
    vi = di = None
    stamped: list[str] = []
    out: list[str] = []
    for line in lines:
        s = line.strip()
        if not s.startswith("|"):
            out.append(line)
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if keys is None:
            keys = [_norm_key(c) for c in cells]
            if "verzió" in keys and "dátum" in keys:
                vi, di = keys.index("verzió"), keys.index("dátum")
            out.append(line)
            continue
        if all(_RE_SEP_CELL.match(c) or c == "" for c in cells):
            out.append(line)
            continue
        if vi is not None and len(cells) == len(keys):
            row = dict(zip(keys, cells))
            if "✅" in row.get("állapot", "") and not row.get("verzió", "").strip():
                cells[vi], cells[di] = version, date
                stamped.append(row.get("id", ""))
                line = "| " + " | ".join(cells) + " |"
        out.append(line)
    if stamped and not dry_run:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return stamped


# ── Verzió ────────────────────────────────────────────────────────────────────

def current_version(wip_text: str) -> str:
    """A wip frontmatter `product_version` mezője (default 1.0)."""
    m = _RE_PVER.search(wip_text)
    return m.group(1) if m else "1.0"


def bump_version(version: str, kind: str = "minor") -> str:
    """MAJOR.MINOR bump. minor → x.(y+1); major → (x+1).0."""
    major, minor = (int(p) for p in version.split("."))
    if kind == "major":
        return f"{major + 1}.0"
    return f"{major}.{minor + 1}"


def set_version(wip_text: str, version: str) -> str:
    """A wip frontmatter `product_version`-jét beállítja (ha nincs, a frontmatter végére szúrja)."""
    if _RE_PVER.search(wip_text):
        return _RE_PVER.sub(f"product_version: {version}", wip_text, count=1)
    lines = wip_text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                lines.insert(i, f"product_version: {version}")
                return "\n".join(lines) + ("\n" if wip_text.endswith("\n") else "")
    return wip_text
