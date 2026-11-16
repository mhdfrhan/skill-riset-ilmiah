"""Audit silang antara kunci pustaka (.bib) atau daftar pustaka dan sitasi di naskah teks/Markdown."""
import argparse
import json
import re
import sys
from pathlib import Path


def parse_bib_entries(bib_text: str) -> dict:
    entries = {}
    pattern = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.I)
    matches = list(pattern.finditer(bib_text))
    for i, m in enumerate(matches):
        entry_type = m.group(1).lower()
        key = m.group(2).strip()
        if entry_type in ("comment", "preamble", "string"):
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(bib_text)
        block = bib_text[start:end]
        has_doi = bool(re.search(r"\bdoi\s*=", block, re.I))
        has_year = bool(re.search(r"\b(?:year|date)\s*=", block, re.I))
        has_title = bool(re.search(r"\btitle\s*=", block, re.I))
        entries[key] = {"type": entry_type, "has_doi": has_doi, "has_year": has_year, "has_title": has_title}
    return entries


def extract_pandoc_citations(text: str) -> set:
    # Matches [@key], [@a; @b], or standalone @key (avoiding email addresses)
    return set(re.findall(r"(?<![A-Za-z0-9_.+-])@([A-Za-z0-9_][A-Za-z0-9_:.#$%&\-+?<>~/]*)", text))


def extract_numeric_citations(text: str) -> list:
    nums = []
    for grp in re.findall(r"\[(\d+(?:\s*[-,]\s*\d+)*)\]", text):
        for part in re.split(r"\s*,\s*", grp):
            if "-" in part:
                a, b = [int(x.strip()) for x in part.split("-", 1)]
                if a <= b and (b - a) <= 50:
                    nums.extend(range(a, b + 1))
            elif part.strip().isdigit():
                nums.append(int(part.strip()))
    return nums


def extract_authoryear_citations(text: str) -> list:
    return re.findall(r"\(([A-Z][A-Za-zÀ-ÖØ-öø-ÿ'`-]+(?:\s+(?:et al\.|dkk\.|&|dan)\s*[A-Z]?[A-Za-zÀ-ÖØ-öø-ÿ'`-]*)*,\s*(?:19|20)\d{2}[a-z]?(?:,\s*(?:hlm\.|p\.|pp\.)\s*\d+(?:-\d+)?)?)\)", text)


def main():
    parser = argparse.ArgumentParser(description="Audit silang sitasi naskah teks/Markdown dan berkas BibTeX (.bib).")
    parser.add_argument("--text", type=Path, required=True, help="Berkas naskah .md atau .txt")
    parser.add_argument("--bib", type=Path, help="Opsional: berkas .bib sumber referensi")
    args = parser.parse_args()

    if not args.text.exists():
        print(f"Berkas teks tidak ditemukan: {args.text}", file=sys.stderr)
        sys.exit(1)

    text = args.text.read_text(encoding="utf-8")
    result = {
        "text_file": str(args.text),
        "numeric_citations_found": sorted(set(extract_numeric_citations(text))),
        "author_year_samples": extract_authoryear_citations(text)[:30],
        "mixed_etal_and_dkk": ("et al." in text and "dkk." in text),
    }

    if args.bib:
        if not args.bib.exists():
            print(f"Berkas .bib tidak ditemukan: {args.bib}", file=sys.stderr)
            sys.exit(1)
        bib_entries = parse_bib_entries(args.bib.read_text(encoding="utf-8"))
        cited_keys = extract_pandoc_citations(text)
        orphan = sorted(cited_keys - set(bib_entries.keys()))
        uncited = sorted(set(bib_entries.keys()) - cited_keys)
        missing_doi = sorted(k for k, v in bib_entries.items() if not v["has_doi"] and v["type"] in ("article", "inproceedings"))
        missing_meta = sorted(k for k, v in bib_entries.items() if not (v["has_year"] and v["has_title"]))
        result["bib_audit"] = {
            "bib_file": str(args.bib),
            "total_bib_entries": len(bib_entries),
            "pandoc_citekeys_in_text": len(cited_keys),
            "orphan_citekeys_missing_in_bib": orphan,
            "uncited_bib_entries": uncited,
            "articles_without_doi": missing_doi,
            "entries_missing_year_or_title": missing_meta,
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
