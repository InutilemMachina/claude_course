"""
_citations_util.py -- Megosztott citáció-segédfüggvények.

Használja: 10-1_bsc_filter.py, 10-2_pandoc_export.py.
"""

import json
from pathlib import Path


def resolve_week(week_dir: Path, week_arg) -> int:
    """A hét sorszáma CLI argumentumból, vagy a citations.json _meta.week mezőjéből."""
    if week_arg:
        return int(week_arg)
    cit = week_dir / "1_raw_inputs" / "citations.json"
    if cit.exists():
        data = json.loads(cit.read_bytes().decode("utf-8-sig"))
        return data.get("_meta", {}).get("week", 1)
    return 1
