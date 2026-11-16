# Perbandingan Gaya Sitasi dan Manajemen BibTeX/CSL

## 1. Perbandingan Lima Gaya Rujukan Utama

| Gaya | Sitasi dalam Teks | Urutan Daftar Pustaka | Ciri Khas Format Artikel Jurnal |
|---|---|---|---|
| **APA Edisi ke-7** | `(Santoso & Wijaya, 2023)` / `(Santoso et al., 2023)` | Alfabetis nama belakang penulis pertama | Tahun di dalam kurung setelah penulis; hanya huruf awal judul artikel kapital (*sentence case*); nama jurnal miring & berkapital tiap kata penting (*title case*); wajib tautan `https://doi.org/...` tanpa titik di akhir DOI |
| **IEEE** | `[1]`, `[2], [3]`, `[4]–[6]` | Numerik urut kemunculan pertama di teks | Inisial depan sebelum nama belakang (`A. B. Penulis`); judul artikel di dalam tanda kutip `"..."`; nama jurnal miring disingkat baku; mencantumkan `vol.`, `no.`, `pp.`, bulan & tahun, lalu `doi:` |
| **Harvard** | `(Santoso & Wijaya 2023)` atau `(Santoso 2023, hlm. 14)` | Alfabetis nama belakang penulis pertama | Mirip APA tetapi tahun sering tanpa tanda kurung setelah koma/titik tergantung sub-varian kampus, nama jurnal miring |
| **Chicago (Author-Date)** | `(Santoso 2023, 45)` | Alfabetis nama belakang penulis pertama | Penulis pertama dibalik, penulis kedua tidak dibalik; judul artikel diapit tanda kutip; nama jurnal miring diikuti `volume, no. isu (tahun): halaman` |
| **Vancouver** | `(1)` atau superskrip `¹` | Numerik urut kemunculan pertama di teks | Lazim di bidang kedokteran/kesehatan; nama belakang lalu inisial tanpa tanda titik (`Santoso AB.`); singkatan nama jurnal standar PubMed/NLM tanpa huruf miring; format tahun;vol(isu):hlm |

---

## 2. Penulisan Nama Indonesia Tanpa Marga

Pedoman perguruan tinggi di Indonesia berbeda-beda mengenai nama tunggal atau nama dua kata tanpa marga (misal *Budi Santoso*):

- **Ikuti pedoman institusi target terlebih dahulu** (tandai `[CEK MANUSIA]` bila belum ada kepastian):
  1. Sebagian kampus mengadopsi gaya internasional penuh: membalik bagian akhir (`Santoso, B.`).
  2. Sebagian kampus (merujuk EYD / pedoman perpusnas) **tidak membalik** nama tanpa marga (`Budi Santoso`), dan hanya membalik nama yang jelas memiliki marga/keluarga.
- Apa pun aturan yang dipilih, **terapkan konsisten 100% dari awal hingga akhir daftar pustaka**.

---

## 3. Contoh Entri BibTeX (`.bib`) yang Bersih

```bibtex
@article{santoso2024ekg,
  author  = {Santoso, Budi and Lestari, Rina},
  title   = {Evaluation of lightweight image models on 12-lead ECG classification},
  journal = {Journal of Medical Systems},
  year    = {2024},
  volume  = {48},
  number  = {2},
  pages   = {112--124},
  doi     = {10.1007/s10916-024-0000-0}
}

@inproceedings{pratama2023retrieval,
  author    = {Pratama, Andi},
  title     = {Vector retrieval benchmarks in clinical summaries},
  booktitle = {Proceedings of the International Conference on Informatics},
  year      = {2023},
  pages     = {45--52},
  publisher = {IEEE},
  doi       = {10.1109/ICI.2023.00010}
}
```

### Aturan Penulisan `.bib` Agar Tidak Salah Kapitalisasi
- Pandoc/LaTeX secara otomatis mengubah huruf besar di dalam `title` menjadi huruf kecil saat memakai gaya APA (`sentence case`). Bungkus singkatan baku atau nama diri (seperti `{EKG}`, `{PTB-XL}`, `{Indonesia}`, `{COVID-19}`) dengan kurung kurawal `{...}` agar kapitalisasinya tetap terjaga.
- Pisahkan beberapa penulis di `.bib` **hanya dengan kata `and`** (bukan koma atau `&`).

---

## 4. Daftar Periksa Audit 1-Banding-1

- [ ] Setiap kutipan di narasi utama, tabel, dan keterangan gambar memiliki pasangan persis di Daftar Pustaka.
- [ ] Tidak ada entri di Daftar Pustaka yang tertinggal tanpa pernah disebut di teks.
- [ ] Tahun terbit di teks sama persis dengan tahun terbit di Daftar Pustaka.
- [ ] Penulis dengan tahun yang sama dibedakan memakai `2023a`, `2023b` (untuk gaya penulis-tahun).
- [ ] Seluruh DOI mengarah ke halaman terbitan yang sah (`https://doi.org/...`), bukan tebakan atau rusak (`404`).
