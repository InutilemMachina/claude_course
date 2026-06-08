"""_nav_util.py — Megosztott navigációs modell (mindmap-fa → breadcrumb / TOC).

A `10_presentation_maker` két prezentáció-variánsa (default / mindmap) ugyanabból
a navigációs modellből származik: a `3_mindmap/mindmap.md` Mermaid-fája + „hol vagyok"
(aktuális csomópont). Ez a util parse-olja a fát, és kétféleképpen rendereli:

  - render_breadcrumb(...)  → DEFAULT nézet: szakasz-útvonal (többsoros fejléc-cím)
  - render_toc(...)         → MINDMAP nézet: beágyazott sorszámozott TOC szöveg

Használja: `10_pptx_gyarto.py` (PPTX idx0/idx5), `10-2_nav_inject.py` (MARP renditionök).

A két renderelő SZÖVEGET ad — a navigáció soha nem kép. A jegyzetből vett valódi
folyamatábrák ettől függetlenül Mermaid→PNG-ként élnek a belső diákon (10-1).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# Adatmodell
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class NavNode:
    id: str                              # "ROOT", "N2", "N25"
    num: str = ""                        # "" | "2" | "2.5"  (címke-prefixből)
    title: str = ""                      # "Kompresszortérkép" (prefix és [MSc] nélkül)
    label_raw: str = ""                  # eredeti Mermaid-címke
    msc: bool = False                    # True, ha [MSc] tag a címkében
    children: list["NavNode"] = field(default_factory=list)
    parent: "NavNode | None" = field(default=None, repr=False)

    def walk(self):
        """Preorder bejárás (önmaga + leszármazottak)."""
        yield self
        for c in self.children:
            yield from c.walk()


# ─────────────────────────────────────────────────────────────────────────────
# Parse: mindmap.md → fa
# ─────────────────────────────────────────────────────────────────────────────

_MERMAID_BLOCK = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
_NODE_DECL     = re.compile(r'(\w+)\s*\[\s*"(.+?)"\s*\]', re.DOTALL)
_EDGE          = re.compile(r'(\w+)\s*-->\s*(\w+)')
_MSC_TAG       = re.compile(r'\[MSc\]\s*')
_NUM_PREFIX    = re.compile(r'^(\d+(?:\.\d+)*)\.\s+(.*)$', re.DOTALL)


def _parse_label(raw: str) -> tuple[str, str, bool]:
    """Címke → (num, title, msc). Hibatűrő: ha nincs prefix, num='' és title=raw."""
    msc = bool(_MSC_TAG.search(raw))
    s = _MSC_TAG.sub("", raw).strip()
    s = s.split("<br>")[0].strip()       # csak az első sor a cím
    m = _NUM_PREFIX.match(s)
    if m:
        return m.group(1), m.group(2).strip(), msc
    return "", s, msc


def parse_mindmap(mindmap_path: str | Path) -> NavNode:
    """A mindmap.md első ```mermaid``` blokkjából navigációs fát épít.

    A ROOT mindig a gyökér; ha a forrásban nincs explicit "ROOT" id, az első
    él-nélküli (szülő nélküli) csomópont lesz a gyökér.
    """
    text = Path(mindmap_path).read_text(encoding="utf-8")
    block_m = _MERMAID_BLOCK.search(text)
    block = block_m.group(1) if block_m else text

    # 1) Csomópont-deklarációk (id → címke); az élek céljai is itt jönnek elő.
    nodes: dict[str, NavNode] = {}
    for nid, raw in _NODE_DECL.findall(block):
        if nid not in nodes:
            num, title, msc = _parse_label(raw)
            nodes[nid] = NavNode(id=nid, num=num, title=title, label_raw=raw, msc=msc)

    # 2) Élek (szülő → gyermek). A '-->' utáni '\w+' a node-decl-ből már létezik.
    children_of: dict[str, list[str]] = {}
    has_parent: set[str] = set()
    for parent, child in _EDGE.findall(block):
        if parent not in nodes:
            nodes[parent] = NavNode(id=parent)
        if child not in nodes:
            nodes[child] = NavNode(id=child)
        children_of.setdefault(parent, []).append(child)
        has_parent.add(child)

    # 3) Fa összefűzése (a deklarációs sorrend megőrzésével).
    for parent, kids in children_of.items():
        seen = set()
        for k in kids:
            if k in seen:
                continue
            seen.add(k)
            nodes[k].parent = nodes[parent]
            nodes[parent].children.append(nodes[k])

    # 4) Gyökér: "ROOT", különben az első szülő nélküli.
    if "ROOT" in nodes:
        return nodes["ROOT"]
    for nid, node in nodes.items():
        if nid not in has_parent:
            return node
    # üres fallback
    return NavNode(id="ROOT")


# ─────────────────────────────────────────────────────────────────────────────
# Csomópont-feloldás
# ─────────────────────────────────────────────────────────────────────────────

def find_node(root: NavNode, node_id: str | None) -> NavNode | None:
    if not node_id:
        return None
    for n in root.walk():
        if n.id == node_id:
            return n
    return None


def node_for_number(root: NavNode, number: str | None) -> NavNode | None:
    """Szakasz/alszakasz szám ('2', '2.1') → csomópont."""
    if not number:
        return None
    for n in root.walk():
        if n.num == number:
            return n
    return None


_LEADING_NUM = re.compile(r'^\s*(?:\[MSc\]\s*)?(\d+(?:\.\d+)*)')


def number_from_title(title: str) -> str | None:
    """Dia-cím vezető számának kinyerése: '2.1–2.3. Határok…' → '2.1'."""
    m = _LEADING_NUM.match(title or "")
    return m.group(1) if m else None


# ─────────────────────────────────────────────────────────────────────────────
# Navigációs kép felismerés (a meglévő _prezi_assets képek = navigációs helyek)
# ─────────────────────────────────────────────────────────────────────────────

_NAV_IMG = re.compile(r'_prezi_assets[\\/](navigator|sec(\d+))\.png', re.IGNORECASE)


def is_nav_image(path: str) -> bool:
    """True, ha a képhivatkozás navigációs (navigator.png / secN.png)."""
    return bool(_NAV_IMG.search(path or ""))


def section_from_nav_image(path: str) -> str | None:
    """navigator.png → None (áttekintő); secN.png → 'N' szakaszszám."""
    m = _NAV_IMG.search(path or "")
    if not m:
        return None
    return m.group(2) if m.group(2) else None


# ─────────────────────────────────────────────────────────────────────────────
# Renderelők
# ─────────────────────────────────────────────────────────────────────────────

def _node_text(node: NavNode, show_msc: bool) -> str:
    base = f"{node.num}. {node.title}" if node.num else node.title
    if show_msc and node.msc:
        base += " [MSc]"
    return base


def render_breadcrumb(root: NavNode, current_id: str | None, *,
                      show_msc: bool = True) -> str:
    """DEFAULT nézet: a szülő-lánc fentről le, soronként (többsoros cím).

    Belső/alszakasz diánál a szakasz + alszakasz sor; szakasz-nyitónál egy sor.
    Ha a csomópont nem oldható fel, üres stringet ad (a hívó marad a literál címnél).
    """
    node = find_node(root, current_id)
    if node is None:
        return ""
    chain: list[NavNode] = []
    cur = node
    while cur is not None and cur.id != root.id:
        chain.append(cur)
        cur = cur.parent
    chain.reverse()
    return "\n".join(_node_text(n, show_msc) for n in chain)


def _section_of(node: NavNode | None, root: NavNode) -> NavNode | None:
    """A node depth-1 őse (ROOT közvetlen gyermeke) = a szakasza."""
    cur = node
    while cur is not None and cur.parent is not None:
        if cur.parent.id == root.id:
            return cur
        cur = cur.parent
    return None


def render_toc(root: NavNode, current_id: str | None, *,
               expansion: str = "current-section",
               show_msc: bool = True,
               view: str = "pptx") -> str:
    """MINDMAP nézet: beágyazott sorszámozott TOC szöveg.

    Politika ('current-section'): mind a top-level szakasz látszik; csak az
    aktuális szakasz gyermekei kibontva; a többi összecsukva. Az aktuális
    csomópont kiemelve (▸ a 'pptx' nézetben, **félkövér** a 'md' nézetben,
    <strong>…</strong> a 'html' nézetben).

    A behúzás 2 szóköz/szint — a PPTX `set_tf()` indent→p.level logikája kezeli.
    'html' nézetben: 4 &nbsp;/szint, sorok <br>\\n-nel fűzve.
    """
    node = find_node(root, current_id)
    cur_section = _section_of(node, root) if node else None
    # ha az aktuális maga egy szakasz, az a kibontandó szakasz
    if node is not None and node.parent is not None and node.parent.id == root.id:
        cur_section = node

    lines: list[str] = []

    def emit(n: NavNode, depth: int):
        text = _node_text(n, show_msc)
        is_current = node is not None and n.id == node.id
        if view == "html":
            indent = "&nbsp;" * (4 * depth)
            if is_current:
                line = f"{indent}<strong>{text}</strong>"
            else:
                line = f"{indent}{text}"
        elif view == "md":
            indent = "  " * depth
            line = f"{indent}**{text}**" if is_current else f"{indent}{text}"
        else:  # pptx (default)
            indent = "  " * depth
            line = f"{indent}▸ {text}" if is_current else f"{indent}{text}"
        lines.append(line)

    for section in root.children:
        emit(section, 0)
        expand = (expansion == "full") or (cur_section is not None and section.id == cur_section.id)
        if expand:
            for child in section.children:
                emit(child, 1)

    if view == "html":
        return "<br>\n".join(lines)
    return "\n".join(lines)
