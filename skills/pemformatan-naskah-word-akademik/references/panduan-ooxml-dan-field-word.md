# Panduan Teknis OOXML, Field Word, dan Verifikasi PDF

Dokumen ini menjadi rujukan teknis saat membangun, menyunting, atau mengaudit `.docx` secara terprogram (`python-docx`, manipulasi XML langsung, `docx` JS, Pandoc, atau Word COM).

---

## 1. Struktur XML Inti `.docx` untuk Elemen Akademik

Berkas `.docx` adalah arsip ZIP berisi berkas XML. Bagian yang paling sering disentuh untuk pemformatan akademik:

- `word/document.xml`: isi paragraf, tabel, *section break* (`w:sectPr`), *field code* (`TOC`, `SEQ`, `REF`, `STYLEREF`), dan persamaan (`m:oMath`).
- `word/styles.xml`: definisi `Heading1..Heading4`, `TOC1..TOC3`, `Caption`, font, spasi, dan *keepNext*.
- `word/settings.xml`: tempat mengaktifkan pembaruan *field* otomatis saat berkas dibuka di Word:
  ```xml
  <w:updateFields w:val="true"/>
  ```
- `word/header*.xml` & `word/footer*.xml`: tempat meletakkan *field* `PAGE` serta konfigurasi *Different First Page* (`<w:titlePg/>` di `w:sectPr`).

---

## 2. Daftar Isi Otomatis (`TOC`), Daftar Gambar (`TOF`), dan Daftar Tabel (`TOT`)

1. **Daftar Isi (`TOC`):**
   - Pastikan judul bab/subbab memakai style `Heading 1`..`Heading 3` (atau punya `<w:outlineLvl w:val="0..2"/>`).
   - Sisipkan *complex field* dengan instrumen:
     `TOC \o "1-3" \h \z \u`
     - `\o "1-3"`: merangkum level 1 sampai 3.
     - `\h`: membuat entri bisa diklik (*hyperlink*).
     - `\u`: menggunakan *outline level*.
2. **Caption (`SEQ`) & Penomoran per Bab (`STYLEREF`):**
   - Penomoran menerus (`Gambar 1`, `Gambar 2`): gunakan `{ SEQ Gambar \* ARABIC }` (atau `Figure`, `Table`, `Tabel` sesuai bahasa naskah dan label *Caption* yang dipilih).
   - Penomoran per bab (`Tabel 3.2`): gabungkan dua *field*:
     `{ STYLEREF 1 \s }.{ SEQ Tabel \* ARABIC \s 1 }`
     - `STYLEREF 1 \s` mengambil angka bab dari `Heading 1`.
     - `\s 1` me-reset hitungan `SEQ` setiap berganti `Heading 1`.
3. **Daftar Gambar & Daftar Tabel (`TOF` / `TOT`):**
   - Keduanya memakai instrumen `TOC` dengan sakelar `\c "<NamaLabelCaption>"` dan `\h \z`:
     - Daftar Gambar: `TOC \h \z \c "Gambar"`
     - Daftar Tabel: `TOC \h \z \c "Tabel"`
   - Nama label di `\c "..."` **harus sama persis** (huruf besar-kecil) dengan nama label pada *field* `SEQ`.
4. **Rujukan Silang di Dalam Teks (`REF`):**
   - Bungkus judul/nomor caption target dengan `<w:bookmarkStart w:id="..." w:name="_RefXXXXXX"/> ... <w:bookmarkEnd w:id="..."/>`, lalu panggil di teks dengan:
     `REF _RefXXXXXX \h`
     Jangan mengetik teks mati `seperti pada Tabel 3` bila naskah masih bisa bertambah tabelnya.

---

## 3. Section Break, Penomoran Halaman Romawi/Arab, dan Halaman Landscape

Setiap pergantian jenis nomor halaman atau orientasi halaman memerlukan `<w:sectPr>` di dalam `<w:pPr>` paragraf pemutus bagian:

