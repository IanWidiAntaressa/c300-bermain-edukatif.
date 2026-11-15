# C300 – Kalkulasi Keterlibatan Bermain Edukatif (YOLOv8 + ByteTrack)

Menghitung jumlah anak yang **sedang berada di dalam satu kotak ROI** (zona bermain) pada video MP4 / webcam / CCTV.
Definisi operasional: anak yang titik **bottom-center** bounding box-nya berada di dalam ROI dianggap terlibat bermain edukatif.
Tidak ada pengenalan wajah, identitas, gerakan, ekspresi, atau klasifikasi aktivitas.

## 1. Instalasi (Windows 10/11, VS Code + PowerShell)
Prasyarat: Python 3.10–3.12 (centang "Add Python to PATH" saat instal).

    cd C:\path\ke\c300_play
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt

Jika aktivasi diblokir: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` lalu ulangi aktivasi.
Model `yolov8n.pt` sudah ada di folder `models/` (jika hilang, diunduh otomatis saat pertama Mulai).
Untuk akurasi lebih baik di kelas ramai, ganti `"model"` di `data/config.json` menjadi `yolov8s.pt` atau `yolov8m.pt`.

## 2. Menjalankan
    streamlit run app.py
Buka http://localhost:8501.

**Login**
- Admin: username `admin`, password `admin123` (segera ubah di Dashboard > Akun Admin).
- Guest: tab "Guest" > "Masuk sebagai Guest" (tanpa password; melihat video kamera bersih tanpa bounding box, ID tracking, atau overlay ROI; jumlah anak ditampilkan di dashboard).
- Admin: video tetap menampilkan bounding box, ID tracking, dan ROI untuk pemantauan proses deteksi.

## 3. Alur penggunaan Admin
1. **Pemrosesan Video**: pilih sumber:
   - **MP4**: unggah file, atau taruh file di folder `videos/` lalu pilih dari daftar.
   - **Webcam laptop**: pilih "Webcam laptop", indeks `0` (coba `1` bila gagal). Tutup Zoom/Meet/Camera; Windows: Settings > Privacy & security > Camera > izinkan aplikasi desktop.
   - **CCTV/IP camera**: URL RTSP dari MediaMTX, mis. `rtsp://127.0.0.1:8554/kelas` jika MediaMTX berjalan pada komputer yang sama. Sesuaikan host, port, dan path dengan konfigurasi MediaMTX. Backend membaca stream langsung; tidak perlu upload atau nama file rekaman.
2. **Pengaturan ROI** (cukup sekali per kamera): klik **Ambil frame dari sumber aktif** > klik dua sudut berlawanan pada gambar > sesuaikan dengan slider > isi nama profil > **Simpan Zona**.
3. Kembali ke **Pemrosesan Video**, pilih **Profil ROI**, klik **Mulai**. Video baru dari kamera/sudut pandang yang sama langsung memakai profil tersimpan tanpa menggambar ulang.
4. **Profil Kamera**: lihat, aktifkan, atau hapus profil. **Ubah Zona**: di Pengaturan ROI pilih profil yang ingin diedit. **Reset Zona**: tombol di Pengaturan ROI.
5. **Jeda** membekukan frame dan hitungan (berguna untuk pengujian manual). Video MP4 diproses sesuai durasi aslinya dan berhenti di akhir ("Video selesai").

## 4. Profil ROI & pengecekan kecocokan
Profil disimpan di `data/roi_profiles.json` (koordinat 0–1, resolusi referensi, sumber) + frame referensi di `data/profiles/`.
Koordinat ternormalisasi sehingga otomatis proporsional di resolusi berbeda. Saat Mulai, sistem membandingkan frame pertama dengan frame referensi (fitur ORB + RANSAC) dan
rasio gambar. Jika tampak berbeda, muncul **peringatan** dan pemrosesan tidak dimulai; Admin dapat memilih profil lain, membuat ROI baru, atau menekan "Tetap gunakan profil ini".
Ambang: `scene_match_min_inliers` dan `aspect_tolerance` di `data/config.json`.

## 5. Cara menghitung
YOLOv8 (kelas person) > ByteTrack memberi ID > titik kaki = (tengah x, bawah y) kotak > dihitung jika di dalam ROI.
- Jumlah yang tampil = anak **saat ini** di ROI (bukan akumulasi). Masuk = bertambah, keluar = berkurang.
- Satu ID dihitung satu kali; deteksi tanpa ID belum dihitung.
- ID yang tidak terdeteksi > `lost_grace_seconds` (1 detik) tidak dihitung lagi.
- Hijau = di dalam ROI, merah = di luar ROI, garis/isian ungu = zona bermain.

## 6. Pengujian Counting Accuracy (target ≥ 80%)
Menu **Pengujian Akurasi**: pilih kondisi (di dalam/di luar ROI, masuk, keluar, banyak anak bergerak, berdekatan/tertutup, tidak terlihat), isi jumlah aktual (hitung manual), klik **Catat**.
Jumlah sistem diambil otomatis dari deteksi saat itu. Hasil tersimpan di SQLite, tampil sebagai tabel + ringkasan per kondisi, dan bisa diunduh CSV.

    Accuracy = (1 − |Aktual − Sistem| / Aktual) × 100%   (minimum 0%)
    Aktual = 0  ->  100% jika Sistem = 0, selain itu 0%
    Counting Accuracy akhir = rata-rata akurasi seluruh pengamatan

## 7. Struktur
    app.py            entry Streamlit, navigasi per peran
    core/             config, db (SQLite), auth, roi (profil+kecocokan), counter, processor (YOLO+ByteTrack), video, evaluation
    ui/               theme (putih-abu-ungu), login, dashboard, process, roi_page, profiles_page, testing_page
    .streamlit/       config.toml (tema ungu, batas unggah 2 GB)
    data/             config.json, roi_profiles.json, app.db, profiles/   (dibuat otomatis, permanen)
    models/ videos/   bobot YOLO dan video
    tests/            python tests/test_core.py

## 8. Keterbatasan (jujur)
- Akurasi deteksi pada video kelas Anda belum diukur; bergantung pada sudut kamera, resolusi, dan oklusi. Angka resmi harus dari menu Pengujian.
- ROI digambar dengan dua klik + slider (bukan tarik-seret), agar tidak bergantung pada komponen kanvas pihak ketiga yang rapuh.
- Video di dashboard diperbarui ±2 kali/detik (bukan streaming mulus); pemrosesan sendiri berjalan penuh di latar belakang.
- Guest tidak bisa mengubah apa pun karena menu pengaturan tidak dirender untuk Guest; ini kontrol sesi aplikasi lokal, bukan keamanan tingkat jaringan.
