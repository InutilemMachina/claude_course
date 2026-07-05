"""_omml.py — LaTeX → natív PPTX-egyenlet (OMML) beillesztés.

A `$...$` szövegközi és `$$...$$` saját-soros képleteket **natív** PowerPoint-
egyenletté alakítja (nem kép!), így az inline képlet a szövegben folyik, a block
képlet saját, középre zárt bekezdés. A lánc:

    LaTeX --latex2mathml--> MathML --MML2OMML.XSL(lxml XSLT)--> OMML(m:oMath)

majd a DrawingML text-body-ba `mc:AlternateContent/a14:m` wrapperben ágyazva.

Ha a lánc nem elérhető (nincs latex2mathml vagy XSLT), `available()` False —
a hívó ilyenkor szöveges/kép fallbackre vált.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from lxml import etree

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
A14 = "http://schemas.microsoft.com/office/drawing/2010/main"

_XSLT = None
_L2M = None
_READY = None


def _find_xslt_path() -> Path | None:
    env = os.environ.get("MML2OMML_XSL")
    if env and Path(env).exists():
        return Path(env)
    candidates = [
        r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL",
        r"C:\Program Files (x86)\Microsoft Office\root\Office16\MML2OMML.XSL",
        r"C:\Program Files\Microsoft Office\Office16\MML2OMML.XSL",
    ]
    for c in candidates:
        if Path(c).exists():
            return Path(c)
    for root in (r"C:\Program Files\Microsoft Office", r"C:\Program Files (x86)\Microsoft Office"):
        p = Path(root)
        if p.exists():
            hits = list(p.rglob("MML2OMML.XSL"))
            if hits:
                return hits[0]
    return None


def available() -> bool:
    """Lazy inicializálás; True, ha a teljes lánc használható."""
    global _XSLT, _L2M, _READY
    if _READY is not None:
        return _READY
    try:
        import latex2mathml.converter as conv
        xpath = _find_xslt_path()
        if xpath is None:
            _READY = False
            return False
        _XSLT = etree.XSLT(etree.parse(str(xpath)))
        _L2M = conv
        _READY = True
    except Exception:
        _READY = False
    return _READY


def why_unavailable() -> str:
    """Diagnosztika: MIÉRT nem elérhető az OMML-lánc.

    Üres string, ha a lánc rendben; egyébként a hiányzó láncszemek felsorolása,
    hogy a hívó explicit (nem néma) figyelmeztetést tudjon adni.
    """
    if available():
        return ""
    reasons = []
    try:
        import latex2mathml.converter  # noqa: F401
    except Exception as e:
        reasons.append(f"latex2mathml import hiba ({e})")
    if _find_xslt_path() is None:
        reasons.append(
            "MML2OMML.XSL nem található (MS Office XSL; add meg a MML2OMML_XSL env-változót)"
        )
    return "; ".join(reasons) or "ismeretlen ok (lásd lxml/latex2mathml telepítés)"


def _esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tex_to_omath(tex: str) -> str | None:
    """LaTeX → <m:oMath> XML-string (vagy None hiba esetén)."""
    if not available():
        return None
    try:
        mml = _L2M.convert(tex.strip())
        omml = _XSLT(etree.fromstring(mml.encode())).getroot()
        return etree.tostring(omml, encoding="unicode")
    except Exception:
        return None


def _amc(inner_xml: str, fallback_text: str) -> str:
    """mc:AlternateContent/a14:m wrapper, sima-szöveg fallbackkel."""
    return (
        f'<mc:AlternateContent xmlns:mc="{MC}">'
        f'<mc:Choice xmlns:a14="{A14}" Requires="a14"><a14:m>{inner_xml}</a14:m></mc:Choice>'
        f'<mc:Fallback><a:r xmlns:a="{A}"><a:t>{_esc(fallback_text)}</a:t></a:r></mc:Fallback>'
        f'</mc:AlternateContent>'
    )


_INLINE = re.compile(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)")   # $...$ (nem $$)


def has_inline(line: str) -> bool:
    return bool(_INLINE.search(line))


def _run(text: str) -> str:
    return f'<a:r><a:t>{_esc(text)}</a:t></a:r>' if text else ""


def inline_paragraph_xml(line: str, level: int = 0) -> str | None:
    """Szöveg `$...$` képletekkel → <a:p> XML (run-ok + inline m:oMath).
    None, ha nincs inline képlet vagy a lánc nem elérhető."""
    if not available() or not has_inline(line):
        return None
    parts = []
    pos = 0
    for m in _INLINE.finditer(line):
        parts.append(_run(line[pos:m.start()]))
        om = tex_to_omath(m.group(1))
        parts.append(_amc(om, m.group(1)) if om else _run(f"${m.group(1)}$"))
        pos = m.end()
    parts.append(_run(line[pos:]))
    ppr = f'<a:pPr lvl="{level}"/>' if level else ''
    return f'<a:p xmlns:a="{A}">{ppr}{"".join(parts)}</a:p>'


def block_paragraph_xml(tex: str, align: str = "ctr") -> str | None:
    """Saját-soros block egyenlet → középre zárt <a:p>(m:oMathPara)."""
    om = tex_to_omath(tex)
    if om is None:
        return None
    para = f'<m:oMathPara xmlns:m="{M}">{om}</m:oMathPara>'
    return f'<a:p xmlns:a="{A}"><a:pPr algn="{align}"/>{_amc(para, tex)}</a:p>'


def plain_paragraph_xml(line: str, level: int = 0) -> str:
    """Sima szöveg-bekezdés (md lista-jelölő levágva); math nem elérhető esetén is."""
    txt = _esc(re.sub(r"^\s*[-*•]\s+", "", line).strip())
    ppr = f'<a:pPr lvl="{level}"/>' if level else ''
    return f'<a:p xmlns:a="{A}">{ppr}<a:r><a:t>{txt}</a:t></a:r></a:p>'


def append_paragraph(text_frame, p_xml: str):
    """Nyers <a:p> XML hozzáfűzése a text-frame txBody-jához."""
    text_frame._txBody.append(etree.fromstring(p_xml.encode()))


def drop_leading_empty(text_frame):
    """A text_frame.clear() utáni üres első <a:p> eltávolítása (ha van más is)."""
    body = text_frame._txBody
    ps = body.findall(f"{{{A}}}p")
    if len(ps) > 1:
        first = ps[0]
        if first.find(f"{{{A}}}r") is None and first.find(f".//{{{M}}}oMathPara") is None:
            body.remove(first)
