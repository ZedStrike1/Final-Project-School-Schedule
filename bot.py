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

# === INIT DATABASE ===
conn = sqlite3.connect("jadwal.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS jadwal (
    hari_id INTEGER,
    guild_id INTEGER,
    seragam TEXT,
    pelajaran TEXT,
    jam TEXT,
    PRIMARY KEY (hari_id, guild_id)
)""")
c.execute("""CREATE TABLE IF NOT EXISTS jadwal_catatan (
    nomor INTEGER,
    hari_id INTEGER,
    guild_id INTEGER,
    isi TEXT,
    PRIMARY KEY (nomor, hari_id, guild_id)
)""")
conn.commit()
conn.close()

# === COMMANDS ===
@bot.command()
async def start(ctx):
    embed = discord.Embed(
        title="Selamat datang di Bot Schedule!",
        description=(
            "Bot ini dapat menyimpan dan menampilkan jadwal sekolah, termasuk:\n"
            "- Pelajaran\n"
            "- Jam\n"
            "- Seragam\n"
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
            "**Command untuk Guru (Admin):**\n"
            "Catatan: `<hari_id>` 1 = Senin, 2 = Selasa... 5 = Jumat.\n"
            "`!addPelajaran <hari_id> <pelajaran>` - Tambah pelajaran.\n"
            "`!addSeragam <hari_id> <seragam>` - Tambah atau ubah seragam.\n"
            "`!addJam <hari_id> <jam>` - Tambah atau ubah jam.\n"
            "`!addCatatan <hari_id> <isi>` - Tambah catatan.\n"
            "`!hapusCatatan <hari_id> <nomor>` - Hapus catatan berdasarkan nomor.\n"
        ),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# === ADD PELAJARAN ===
@bot.command()
@commands.has_permissions(administrator=True)
async def addPelajaran(ctx, hari_id: int, *, pelajaran: str):
    guild_id = ctx.guild.id
    conn = sqlite3.connect("jadwal.db")
    c = conn.cursor()
    c.execute("SELECT pelajaran FROM jadwal WHERE hari_id = ? AND guild_id = ?", (hari_id, guild_id))
    row = c.fetchone()
    if row:
        existing = row[0] if row[0] else ""
        new_val = existing + "\n" + pelajaran if existing else pelajaran
        c.execute("UPDATE jadwal SET pelajaran = ? WHERE hari_id = ? AND guild_id = ?", (new_val, hari_id, guild_id))
    else:
        c.execute("INSERT INTO jadwal (hari_id, guild_id, pelajaran, seragam, jam) VALUES (?, ?, ?, ?, ?)",
                  (hari_id, guild_id, pelajaran, None, None))
    conn.commit()
    conn.close()
    await ctx.send(f"Pelajaran '{pelajaran}' berhasil ditambahkan ke {hari_map[hari_id]}")

# === ADD SERAGAM ===
@bot.command()
@commands.has_permissions(administrator=True)
async def addSeragam(ctx, hari_id: int, *, seragam: str):
    guild_id = ctx.guild.id
    conn = sqlite3.connect("jadwal.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM jadwal WHERE hari_id = ? AND guild_id = ?", (hari_id, guild_id))
    if c.fetchone():
        c.execute("UPDATE jadwal SET seragam = ? WHERE hari_id = ? AND guild_id = ?", (seragam, hari_id, guild_id))
    else:
        c.execute("INSERT INTO jadwal (hari_id, guild_id, seragam, pelajaran, jam) VALUES (?, ?, ?, ?, ?)",
                  (hari_id, guild_id, seragam, None, None))
    conn.commit()
    conn.close()
    await ctx.send(f"Seragam '{seragam}' berhasil ditambahkan ke {hari_map[hari_id]}")

# === ADD JAM ===
@bot.command()
@commands.has_permissions(administrator=True)
async def addJam(ctx, hari_id: int, *, jam: str):
    guild_id = ctx.guild.id
    conn = sqlite3.connect("jadwal.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM jadwal WHERE hari_id = ? AND guild_id = ?", (hari_id, guild_id))
    if c.fetchone():
        c.execute("UPDATE jadwal SET jam = ? WHERE hari_id = ? AND guild_id = ?", (jam, hari_id, guild_id))
    else:
        c.execute("INSERT INTO jadwal (hari_id, guild_id, seragam, pelajaran, jam) VALUES (?, ?, ?, ?, ?)",
                  (hari_id, guild_id, None, None, jam))
    conn.commit()
    conn.close()
    await ctx.send(f"Jam '{jam}' berhasil ditambahkan ke {hari_map[hari_id]}")

# === ADD CATATAN ===
@bot.command()
@commands.has_permissions(administrator=True)
async def addCatatan(ctx, hari_id: int, *, catatan: str):
    guild_id = ctx.guild.id
    conn = sqlite3.connect("jadwal.db")
    c = conn.cursor()
    c.execute("SELECT MAX(nomor) FROM jadwal_catatan WHERE hari_id=? AND guild_id=?", (hari_id, guild_id))
    last = c.fetchone()[0]
    nomor = (last or 0) + 1
    c.execute("INSERT INTO jadwal_catatan (nomor, hari_id, guild_id, isi) VALUES (?, ?, ?, ?)",
              (nomor, hari_id, guild_id, catatan))
    conn.commit()
    conn.close()
    await ctx.send(f"Catatan [{nomor}] '{catatan}' berhasil ditambahkan ke {hari_map[hari_id]}")

# === HAPUS CATATAN ===
@bot.command()
@commands.has_permissions(administrator=True)
async def hapusCatatan(ctx, hari_id: int, nomor: int):
    guild_id = ctx.guild.id
    conn = sqlite3.connect("jadwal.db")
    c = conn.cursor()

    c.execute("SELECT isi FROM jadwal_catatan WHERE nomor=? AND hari_id=? AND guild_id=?", (nomor, hari_id, guild_id))
    row = c.fetchone()
    if not row:
        await ctx.send(f"Catatan nomor {nomor} tidak ditemukan di {hari_map[hari_id]}")
        conn.close()
        return
    isi = row[0]

    # hapus catatan
    c.execute("DELETE FROM jadwal_catatan WHERE nomor=? AND hari_id=? AND guild_id=?", (nomor, hari_id, guild_id))

    # rapatkan nomor
    c.execute("""
        UPDATE jadwal_catatan
        SET nomor = nomor - 1
        WHERE nomor > ? AND hari_id=? AND guild_id=?
    """, (nomor, hari_id, guild_id))

    conn.commit()
    conn.close()
    await ctx.send(f"Catatan [{nomor}] '{isi}' pada {hari_map[hari_id]} berhasil dihapus dan nomor dirapatkan.")

# === BUTTONS & VIEW ===
class JadwalButton(discord.ui.Button):
    def __init__(self, hari_id: int, label: str):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.hari_id = hari_id

    async def callback(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        conn = sqlite3.connect("jadwal.db")
        c = conn.cursor()
        c.execute("SELECT jam, pelajaran, seragam FROM jadwal WHERE hari_id=? AND guild_id=?", (self.hari_id, guild_id))
        row = c.fetchone()
        c.execute("SELECT nomor, isi FROM jadwal_catatan WHERE hari_id=? AND guild_id=? ORDER BY nomor",
                  (self.hari_id, guild_id))
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

# === RUN ===
bot.run(TOKEN)
