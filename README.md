# Bot Jadwal Sekolah Discord

Bot ini dirancang untuk mengelola dan menampilkan **jadwal sekolah** lengkap dengan pelajaran, jam, seragam, PR, dan catatan harian. Bot menggunakan **discord.py** dan **SQLite** sebagai database.

---

## Fitur

1. **Lihat Jadwal Interaktif**
   - Command: `!lihatJadwal`
   - Menampilkan tombol per hari (Senin–Jumat)
   - Menampilkan:
     - Pelajaran
     - Jam
     - Seragam
     - PR
     - Catatan

2. **Admin Commands**
   - `!addPelajaran <hari_id> <pelajaran>` → Tambah pelajaran per hari
   - `!addSeragam <hari_id> <seragam>` → Tambah/ubah seragam
   - `!addJam <hari_id> <jam>` → Tambah/ubah jam
   - `!addPR <hari_id> <isi>` → Tambah PR
   - `!addCatatan <hari_id> <isi>` → Tambah catatan
   - `!hapusPR <id>` → Hapus PR berdasarkan ID
   - `!hapusCatatan <id>` → Hapus catatan berdasarkan ID

3. **Informasi Bot**
   - `!start` → Menjelaskan fungsi bot, meminta user ketik `!info`
   - `!info` → Menampilkan daftar command bot

---

## Struktur Database

- **jadwal**  
  - `hari_id` INTEGER PRIMARY KEY  
  - `pelajaran` TEXT  
  - `jam` TEXT  
  - `seragam` TEXT

- **jadwal_pr**  
  - `id` INTEGER PRIMARY KEY AUTOINCREMENT  
  - `hari_id` INTEGER  
  - `isi` TEXT

- **jadwal_catatan**  
  - `id` INTEGER PRIMARY KEY AUTOINCREMENT  
  - `hari_id` INTEGER  
  - `isi` TEXT

---

## Instalasi

1. Install Python 3.11+  
2. Install library:  
```bash
pip install discord.py
