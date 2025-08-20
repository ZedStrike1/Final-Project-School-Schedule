# Final Project - School Schedule Bot

## Deskripsi
Bot Discord yang dirancang untuk membantu pengelolaan kegiatan sekolah.  
Fitur utama meliputi absensi, pengecekan jadwal, PR, dan event, serta pengaturan jadwal khusus oleh admin.  
Bot ini memanfaatkan **Database** agar data bisa diubah oleh admin dan **Time** untuk sistem absensi maupun jadwal khusus.  

## Alat yang digunakan
- **Bot Discord** (discord.py)
- **Database** (untuk menyimpan dan mengubah jadwal, PR, event)
- **Time** (untuk penjadwalan otomatis dan absensi harian)

## Fitur Utama
- `!info` → Menampilkan daftar command yang tersedia (dilengkapi button untuk penjelasan fungsi).
- `!absen` → Siswa bisa melakukan absensi harian berdasarkan waktu.
- `!jadwal` → Menampilkan jadwal sekolah hari Senin–Jumat (menggunakan button untuk navigasi).
- `!pr` → Menampilkan daftar PR yang ada.
- `!event` → Menampilkan daftar event yang ada.
- `!yjadwal` → Khusus admin, mengubah jadwal.
- `!ypr` → Khusus admin, menambahkan/menginfokan PR.
- `!yevent` → Khusus admin, menambahkan/menginfokan event