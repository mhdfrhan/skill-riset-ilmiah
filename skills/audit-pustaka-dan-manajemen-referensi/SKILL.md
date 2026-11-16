---
name: audit-pustaka-dan-manajemen-referensi
description: Membantu mengelola data pustaka terstruktur (BibTeX, RIS, CSL, Zotero/Mendeley), menerapkan format daftar pustaka lintas gaya (APA, IEEE, Chicago, Harvard, Vancouver), serta mengaudit kecocokan satu banding satu antara sitasi di teks dan daftar pustaka. Gunakan saat merapikan format daftar pustaka atau memeriksa konsistensi sitasi naskah.
---

# 11 — Audit Pustaka dan Manajemen Referensi

**Tujuan:** Memastikan seluruh sitasi di dalam teks dan entri pada Daftar Pustaka memakai satu gaya format secara konsisten, berpadanan satu banding satu tanpa rujukan yatim atau pustaka menganggur, dan memiliki metadata lengkap yang dapat ditelusuri.

*(Catatan: Untuk etika pengutipan, pembedaan kutipan langsung vs parafrase etis, dan pencegahan plagiarisme, gunakan bersama skill `sitasi-dan-integritas-akademik`.)*

## Alur Kerja Inti

1. **Kunci satu gaya rujukan sesuai pedoman tujuan:**
   - Pilih salah satu gaya resmi (misalnya **APA 7th**, **IEEE**, **Harvard**, **Chicago Author-Date/Notes**, atau **Vancouver**) sesuai pedoman kampus atau *Author Guidelines* jurnal.
   - Samakan bahasa penyambung di seluruh naskah: gunakan **`dkk.`** hanya jika pedoman berbahasa Indonesia mensyaratkannya atau **`et al.`** secara konsisten bila mengikuti standar internasional; jangan mencampur keduanya dalam satu dokumen.
   - Perhatikan aturan penulisan nama pengarang Indonesia tanpa nama keluarga (sesuaikan pedoman institusi apakah dibalik pada kata akhir atau tetap utuh tanpa pembalikan saat mengurutkan abjad daftar pustaka).
2. **Kelola sumber dalam format terstruktur sebelum menempel ke naskah:**
   - Simpan data rujukan di pengelola pustaka (Zotero, Mendeley, EndNote) atau berkas terstruktur (`.bib` BibTeX, `.ris`, CSL-JSON) dari tautan/DOI asli agar judul, tahun, volume, nomor, halaman, dan DOI tidak salah ketik.
   - Saat mengonversi draf ke Word (`.docx`), pertahankan *field* pengelola referensi bila disyaratkan pembimbing, atau gunakan `pandoc --citeproc --bibliography=pustaka.bib --csl=gaya.csl` agar penomoran/pengurutan terbentuk otomatis.
   - Terapkan format paragraf standar daftar pustaka: jarak antar-entri jelas serta **indentasi menggantung (*hanging indent* `1,27 cm / 0,5 inci`)** untuk gaya penulis-tahun maupun jarak nomor rata kiri untuk gaya bernomor.
3. **Jalankan audit silang 5 lapis sebelum pengumpulan:**
   - **Sitasi yatim (*orphan citations*):** setiap kutipan di teks (termasuk di catatan tabel/gambar) wajib punya entri di Daftar Pustaka.
   - **Pustaka tak terpakai (*uncited references*):** entri di Daftar Pustaka yang tidak pernah dikutip di teks harus dihapus atau dikutip pada tempatnya.
   - **Kecocokan tahun, ejaan nama, dan urutan nomor:** pastikan tahun di teks sama persis dengan tahun di Daftar Pustaka (khusus gaya bernomor seperti IEEE/Vancouver, cek apakah `[1]`, `[2]`, `[3]` berurutan kemunculan tanpa loncat).
   - **Kelengkapan metadata & DOI:** pastikan setiap artikel jurnal memuat penulis, tahun, judul, nama jurnal lengkap/singkatan baku, volume, isu/nomor, rentang halaman/nomor artikel, serta DOI aktif (`https://doi.org/...`).
   - **Keseragaman tanda baca:** cek penggunaan huruf miring nama jurnal/judul buku, tanda `&` vs `dan`, serta tanda titik di akhir entri sesuai gaya terpilih.
   - Bila memakai berkas `.bib` atau draf teks/Markdown, jalankan alat bantu: `python scripts/audit_bib_citations.py --bib pustaka.bib --text naskah.md`.

## WAJIB

- Pastikan seluruh entri pustaka yang dirapikan maupun dilengkapi berasal dari metadata terverifikasi (berkas `.bib`/`.ris`/PDF asli atau DOI yang dicek nyata), bukan hasil tebakan memori AI.
- Bedakan secara jelas dalam laporan audit antara **temuan pasti** (misalnya sitasi ada di teks tetapi hilang dari Daftar Pustaka), **dugaan ketidakcocokan** (ejaan nama mirip berbeda tahun), dan **metadata yang belum diverifikasi**.
- Sebutkan keterbatasan pemeriksaan bila alat bantu atau teks yang diberikan peneliti tidak memuat bagian lampiran, gambar berisi teks kutipan, atau *field* tersembunyi Zotero/Mendeley.
- Tandai entri tanpa DOI, tanpa halaman/nomor terbitan, atau sumber meragukan dengan `[VERIFIKASI]` dan mintakan keputusan penghapusan pustaka tak terpakai ke peneliti dengan `[CEK MANUSIA]`.

## BOLEH

- Membantu memformat daftar sumber terverifikasi dari pengguna ke gaya APA 7th, IEEE, Harvard, Chicago, Vancouver, atau format `.bib` / `.ris`.
- Membantu melakukan audit silang teks melawan daftar pustaka dan menyusun daftar perbaikan per entri secara rinci.
- Menjalankan skrip [audit_bib_citations.py](scripts/audit_bib_citations.py) untuk menemukan kunci sitasi yatim, entri `.bib` tak terpakai, serta loncatan penomoran numerik.

## DILARANG

- Mengarang nama pengarang, tahun terbit, nomor volume, rentang halaman, atau kode DOI untuk "melengkapi" entri daftar pustaka yang datanya kurang.
- Memalsukan daftar pustaka atau menyisipkan rujukan tambahan hanya agar jumlah daftar pustaka memenuhi batas minimal tertentu.
- Menghapus sitasi atau entri pustaka milik peneliti secara sepihak tanpa daftar laporan dan persetujuan penulis.
- Menyimpulkan sebuah entri valid hanya karena format penulisannya sudah rapi padahal identitas publikasi aslinya belum diverifikasi (`[VERIFIKASI]`).

## Referensi & Alat Bantu

- Matriks perbandingan 5 gaya sitasi utama, pola entri BibTeX, dan alur Pandoc CSL: [perbandingan-gaya-sitasi-dan-bib.md](references/perbandingan-gaya-sitasi-dan-bib.md)
- Skrip audit silang `.bib` dan sitasi draf teks/Markdown: [audit_bib_citations.py](scripts/audit_bib_citations.py)
