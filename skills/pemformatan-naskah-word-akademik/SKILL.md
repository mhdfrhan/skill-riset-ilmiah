---
name: pemformatan-naskah-word-akademik
description: Membantu memformat dan mengaudit dokumen Microsoft Word (.docx) akademik secara umum, meliputi Section Breaks, penomoran halaman Romawi dan Arab, Heading Styles, Daftar Isi otomatis, Caption serta Daftar Gambar/Tabel, rujukan silang, persamaan OMML, daftar pustaka, pembaruan field, dan inspeksi visual PDF. Gunakan saat menyusun, mengotomatiskan, atau merapikan format .docx skripsi, tesis, laporan riset, maupun artikel jurnal.
---

# 10 — Pemformatan Naskah Word Akademik

**Tujuan:** Menghasilkan berkas Microsoft Word (`.docx`) akademik yang patuh aturan tata letak kampus atau templat jurnal, seluruh elemen dinamisnya terhubung lewat *Word fields* asli (bukan ketikan manual yang gampang berantakan saat ada revisi halaman), dan terverifikasi bersih secara visual setelah ekspor ke PDF.

## Alur Kerja Inti

1. **Pisahkan dokumen dengan `Section Breaks` sebelum menomori halaman:**
   - Bagi dokumen menjadi minimal tiga zona lewat *Section Break (Next Page)*: **Sampul & pengesahan** (tanpa nomor halaman), **Bagian Awal** (kata pengantar, daftar isi/tabel/gambar dengan angka Romawi kecil `i, ii, iii`), dan **Bagian Isi & Pustaka** (angka Arab `1, 2, 3`).
   - Matikan tautan antarbagian (*Link to Previous = false*) sebelum mengubah format nomor halaman atau mengganti posisi nomor pada halaman awal tiap bab (*Different First Page*).
   - Jika ada tabel atau gambar lebar, bungkus dengan *Section Break* khusus berorientasi *Landscape* agar orientasi halaman sebelum dan sesudahnya tidak berubah.
2. **Bangun struktur judul dengan *Styles*, bukan format manual:**
   - Terapkan gaya bawaan Word (`Heading 1`, `Heading 2`, `Heading 3`, dst.) atau gaya templat jurnal secara konsisten; aktifkan *Keep with Next* pada setiap judul bab/subbab agar judul tidak tertinggal sendirian di dasar halaman (*widow/orphan*).
   - Gunakan **Daftar Isi otomatis (`TOC` field)** agar nomor halaman selalu dapat diperbarui otomatis (`F9`); jangan mengetik titik-titik penuntun (`......`) secara manual.
