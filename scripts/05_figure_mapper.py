"""
09_figure_mapper.py -- Map figure_catalog keywords to Markdown paragraphs.

Reads figure_catalog.json (with VLM keywords) and N_Jegyzet.md,
finds the best-matching paragraph for each figure entry,
writes inserted_after_paragraph + match_score back to the catalog.

Usage:
    python 09_figure_mapper.py <figure_catalog.json> <N_Jegyzet.md> [options]

Options:
    --min-matches  N   Minimum keyword token overlap required (default: 1)
    --dry-run          Print matches without saving catalog
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ---- Stopwords (Hungarian + English) ----

STOPWORDS = {
    "a", "az", "es", "vagy", "hogy", "ez", "egy", "is", "nem",
    "van", "volt", "lesz", "de", "ha", "sem", "mar", "meg", "csak",
    "the", "of", "in", "on", "at", "for", "with", "by", "from",
    "as", "an", "to", "are", "this", "that", "which", "can", "be",
    "it", "its", "was", "has", "have", "been", "also", "such",
}


# ---- Text utilities ----

def tokenize(text: str) -> set[str]:
    """Lowercase word tokens, stopword-filtered, min length 2."""
    words = re.findall(r"[a-záéíóöőúüű\w]+",
                       text.lower())
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}


def load_md(path: Path) -> str:
    """Read Markdown, handling BOM and CRLF."""
    return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def is_preserved_block(block: str) -> bool:
    """Return True if block should be excluded from paragraph matching."""
    first_line = block.lstrip().split("\n")[0]
    if (
        first_line.startswith("#") or
        first_line.startswith("![") or
        first_line.startswith("<!--") or
        first_line.startswith(">") or
        first_line.startswith("---") or
        first_line.startswith("{") or   # YAML-like
        not first_line.strip()
    ):
        return True
    # Exclude ToC-like blocks: blocks dominated by markdown link-list items "- [..."
    link_lines = sum(1 for l in block.splitlines() if re.match(r'\s*-\s+\[', l))
    total_lines = len([l for l in block.splitlines() if l.strip()])
    if total_lines > 0 and link_lines / total_lines > 0.5:
        return True
    return False


def extract_paragraphs(md_text: str) -> list[str]:
    """
    Split Markdown into text paragraphs for keyword matching.
    Excludes: headers, images, comments, blockquotes, HR, YAML.
    """
    blocks = md_text.split("\n\n")
    paragraphs = []
    for block in blocks:
        block = block.strip()
        if block and not is_preserved_block(block):
            paragraphs.append(block)
    return paragraphs


# ---- Core matching ----

def keywords_to_tokens(keywords: list[str]) -> set[str]:
    """Expand keyword phrases into individual tokens."""
    tokens: set[str] = set()
    for kw in keywords:
        tokens.update(tokenize(kw))
    return tokens


def match_figure_to_paragraphs(
    kw_tokens: set[str],
    para_tokens: list[set[str]],
) -> tuple[int, int]:
    """
    Find paragraph index with highest keyword overlap.
    Returns (best_idx, best_score). best_idx = -1 if no match.
    """
    best_idx, best_score = -1, 0
    for idx, p_tokens in enumerate(para_tokens):
        score = len(kw_tokens & p_tokens)
        if score > best_score:
            best_score, best_idx = score, idx
    return best_idx, best_score


# ---- Main ----

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Map figure_catalog keywords to Markdown paragraphs."
    )
    parser.add_argument("catalog", help="Path to figure_catalog.json")
    parser.add_argument("markdown", help="Path to N_Jegyzet.md")
    parser.add_argument(
        "--min-matches", type=int, default=1,
        help="Minimum keyword token overlap to accept a match (default: 1)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print matches but do not save the updated catalog"
    )
    args = parser.parse_args()

    catalog_path = Path(args.catalog)
    md_path = Path(args.markdown)

    if not catalog_path.exists():
        sys.exit(f"[Error] Catalog not found: {catalog_path}")
    if not md_path.exists():
        sys.exit(f"[Error] Markdown not found: {md_path}")

    # Load inputs
    catalog: dict = json.loads(catalog_path.read_text(encoding="utf-8"))
    md_text = load_md(md_path)

    # Sanity check: need at least some entries with keywords (vlm_done nem kötelező)
    # Keywords jöhetnek: (1) 03_util_figure_catalog.py --vlm, vagy (2) 03-1_qfig_parser.py (Qfig)
    vlm_done_count = sum(1 for e in catalog.values() if e.get("vlm_done"))
    has_keywords   = sum(1 for e in catalog.values() if e.get("keywords"))
    if has_keywords == 0:
        print("[Warning] No entries with keywords. Run either:")
        print("  03_util_figure_catalog.py --vlm  (Claude Vision API)")
        print("  04_nlm_dfs_queries.py --qfig + 03-1_qfig_parser.py  (NLM Qfig, free)")
        sys.exit(0)
    if vlm_done_count == 0:
        print(f"[Info] vlm_done=False everywhere, de {has_keywords} bejegyzésnek van keywords (Qfig alapú) -- folytatom.")

    print(f"[09_figure_mapper] Catalog: {len(catalog)} entries, "
          f"{vlm_done_count} VLM done, {has_keywords} with keywords")

    # Extract paragraphs + pre-tokenize
    paragraphs = extract_paragraphs(md_text)
    para_tokens = [tokenize(p) for p in paragraphs]
    print(f"[09_figure_mapper] Markdown: {len(paragraphs)} matchable paragraphs")

    # Match each figure entry
    matched = 0
    skipped_no_kw = 0
    skipped_low_score = 0

    for key, entry in catalog.items():
        keywords = entry.get("keywords", [])
        if not keywords:
            skipped_no_kw += 1
            continue

        kw_tokens = keywords_to_tokens(keywords)
        best_idx, best_score = match_figure_to_paragraphs(kw_tokens, para_tokens)

        if best_score >= args.min_matches and best_idx >= 0:
            entry["inserted_after_paragraph"] = best_idx
            entry["match_score"] = best_score
            matched += 1
            if args.dry_run:
                preview = paragraphs[best_idx][:80].replace("\n", " ")
                print(
                    f"  MATCH  {key}: score={best_score}, "
                    f"para[{best_idx}]: '{preview}...'"
                )
        else:
            entry["inserted_after_paragraph"] = None
            entry["match_score"] = best_score
            skipped_low_score += 1
            if args.dry_run:
                print(f"  NOMATCH {key}: score={best_score} < {args.min_matches}")

    print(
        f"[09_figure_mapper] Results: {matched} matched, "
        f"{skipped_no_kw} no-keywords, {skipped_low_score} below threshold"
    )

    # Save updated catalog
    if not args.dry_run:
        catalog_path.write_text(
            json.dumps(catalog, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"[09_figure_mapper] Saved: {catalog_path}")
    else:
        print("[09_figure_mapper] Dry-run: catalog NOT saved.")


if __name__ == "__main__":
    main()