- **Format Nomor Halaman (`w:pgNumType`):**
  - Bagian awal (Kata Pengantar, Daftar Isi, dll.): `<w:pgNumType w:fmt="lowerRoman" w:start="1"/>` (`i, ii, iii`).
  - Bagian isi (Bab 1 dst.): `<w:pgNumType w:fmt="decimal" w:start="1"/>` (`1, 2, 3`).
- **Memutus sambungan header/footer antarbagian:** saat menambahkan header/footer pada bagian baru via `python-docx`, atur `section.header.is_linked_to_previous = False` dan `section.footer.is_linked_to_previous = False` sebelum menyunting teks atau format nomor.
- **Halaman Awal Bab Berbeda (*Different First Page*):** aktifkan `section.different_first_page_header_footer = True` (`<w:titlePg/>`) agar halaman pembuka bab menaruh nomor di bawah tengah, sedangkan halaman lanjutannya menaruh nomor di kanan atas.
- **Halaman Landscape Terisolasi:** buat *section* baru di awal dan akhir tabel lebar dengan `section.orientation = WD_ORIENT.LANDSCAPE` serta tukar `page_width` dan `page_height`, lalu kembalikan ke `PORTRAIT` di *section* berikutnya.

---

## 4. Tabel Akademik dan Persamaan Matematika

- **Tabel multi-halaman:** selalu pasang `<w:tblHeader/>` pada `<w:trPr>` baris judul kolom teratas agar judul kolom berulang otomatis di halaman berikut, dan pasang `<w:cantSplit/>` pada setiap baris data `<w:trPr>` supaya satu baris tidak terpotong di tengah halaman.
- **Judul tabel & judul gambar:** pasang `keep_with_next = True` pada **paragraf judul tabel** (di atas tabel) dan pada **paragraf gambar itu sendiri** (di atas judul gambar), supaya judul tabel/gambar tidak pernah terpisah ke halaman berbeda dari isi tabel/gambarnya.
- **Persamaan OMML:** bila menulis naskah dari Markdown/LaTeX (`$...$` dan `$$...$$`), konversi lewat Pandoc (`pandoc naskah.md -o out.docx --reference-doc=template.docx`) karena Pandoc otomatis mengubah LaTeX menjadi elemen **OMML (`m:oMath`)** yang dapat disunting langsung dengan *Equation Editor* Microsoft Word.

---

## 5. Sitasi dan Daftar Pustaka Otomatis dengan Pandoc + CSL

Jika menyusun draf dari Markdown + `.bib` ke `.docx`:

```bash
pandoc naskah.md -o naskah.docx ^
  --reference-doc=template_kampus_atau_jurnal.docx ^
  --citeproc ^
  --bibliography=pustaka.bib ^
  --csl=apa.csl
```

- Catatan penting: Pandoc `--citeproc` merender daftar pustaka sebagai paragraf terformat sesuai gaya `.csl`, sedangkan bila dosen pembimbing mewajibkan *field* Zotero/Mendeley aktif di Word, gunakan plugin resmi Zotero/Mendeley atau format `.ris`/`.bib` yang diimpor ke Zotero terlebih dahulu.

---

## 6. Memperbarui Field & Ekspor PDF untuk Inspeksi Visual

### Di Windows (dengan Microsoft Word terpasang — Hasil Paling Akurat)

```powershell
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open("D:\path\naskah.docx")
try {
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    foreach ($tof in $doc.TablesOfFigures) { $tof.Update() }
    $doc.Fields.Update() | Out-Null
    $doc.Save()
    $doc.ExportAsFixedFormat("D:\path\naskah.pdf", 17) # 17 = wdExportFormatPDF
} finally {
    $doc.Close($false)
    $word.Quit()
}
```

### Lintas Platform (Tanpa Microsoft Word — LibreOffice + Poppler/PyMuPDF)

```bash
soffice --headless --convert-to pdf naskah.docx
pdftoppm -png -r 120 naskah.pdf halaman
```

Lalu buka/inspeksi gambar halaman terutama pada: halaman Daftar Isi, Daftar Tabel, Daftar Gambar, batas pergantian bab (*Section Break*), serta setiap tabel atau persamaan panjang.
