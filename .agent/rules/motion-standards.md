# Motion Standards (9:16 Vertical)

- **Resolusi & Rasio:** `1080x1920` (vertikal `9:16`).
- **Frame Rate:** `30fps` (sesuai standar cheat sheet).
- **Safe Zone Mobile:** Sisakan ruang kosong `18%` di bagian atas dan `22%` di bagian bawah agar teks, judul, dan elemen utama tidak tertutup UI aplikasi maupun caption.
- **Animasi:** Utamakan gerak berbasis `spring physics` yang halus dan terukur.
- **Audio & Output:** Gunakan `public/vo.wav` sebagai patokan durasi dan ketukan narasi bila tersedia, lalu hasilkan video akhir ke `out/final-video.mp4`.
- **Visual QA di Runner:** Karena GitHub Actions berjalan di runner tanpa browser interaktif bawaan, pemeriksaan hasil dilakukan melalui artefak atau rilis hasil render yang diunduh.