3. **Gunakan `Caption` (`SEQ` field), `TOF`/`TOT`, dan rujukan silang (`REF`):**
   - Letakkan **judul tabel di atas tabel** (beri penanda baris kepala berulang/*Repeat Header Rows* agar kepala tabel otomatis muncul kembali bila tabel melintasi pergantian halaman, serta catatan/sumber di bawah tabel).
   - Letakkan **judul gambar di bawah gambar** dengan kontras dan ketajaman memadai.
   - Bentuk nomor `Gambar X.Y` dan `Tabel X.Y` lewat *Caption* (`SEQ` field + `STYLEREF` bab bila memakai nomor per bab) agar **Daftar Gambar (`TOF`)**, **Daftar Tabel (`TOT`)**, dan **rujukan silang di dalam teks (`REF`)** ikut bergeser otomatis setiap kali ada tabel atau gambar baru disisipkan.
4. **Rapikan persamaan matematika dan daftar pustaka terhubung:**
   - Tulis rumus matematika menggunakan **Equation Editor / OMML** (atau konversi LaTeX ke OMML lewat Pandoc), jangan menempel gambar rumus buram; atur nomor persamaan `(1)`, `(2)` rata kanan secara konsisten.
   - Hubungkan sitasi dan Daftar Pustaka lewat pengelola referensi (Zotero, Mendeley, EndNote, Pandoc `--citeproc` dengan berkas `.bib`/`.csl`, atau sumber Word) serta atur *hanging indent* (`1,27 cm / 0,5 inci`) pada daftar pustaka.
5. **Perbarui seluruh *field* dan audit visual PDF sebelum finalisasi:**
   - Dokumen `.docx` hasil skrip (Python, Node, atau Pandoc) tidak otomatis menghitung ulang nomor halaman pada `TOC`/`TOF`/`TOT`. Wajib aktifkan pembaruan *field* saat dibuka atau jalankan pembaruan lewat Word/LibreOffice, lalu ekspor ke PDF dan periksa visual halaman demi halaman.
   - Untuk memeriksa kesehatan struktur internal berkas secara cepat lintas platform, jalankan skrip bantu: `python scripts/inspect_docx.py <berkas.docx>`.

## WAJIB

- Pastikan semua aturan margin, jenis dan ukuran huruf, spasi baris, serta letak nomor halaman mengikuti pedoman institusi atau templat jurnal tujuan pengguna (tandai `[CEK MANUSIA]` bila pedoman target belum disebutkan).
- Pastikan seluruh rujukan gambar, tabel, halaman, dan entri Daftar Isi terhubung ke *field* atau telah diperbarui terhadap hasil ekspor PDF final tanpa menyisakan pesan galat seperti `Error! Reference source not found` atau `#REF!`.
- Pastikan tidak ada penanda draf (`[VERIFIKASI]`, `[BUTUH DATA]`, `[SITASI]`, `[CEK MANUSIA]`) yang tertinggal saat menandai dokumen sebagai naskah siap kumpul.
- Lakukan pemeriksaan cadangan sebelum mengubah berkas `.docx` asli pengguna, terutama bila dokumen berisi *field* Zotero/Mendeley aktif agar tautan sitasinya tidak rusak (*unlinked*) secara tidak sengaja.

## BOLEH

- Membantu membuat, merapikan, atau mengaudit struktur `.docx` menggunakan `python-docx`, OOXML (`word/document.xml`, `word/settings.xml`), Pandoc (`--reference-doc`, `--citeproc`), maupun otomasi Word COM (Windows) atau LibreOffice.
- Membantu merancang gaya tabel akademik bersih, memisahkan *Section Break* untuk halaman *Landscape* atau nomor Romawi/Arab, serta menyusun skrip pembaruan otomatis seluruh *Daftar Isi*, *Daftar Gambar*, dan *Daftar Tabel*.
- Menjalankan skrip [inspect_docx.py](scripts/inspect_docx.py) untuk menemukan kekurangan struktural (heading palsu, daftar isi manual, tabel tanpa *repeat header*, field rusak) sebelum pengiriman dokumen.

## DILARANG

- Mengetik manual daftar isi dengan spasi/titik-titik penuntun (`.....`), mengetik nomor halaman secara statis, atau mengetik nomor `Gambar`/`Tabel` secara manual di dalam daftar depan.
- Menumpuk *Enter* kosong berulang-ulang sebagai pengganti *Page Break* atau *Section Break* (yang membuat tata letak rusak saat berpindah komputer atau versi Word).
- Menghancurkan atau menimpa *field code* Zotero/Mendeley/EndNote atau XML sitasi milik peneliti tanpa persetujuan eksplisit pengguna.
- Menyatakan format `.docx` "sudah rapi/siap cetak" sebelum *field* diperbarui dan hasil PDF-nya benar-benar dibuka serta diperiksa halamannya.

## Referensi & Alat Bantu

- Resep teknis OOXML, `TOC`/`SEQ`/`STYLEREF`/`REF`, *Section Break*, persamaan OMML, Pandoc CSL, dan pembaruan *field* via Word COM / LibreOffice: [panduan-ooxml-dan-field-word.md](references/panduan-ooxml-dan-field-word.md)
- Skrip audit struktur `.docx` bawaan Python stdlib: [inspect_docx.py](scripts/inspect_docx.py)
