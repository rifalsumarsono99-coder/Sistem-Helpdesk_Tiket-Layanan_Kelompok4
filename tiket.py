"""
tiket.py
Modul logika data tiket (Tahap 1: Array of Struct).

Satu tiket = satu dict, seluruh tiket disimpan dalam list (daftar_tiket).
Modul ini hanya berisi logika data dan validasi, tanpa print/input,
agar mudah diuji dan dibagi antar anggota kelompok.
"""

# ---------------------------------------------------------------------------
# Konstanta
# ---------------------------------------------------------------------------

JENIS_MASALAH_VALID = ("Hardware", "Software", "Jaringan", "Lainnya")
PRIORITAS_VALID = ("Rendah", "Sedang", "Tinggi")
ALUR_STATUS = ("Menunggu", "Diproses", "Selesai")


# ---------------------------------------------------------------------------
# Validasi Input
# ---------------------------------------------------------------------------

def normalisasi_pilihan(teks, pilihan_valid):
    """
    Mencocokkan input pengguna dengan pilihan valid
    tanpa memperhatikan huruf besar/kecil.
    """
    teks = teks.strip().lower()

    for pilihan in pilihan_valid:
        if pilihan.lower() == teks:
            return pilihan

    return None


def validasi_tidak_kosong(teks, nama_field):
    teks = teks.strip()

    if teks == "":
        return None, f"{nama_field} tidak boleh kosong."

    return teks, None


def validasi_kode_baru(daftar_tiket, teks):
    """
    Kode tiket harus unik.
    """
    kode, error = validasi_tidak_kosong(teks, "Kode tiket")

    if error:
        return None, error

    if cari_tiket_by_kode(daftar_tiket, kode) is not None:
        return None, f"Kode tiket '{kode}' sudah digunakan."

    return kode, None


def validasi_jenis_masalah(teks):
    jenis = normalisasi_pilihan(teks, JENIS_MASALAH_VALID)

    if jenis is None:
        return (
            None,
            f"Jenis masalah harus salah satu dari: "
            f"{', '.join(JENIS_MASALAH_VALID)}."
        )

    return jenis, None


def validasi_prioritas(teks):
    prioritas = normalisasi_pilihan(teks, PRIORITAS_VALID)

    if prioritas is None:
        return (
            None,
            f"Prioritas harus salah satu dari: "
            f"{', '.join(PRIORITAS_VALID)}."
        )

    return prioritas, None


# ---------------------------------------------------------------------------
# Operasi Data
# ---------------------------------------------------------------------------

def buat_tiket(kode, nama_pelapor, jenis_masalah, deskripsi, prioritas):
    """
    Membuat tiket baru.
    Status awal selalu 'Menunggu'.
    """
    return {
        "kode_tiket": kode,
        "nama_pelapor": nama_pelapor,
        "jenis_masalah": jenis_masalah,
        "deskripsi": deskripsi,
        "prioritas": prioritas,
        "status": ALUR_STATUS[0]
    }


def tambah_tiket(daftar_tiket, tiket):
    daftar_tiket.append(tiket)


def cari_tiket_by_kode(daftar_tiket, kode):
    """
    Mencari tiket berdasarkan kode.
    """
    kode = kode.strip()

    for tiket in daftar_tiket:
        if tiket["kode_tiket"] == kode:
            return tiket

    return None


def cari_tiket_by_nama(daftar_tiket, kata_kunci):
    """
    Pencarian nama pelapor (partial match).
    """
    kata = kata_kunci.strip().lower()

    hasil = []

    for tiket in daftar_tiket:
        if kata in tiket["nama_pelapor"].lower():
            hasil.append(tiket)

    return hasil


def filter_tiket_by_jenis(daftar_tiket, jenis_masalah):
    hasil = []

    for tiket in daftar_tiket:
        if tiket["jenis_masalah"] == jenis_masalah:
            hasil.append(tiket)

    return hasil


def hitung_ringkasan(daftar_tiket):
    """
    Menghitung total tiket dan jumlah per status.
    """
    ringkasan = {
        "total": len(daftar_tiket),
        "Menunggu": 0,
        "Diproses": 0,
        "Selesai": 0
    }

    for tiket in daftar_tiket:
        status = tiket["status"]

        if status in ringkasan:
            ringkasan[status] += 1

    return ringkasan


def status_berikutnya(status_sekarang):
    """
    Mengembalikan status berikutnya.
    None jika sudah selesai.
    """

    if status_sekarang not in ALUR_STATUS:
        return None

    posisi = ALUR_STATUS.index(status_sekarang)

    if posisi == len(ALUR_STATUS) - 1:
        return None

    return ALUR_STATUS[posisi + 1]


def perbarui_status(tiket):
    """
    Memajukan status satu langkah.
    """

    status_lama = tiket["status"]
    status_baru = status_berikutnya(status_lama)

    if status_baru is not None:
        tiket["status"] = status_baru

    return status_lama, tiket["status"]


def hapus_tiket(daftar_tiket, tiket):
    """
    Menghapus tiket jika ditemukan.
    """

    if tiket in daftar_tiket:
        daftar_tiket.remove(tiket)
        return True

    return False


# ---------------------------------------------------------------------------
# Data Contoh
# ---------------------------------------------------------------------------

def buat_data_contoh():
    """
    Data awal untuk demo dan testing.
    """

    contoh = [
        (
            "TKT001",
            "Andi Wijaya",
            "Hardware",
            "Laptop tidak bisa menyala",
            "Tinggi"
        ),
        (
            "TKT002",
            "Andi Saputra",
            "Jaringan",
            "Wi-Fi ruang dosen putus",
            "Sedang"
        ),
        (
            "TKT003",
            "Siti Rahma",
            "Software",
            "Aplikasi SIAKAD tidak bisa dibuka",
            "Rendah"
        ),
        (
            "TKT004",
            "Budi Santoso",
            "Lainnya",
            "Akun email terkunci",
            "Sedang"
        )
    ]

    return [buat_tiket(*data) for data in contoh]