import discord
from discord.ext import commands
import sqlite3
from config import TOKEN

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

hari_map = {
    1: "Senin",
    2: "Selasa",
    3: "Rabu",
    4: "Kamis",
    5: "Jumat"
}

# ===== DATABASE SETUP =====
conn = sqlite3.connect("jadwal.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS jadwal (
    hari_id INTEGER PRIMARY KEY,
    seragam TEXT,
    pelajaran TEXT,
    jam TEXT
)""")
c.execute("""CREATE TABLE IF NOT EXISTS jadwal_pr (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hari_id INTEGER,
    isi TEXT
)""")
c.execute("""CREATE TABLE IF NOT EXISTS jadwal_catatan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hari_id INTEGER,
    isi TEXT
)""")
conn.commit()
conn.close()

# ===== COMMAND PENJELASAN BOT =====
@bot.command()
async def start(ctx):
    embed = discord.Embed(
        title="Selamat datang di Bot Schedule!",
        description=(
            "Bot ini dapat menyimpan dan menampilkan jadwal sekolah, termasuk:\n"
            "- Pelajaran\n"
            "- Jam\n"
            "- Seragam\n"
            "- PR\n"
            "- Catatan\n\n"
            "Ketik `!info` untuk melihat daftar command yang tersedia."
        ),
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)


@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="Daftar Command Bot Schedule",
        description=(
            "**Command untuk Murid:**\n"
            "`!lihatJadwal` - Lihat jadwal interaktif per hari.\n\n"
            "**Command untuk Guru:**\n"
            "`!addPelajaran <hari_id> <pelajaran>` - Tambah pelajaran.\n"
            "`!addSeragam <hari_id> <seragam>` - Tambah atau ubah seragam.\n"
            "`!addJam <hari_id> <jam>` - Tambah atau ubah jam.\n"
            "`!addPR <hari_id> <isi>` - Tambah PR.\n"
            "`!addCatatan <hari_id> <isi>` - Tambah catatan.\n"
            "`!hapusPR <id>` - Hapus PR berdasarkan ID.\n"
            "`!hapusCatatan <id>` - Hapus catatan berdasarkan ID.\n"
        ),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)


# ===== ADMIN COMMANDS =====
async def add_to_table(table: str, hari_id: int, isi: str):
    conn = sqlite3.connect("jadwal.db")
    c = conn.cursor()
    c.execute(f"INSERT INTO {table} (hari_id, isi) VALUES (?, ?)", (hari_id, isi))
    conn.commit()
    conn.close()


@bot.command()
@commands.has_permissions(administrator=True)
async def addPelajaran(ctx, hari_id: int, *, pelajaran: str):
    conn = sqlite3.connect("jadwal.db")
    c = conn.cursor()
    c.execute("SELECT pelajaran FROM jadwal WHERE hari_id = ?", (hari_id,))
    row = c.fetchone()
    if row:
        existing = row[0] if row[0] else ""
        new_val = existing + "\n" + pelajaran if existing else pelajaran
        c.execute("UPDATE jadwal SET pelajaran = ? WHERE hari_id = ?", (new_val, hari_id))
    else:
        c.execute("INSERT INTO jadwal (hari_id, pelajaran, seragam, jam) VALUES (?, ?, ?, ?)",
                  (hari_id, pelajaran, None, None))
    conn.commit()
    conn.close()
    await ctx.send(f"Pelajaran '{pelajaran}' berhasil ditambahkan ke {hari_map[hari_id]}")


@bot.command()
@commands.has_permissions(administrator=True)
async def addSeragam(ctx, hari_id: int, *, seragam: str):
    conn = sqlite3.connect("jadwal.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM jadwal WHERE hari_id = ?", (hari_id,))
    if c.fetchone():
        c.execute("UPDATE jadwal SET seragam = ? WHERE hari_id = ?", (seragam, hari_id))
    else:
        c.execute("INSERT INTO jadwal (hari_id, seragam, pelajaran, jam) VALUES (?, ?, ?, ?)",
                  (hari_id, seragam, None, None))
    conn.commit()
    conn.close()
    await ctx.send(f"Seragam '{seragam}' berhasil ditambahkan ke {hari_map[hari_id]}")


@bot.command()
@commands.has_permissions(administrator=True)
async def addJam(ctx, hari_id: int, *, jam: str):
    conn = sqlite3.connect("jadwal.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM jadwal WHERE hari_id = ?", (hari_id,))
    if c.fetchone():
        c.execute("UPDATE jadwal SET jam = ? WHERE hari_id = ?", (jam, hari_id))
    else:
        c.execute("INSERT INTO jadwal (hari_id, seragam, pelajaran, jam) VALUES (?, ?, ?, ?)",
                  (hari_id, None, None, jam))
    conn.commit()
    conn.close()
    await ctx.send(f"Jam '{jam}' berhasil ditambahkan ke {hari_map[hari_id]}")


@bot.command()
@commands.has_permissions(administrator=True)
async def addPR(ctx, hari_id: int, *, pr: str):
    await add_to_table("jadwal_pr", hari_id, pr)
    await ctx.send(f"PR '{pr}' berhasil ditambahkan ke {hari_map[hari_id]}")


@bot.command()
@commands.has_permissions(administrator=True)
async def addCatatan(ctx, hari_id: int, *, catatan: str):
    await add_to_table("jadwal_catatan", hari_id, catatan)
    await ctx.send(f"Catatan '{catatan}' berhasil ditambahkan ke {hari_map[hari_id]}")


# ===== DELETE COMMANDS =====
@bot.command()
@commands.has_permissions(administrator=True)
async def hapusPR(ctx, pr_id: int):
    conn = sqlite3.connect("jadwal.db")
    c = conn.cursor()
    c.execute("SELECT isi, hari_id FROM jadwal_pr WHERE id = ?", (pr_id,))
    row = c.fetchone()
    if not row:
        await ctx.send(f"PR dengan ID {pr_id} tidak ditemukan.")
        conn.close()
        return
    isi, hari_id = row
    c.execute("DELETE FROM jadwal_pr WHERE id = ?", (pr_id,))
    conn.commit()
    conn.close()
    await ctx.send(f"PR '{isi}' pada {hari_map[hari_id]} berhasil dihapus.")


@bot.command()
@commands.has_permissions(administrator=True)
async def hapusCatatan(ctx, cat_id: int):
    conn = sqlite3.connect("jadwal.db")
    c = conn.cursor()
    c.execute("SELECT isi, hari_id FROM jadwal_catatan WHERE id = ?", (cat_id,))
    row = c.fetchone()
    if not row:
        await ctx.send(f"Catatan dengan ID {cat_id} tidak ditemukan.")
        conn.close()
        return
    isi, hari_id = row
    c.execute("DELETE FROM jadwal_catatan WHERE id = ?", (cat_id,))
    conn.commit()
    conn.close()
    await ctx.send(f"Catatan '{isi}' pada {hari_map[hari_id]} berhasil dihapus.")


# ===== LIHAT JADWAL DENGAN EMBED PILIH HARI =====
class JadwalButton(discord.ui.Button):
    def __init__(self, hari_id: int, label: str):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.hari_id = hari_id

    async def callback(self, interaction: discord.Interaction):
        conn = sqlite3.connect("jadwal.db")
        c = conn.cursor()
        c.execute("SELECT jam, pelajaran, seragam FROM jadwal WHERE hari_id=?", (self.hari_id,))
        row = c.fetchone()
        c.execute("SELECT id, isi FROM jadwal_pr WHERE hari_id=?", (self.hari_id,))
        pr_rows = c.fetchall()
        c.execute("SELECT id, isi FROM jadwal_catatan WHERE hari_id=?", (self.hari_id,))
        catatan_rows = c.fetchall()
        conn.close()

        embed = discord.Embed(title=f"Jadwal {hari_map[self.hari_id]}", color=discord.Color.blue())
        teks = ""

        if row:
            jam, pelajaran, seragam = row
            if jam:
                teks += f"Jam: {jam}\n\n"
            if pelajaran:
                pel_list = [f"- {p.strip()}" for p in pelajaran.split("\n")]
                teks += "Pelajaran:\n" + "\n".join(pel_list) + "\n\n"
            if seragam:
                teks += f"Seragam: {seragam}\n\n"

        if pr_rows:
            pr_list = [f"- [{p[0]}] {p[1].strip()}" for p in pr_rows]
            teks += "PR:\n" + "\n".join(pr_list) + "\n\n"

        if catatan_rows:
            cat_list = [f"- [{c[0]}] {c[1].strip()}" for c in catatan_rows]
            teks += "Catatan:\n" + "\n".join(cat_list)

        if not teks:
            teks = "Belum ada jadwal untuk hari ini."

        embed.add_field(name="\u200b", value=teks, inline=False)
        await interaction.response.edit_message(embed=embed, view=self.view)


class JadwalView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for hari_id, hari in hari_map.items():
            self.add_item(JadwalButton(hari_id=hari_id, label=hari))


@bot.command()
async def lihatJadwal(ctx):
    embed = discord.Embed(description="Pilih hari untuk melihat jadwal.", color=discord.Color.green())
    view = JadwalView()
    await ctx.send(embed=embed, view=view)


bot.run(TOKEN)
