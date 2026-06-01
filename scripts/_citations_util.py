"""
_citations_util.py -- Shared citation utilities

Shared by 04_nlm_dfs_queries.py and 07_citations_renumber.py.
"""

import json
from pathlib import Path


def load_seed(seed_path: Path) -> dict:
    """Load citations_seed.json (UTF-8-sig safe)."""
    return json.loads(seed_path.read_bytes().decode("utf-8-sig"))


def parse_nlm_citations(path: Path) -> dict:
    """Extract citations dict {local_str: uuid} from nlm_qN_raw.txt.

    Returns empty dict if file is malformed or citations field is absent.
    """
    try:
        raw = path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
        obj = json.loads(raw)
        val = obj.get("value", obj)
        return val.get("citations", {})
    except Exception:
        return {}


def build_citations_json(seed: dict, raw_dir: Path) -> dict:
    """Build citations.json from seed + any new UUIDs found in nlm_q*_raw.txt.

    Schema: same as citations_seed.json — int-string keys ("1", "2", ...).
    New UUIDs not in seed get a stub entry with note="???".
    """
    result: dict = {}
    uuid_to_key: dict = {}

    for k, v in seed.items():
        if k.startswith("_"):
            continue
        if isinstance(v, dict) and "nlm_uuid" in v:
            result[k] = dict(v)
            uuid_to_key[v["nlm_uuid"]] = k

    next_key = max((int(k) for k in result), default=0) + 1

    for raw_file in sorted(raw_dir.glob("nlm_q*_raw.txt")):
        citations = parse_nlm_citations(raw_file)
        for uuid in citations.values():
            if uuid and uuid not in uuid_to_key:
                key = str(next_key)
                result[key] = {"nlm_uuid": uuid, "note": "???"}
                uuid_to_key[uuid] = key
                next_key += 1

    return result
