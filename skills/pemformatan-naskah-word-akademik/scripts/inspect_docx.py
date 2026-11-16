"""Inspektor struktur internal berkas .docx (tanpa dependensi eksternal).

Memeriksa pemakaian Heading Styles, field dinamis (TOC, SEQ, REF), section breaks,
format penomoran halaman (Romawi vs Arab), tabel (tblHeader/cantSplit), persamaan
OMML, dan mendeteksi indikasi daftar isi manual atau penanda draf yang tertinggal.
"""
import argparse
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
NS = {"w": W_NS, "m": M_NS}


def w_attr(elem, name):
    return elem.attrib.get(f"{{{W_NS}}}{name}")


def collect_field_instructions(root):
    instructions = []
    for instr in root.findall(".//w:instrText", NS):
        if instr.text:
            instructions.append(instr.text.strip())
    for fld in root.findall(".//w:fldSimple", NS):
        val = w_attr(fld, "instr")
        if val:
            instructions.append(val.strip())
    return instructions


def paragraph_text(p):
    return "".join(t.text for t in p.findall(".//w:t", NS) if t.text)


def inspect_docx(path: Path) -> dict:
    if not path.exists() or path.suffix.lower() != ".docx":
        raise FileNotFoundError(f"Berkas .docx tidak ditemukan: {path}")

    with zipfile.ZipFile(path, "r") as zf:
        names = set(zf.namelist())
        if "word/document.xml" not in names:
            raise ValueError("Berkas bukan dokumen .docx yang valid (word/document.xml tidak ada).")

        doc_root = ET.fromstring(zf.read("word/document.xml"))
        settings_root = ET.fromstring(zf.read("word/settings.xml")) if "word/settings.xml" in names else None
        header_footer_xmls = [
            ET.fromstring(zf.read(n))
            for n in sorted(names)
            if re.match(r"word/(header|footer)\d*\.xml$", n)
        ]

    paragraphs = doc_root.findall(".//w:body/w:p", NS)
    all_paragraphs = doc_root.findall(".//w:p", NS)
    tables = doc_root.findall(".//w:tbl", NS)
    omath_count = len(doc_root.findall(".//m:oMath", NS))

    heading_counts = {}
    manual_dot_leaders = []
    error_texts = []
    draf_markers = []
    consec_empty_paras = 0
    max_empty_streak = 0
    marker_re = re.compile(r"\[(VERIFIKASI|BUTUH DATA|SITASI|CEK MANUSIA)\]")
    err_re = re.compile(r"(Error!\s*Reference source not found|#REF!|Error!\s*Bookmark not defined)", re.I)

    for idx, p in enumerate(all_paragraphs, 1):
        ppr = p.find("w:pPr", NS)
        style_el = ppr.find("w:pStyle", NS) if ppr is not None else None
        style_val = w_attr(style_el, "val") if style_el is not None else None
        if style_val and re.match(r"^(Heading\s*[1-6]|Bab|Judul)", style_val, re.I):
            heading_counts[style_val] = heading_counts.get(style_val, 0) + 1

        txt = paragraph_text(p).strip()
        if not txt and not p.findall(".//w:drawing", NS) and not p.findall(".//m:oMath", NS):
            consec_empty_paras += 1
            max_empty_streak = max(max_empty_streak, consec_empty_paras)
        else:
            consec_empty_paras = 0

        if re.search(r"\.{5,}\s*\d*\s*$", txt):
            manual_dot_leaders.append({"paragraph": idx, "preview": txt[:90]})
        if err_re.search(txt):
            error_texts.append({"paragraph": idx, "preview": txt[:120]})
        for m in marker_re.findall(txt):
            draf_markers.append({"paragraph": idx, "marker": m, "preview": txt[:90]})

    # Fields across document + headers/footers
    doc_instrs = collect_field_instructions(doc_root)
    hf_instrs = []
    for hf in header_footer_xmls:
        hf_instrs.extend(collect_field_instructions(hf))

    toc_fields = [x for x in doc_instrs if re.match(r"^TOC\b", x, re.I)]
    seq_fields = [x for x in doc_instrs if re.match(r"^SEQ\b", x, re.I)]
    ref_fields = [x for x in doc_instrs if re.match(r"^REF\b", x, re.I)]
    page_fields = [x for x in hf_instrs + doc_instrs if re.match(r"^PAGE\b", x, re.I)]

    # Sections
    sections = []
    for i, sect in enumerate(doc_root.findall(".//w:sectPr", NS), 1):
        pg_sz = sect.find("w:pgSz", NS)
        pg_num = sect.find("w:pgNumType", NS)
        title_pg = sect.find("w:titlePg", NS)
        orient = w_attr(pg_sz, "orient") if pg_sz is not None else "portrait"
        num_fmt = w_attr(pg_num, "fmt") if pg_num is not None else "inherit"
        num_start = w_attr(pg_num, "start") if pg_num is not None else None
        sections.append({
            "section": i,
            "orientation": orient or "portrait",
            "page_number_format": num_fmt,
            "page_number_start": num_start,
            "different_first_page": title_pg is not None,
        })

    # Tables check
    tables_with_repeat_header = 0
    tables_with_cant_split = 0
    for tbl in tables:
        if tbl.find(".//w:trPr/w:tblHeader", NS) is not None:
            tables_with_repeat_header += 1
        if tbl.find(".//w:trPr/w:cantSplit", NS) is not None:
            tables_with_cant_split += 1

    update_fields_on_open = False
    if settings_root is not None:
        uf = settings_root.find(".//w:updateFields", NS)
        if uf is not None and w_attr(uf, "val") in ("true", "1", None):
            update_fields_on_open = True

    warnings = []
    if not heading_counts:
        warnings.append("Tidak ditemukan style Heading (mis. Heading1/Heading2); Daftar Isi otomatis berisiko kosong.")
    if not toc_fields and manual_dot_leaders:
        warnings.append("Terdeteksi titik-titik penuntun manual tanpa TOC field; gunakan Daftar Isi otomatis.")
    if manual_dot_leaders and toc_fields:
        warnings.append("Sebagian paragraf memiliki titik penuntun manual (.....); pastikan tidak berasal dari daftar ketikan manual.")
    if error_texts:
        warnings.append(f"Ditemukan {len(error_texts)} pesan error field/rujukan silang di dalam dokumen.")
    if draf_markers:
        warnings.append(f"Masih ada {len(draf_markers)} penanda draf ([VERIFIKASI]/[BUTUH DATA]/[SITASI]/[CEK MANUSIA]).")
    if tables and tables_with_repeat_header == 0:
        warnings.append("Belum ada tabel yang memakai Repeat Header Rows (tblHeader).")
    if (toc_fields or seq_fields or ref_fields) and not update_fields_on_open:
        warnings.append("Dokumen memiliki field dinamis tetapi <w:updateFields w:val=\"true\"/> belum aktif di settings.xml.")
    if max_empty_streak >= 3:
        warnings.append(f"Ditemukan {max_empty_streak} paragraf kosong berurutan; hindari memakai Enter berulang sebagai pemisah halaman.")

    return {
        "file": str(path),
        "body_paragraphs": len(paragraphs),
        "tables_total": len(tables),
        "tables_with_repeat_header": tables_with_repeat_header,
        "tables_with_cant_split": tables_with_cant_split,
        "omml_equations": omath_count,
        "heading_styles_used": heading_counts,
        "fields": {
            "toc_count": len(toc_fields),
            "toc_instructions": toc_fields[:10],
            "seq_caption_count": len(seq_fields),
            "ref_crossref_count": len(ref_fields),
            "page_number_fields": len(page_fields),
        },
        "sections": sections,
        "update_fields_on_open": update_fields_on_open,
        "manual_dot_leader_hits": manual_dot_leaders[:10],
        "field_error_hits": error_texts[:10],
        "draft_markers_remaining": draf_markers[:15],
        "max_consecutive_empty_paragraphs": max_empty_streak,
        "warnings": warnings,
    }


def main():
    parser = argparse.ArgumentParser(description="Audit struktur akademik berkas .docx tanpa Word/LibreOffice.")
    parser.add_argument("docx_path", type=Path, help="Jalur berkas .docx yang akan diperiksa.")
    args = parser.parse_args()
    report = inspect_docx(args.docx_path)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["field_error_hits"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
