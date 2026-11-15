# Skill Riset Ilmiah Lintas Disiplin

Kumpulan *agent skill* berstandar terbuka (`skills/<nama-skill>/SKILL.md`) untuk menjadikan AI sebagai asisten riset yang terstruktur, dengan ketelitian setara kandidat doktoral (S3) dan bahasa yang mudah dipahami mahasiswa semester awal.

## Untuk Siapa

Untuk mahasiswa (S1, S2, S3), dosen, dan peneliti dari jurusan apa pun (sains, kesehatan, sosial, humaniora, hukum, teknik, ekonomi, maupun bisnis) yang sedang menyusun makalah, artikel jurnal, skripsi, tesis, disertasi, atau laporan riset.

## Cara Pakai dalam 3 Langkah

1. **Pasang atau pilih satu skill sesuai tahap riset.** Untuk pengguna AI Agent atau CLI (Antigravity, Claude Code, Codex), salin folder `skills/` ke direktori konfigurasi proyekmu (`.agents/skills/` atau `.claude/skills/`), atau pasang lewat `npx skills add mhdfrhan/skill-riset-ilmiah`. Untuk pengguna chat AI biasa, buka satu file `SKILL.md` yang dibutuhkan lalu tempel isinya di awal percakapan agar instruksi tidak tumpang tindih.
2. **Masukkan bahan nyatamu.** Sertakan pertanyaan penelitian, draf kasar, sumber yang sudah kamu baca, atau data asli. Pakai penanda `[VERIFIKASI]`, `[BUTUH DATA]`, `[SITASI]`, atau `[CEK MANUSIA]` untuk bagian yang masih kosong.
3. **Verifikasi dan pegang kendali.** Gunakan AI untuk mengkritik, membandingkan sumber, dan merapikan tulisan, sementara keputusan ilmiah dan pengecekan fakta ke naskah asli tetap di tanganmu.

## Daftar Skill

| Urutan | Skill | Fokus Utama |
|---|---|---|
| 01 | [perumusan-masalah-dan-celah](skills/perumusan-masalah-dan-celah/SKILL.md) | Menemukan masalah nyata, celah riset, dan pertanyaan terukur |
| 02 | [pencarian-dan-verifikasi-sumber](skills/pencarian-dan-verifikasi-sumber/SKILL.md) | Mencari literatur secara sistematis dan memverifikasi keasliannya |
| 03 | [ekstraksi-dan-sintesis-literatur](skills/ekstraksi-dan-sintesis-literatur/SKILL.md) | Mengekstrak sumber ke matriks dan menyintesis argumen antar sumber |
| 04 | [desain-metodologi](skills/desain-metodologi/SKILL.md) | Merancang metode yang selaras, dapat diulang, sahih, dan etis |
| 05 | [analisis-dan-penyajian-temuan](skills/analisis-dan-penyajian-temuan/SKILL.md) | Mengolah bukti secara jujur dan menyusun tabel atau grafik yang akurat |
| 06 | [penulisan-dan-gaya-ilmiah](skills/penulisan-dan-gaya-ilmiah/SKILL.md) | Menulis tiap bagian naskah dengan alur logis dan gaya bahasa alami |
| 07 | [sitasi-dan-integritas-akademik](skills/sitasi-dan-integritas-akademik/SKILL.md) | Mengutip, memparafrase secara etis, dan menjaga konsistensi pustaka |
| 08 | [telaah-kritis-dan-uji-argumen](skills/telaah-kritis-dan-uji-argumen/SKILL.md) | Menguji ketahanan argumen layaknya penelaah sejawat dan sidang |

## Penanda Standar

Semua skill memakai empat penanda berikut agar bagian yang belum pasti langsung terlihat:

- `[VERIFIKASI]`: klaim atau identitas sumber belum dicek ke naskah asli.
- `[BUTUH DATA]`: membutuhkan bukti, angka, atau kutipan nyata dari peneliti.
- `[SITASI]`: pernyataan masih memerlukan rujukan resmi.
- `[CEK MANUSIA]`: membutuhkan pertimbangan ahli, keputusan peneliti, atau izin etik.
