"""
tampilan.py
Fungsi-fungsi untuk menampilkan data tiket di terminal.
"""

from tiket import ALUR_STATUS

KOLOM_TABEL = ["No", "Kode", "Nama Pelapor", "Jenis Masalah", "Prioritas", "Status"]


def tampilkan_tabel(daftar_tiket):
    """Cetak tabel tiket (tanpa kolom deskripsi) dengan lebar kolom menyesuaikan isi."""
    baris_data = []
    for nomor, tiket in enumerate(daftar_tiket, start=1):
        baris_data.append([
            str(nomor),
            tiket["kode_tiket"],
            tiket["nama_pelapor"],
            tiket["jenis_masalah"],
            f"[{tiket['prioritas'].upper()}]",
            f"[{tiket['status'].upper()}]",
        ])

    lebar = []
    for indeks, judul in enumerate(KOLOM_TABEL):
        lebar_isi = [len(baris[indeks]) for baris in baris_data]
        lebar.append(max([len(judul)] + lebar_isi))

    def format_baris(isi):
        return " | ".join(teks.ljust(lebar[i]) for i, teks in enumerate(isi))

    garis = "-+-".join("-" * w for w in lebar)
    print(format_baris(KOLOM_TABEL))
    print(garis)
    for baris in baris_data:
        print(format_baris(baris))
    print(garis)


def tampilkan_ringkasan(ringkasan):
    print(f"Total tiket: {ringkasan['total']} | "
          f"Menunggu: {ringkasan['Menunggu']} | "
          f"Diproses: {ringkasan['Diproses']} | "
          f"Selesai: {ringkasan['Selesai']}")


def tampilkan_detail(tiket):
    """Detail lengkap satu tiket (termasuk deskripsi)."""
    print("-" * 45)
    print(f"Kode Tiket    : {tiket['kode_tiket']}")
    print(f"Nama Pelapor  : {tiket['nama_pelapor']}")
    print(f"Jenis Masalah : {tiket['jenis_masalah']}")
    print(f"Deskripsi     : {tiket['deskripsi']}")
    print(f"Prioritas     : [{tiket['prioritas'].upper()}]")
    print(f"Status        : [{tiket['status'].upper()}]")
    print("-" * 45)


def tampilkan_menu():
    print("\n" + "=" * 45)
    print("   SISTEM HELPDESK / TIKET LAYANAN")
    print("=" * 45)
    print("1. Tambah tiket baru")
    print("2. Tampilkan semua tiket")
    print("3. Cari tiket")
    print("4. Update status tiket")
    print("5. Filter tiket berdasarkan jenis masalah")
    print("6. Hapus tiket")
    print("7. Muat data contoh (untuk demo)")
    print("0. Keluar")