"""
main.py
Entry point sistem Helpdesk (Tahap 1: Array & Struct).
Jalankan dengan: python main.py
"""

import tiket as t
import tampilan

# Seluruh data tiket disimpan di list ini (Array of Struct).
# Data hilang saat program ditutup (disengaja untuk Tahap 1).
daftar_tiket = []


# ---------------------------------------------------------------------------
# Helper input
# ---------------------------------------------------------------------------

def minta_input_valid(prompt, fungsi_validasi):
    """Ulangi pertanyaan sampai input lolos validasi."""
    while True:
        nilai, pesan_error = fungsi_validasi(input(prompt))
        if pesan_error is None:
            return nilai
        print(f"  [!] {pesan_error}")


def minta_konfirmasi(prompt):
    """Mengembalikan True untuk 'y', False untuk 'n'. Ulangi jika input lain."""
    while True:
        jawaban = input(prompt).strip().lower()
        if jawaban == "y":
            return True
        if jawaban == "n":
            return False
        print("  [!] Masukkan 'y' atau 'n'.")


# ---------------------------------------------------------------------------
# Fitur 1 - 6
# ---------------------------------------------------------------------------

def menu_tambah_tiket():
    print("\n--- Tambah Tiket Baru ---")
    kode = minta_input_valid("Kode tiket      : ",
                             lambda x: t.validasi_kode_baru(daftar_tiket, x))
    nama = minta_input_valid("Nama pelapor    : ",
                             lambda x: t.validasi_tidak_kosong(x, "Nama pelapor"))
    print(f"Pilihan jenis masalah: {', '.join(t.JENIS_MASALAH_VALID)}")
    jenis = minta_input_valid("Jenis masalah   : ", t.validasi_jenis_masalah)
    deskripsi = minta_input_valid("Deskripsi       : ",
                                  lambda x: t.validasi_tidak_kosong(x, "Deskripsi"))
    print(f"Pilihan prioritas: {', '.join(t.PRIORITAS_VALID)}")
    prioritas = minta_input_valid("Prioritas       : ", t.validasi_prioritas)

    tiket_baru = t.buat_tiket(kode, nama, jenis, deskripsi, prioritas)
    t.tambah_tiket(daftar_tiket, tiket_baru)
    print(f"\nTiket {kode} dari {nama} berhasil dicatat.")


def menu_tampilkan_semua():
    print("\n--- Daftar Semua Tiket ---")
    if not daftar_tiket:
        print("Belum ada tiket dalam sistem.")
        return
    tampilan.tampilkan_tabel(daftar_tiket)
    tampilan.tampilkan_ringkasan(t.hitung_ringkasan(daftar_tiket))


def menu_cari_tiket():
    print("\n--- Cari Tiket ---")
    print("1. Berdasarkan kode tiket")
    print("2. Berdasarkan nama pelapor")
    mode = ""
    while mode not in ("1", "2"):
        mode = input("Pilih mode (1/2): ").strip()
        if mode not in ("1", "2"):
            print("  [!] Pilih 1 atau 2.")

    kata_kunci = minta_input_valid(
        "Kata kunci: ", lambda x: t.validasi_tidak_kosong(x, "Kata kunci"))

    if mode == "1":
        hasil = t.cari_tiket_by_kode(daftar_tiket, kata_kunci)
        if hasil is None:
            print(f"Tiket dengan kode '{kata_kunci}' tidak ditemukan.")
        else:
            tampilan.tampilkan_detail(hasil)
    else:
        hasil = t.cari_tiket_by_nama(daftar_tiket, kata_kunci)
        if not hasil:
            print(f"Tiket dengan nama pelapor '{kata_kunci}' tidak ditemukan.")
        else:
            print(f"\nDitemukan {len(hasil)} tiket.")
            tampilan.tampilkan_tabel(hasil)


def menu_update_status():
    print("\n--- Update Status Tiket ---")
    kode = input("Kode tiket: ").strip()
    tiket = t.cari_tiket_by_kode(daftar_tiket, kode)
    if tiket is None:
        print(f"Tiket dengan kode '{kode}' tidak ditemukan.")
        return

    status_baru = t.status_berikutnya(tiket["status"])
    if status_baru is None:
        print(f"Tiket {kode} sudah berstatus Selesai dan tidak dapat diperbarui lagi.")
        return

    print(f"Kode tiket       : {tiket['kode_tiket']}")
    print(f"Nama pelapor     : {tiket['nama_pelapor']}")
    print(f"Status saat ini  : {tiket['status']}")
    print(f"Status berikutnya: {status_baru}")
    if minta_konfirmasi("Lanjutkan perubahan status? (y/n): "):
        status_lama, status_baru = t.perbarui_status(tiket)
        print(f"Status tiket {kode} berhasil diperbarui: {status_lama} menjadi {status_baru}.")
    else:
        print("Perubahan status dibatalkan.")


def menu_filter_jenis():
    print("\n--- Filter Tiket Berdasarkan Jenis Masalah ---")
    print(f"Pilihan: {', '.join(t.JENIS_MASALAH_VALID)}")
    jenis = minta_input_valid("Jenis masalah: ", t.validasi_jenis_masalah)

    hasil = t.filter_tiket_by_jenis(daftar_tiket, jenis)
    if not hasil:
        print(f"Tidak ada tiket dengan jenis masalah '{jenis}' dalam sistem.")
        return
    print(f"\nMenampilkan tiket jenis masalah: {jenis} ({len(hasil)} tiket ditemukan).")
    tampilan.tampilkan_tabel(hasil)


def menu_hapus_tiket():
    print("\n--- Hapus Tiket ---")
    kode = input("Kode tiket: ").strip()
    tiket = t.cari_tiket_by_kode(daftar_tiket, kode)
    if tiket is None:
        print(f"Tiket dengan kode '{kode}' tidak ditemukan.")
        return

    # Cek status SEBELUM meminta konfirmasi
    if tiket["status"] != "Selesai":
        print(f"Tiket {kode} tidak dapat dihapus karena masih berstatus {tiket['status']}. "
              "Selesaikan penanganan tiket terlebih dahulu sebelum menghapusnya.")
        return

    tampilan.tampilkan_detail(tiket)
    if minta_konfirmasi("Yakin ingin menghapus tiket ini? (y/n): "):
        t.hapus_tiket(daftar_tiket, tiket)
        print(f"Tiket {kode} dari {tiket['nama_pelapor']} berhasil dihapus dari sistem.")
    else:
        print("Penghapusan dibatalkan.")


def menu_muat_data_contoh():
    """Hanya menambah data contoh yang kodenya belum ada."""
    ditambah = 0
    for tiket in t.buat_data_contoh():
        if t.cari_tiket_by_kode(daftar_tiket, tiket["kode_tiket"]) is None:
            t.tambah_tiket(daftar_tiket, tiket)
            ditambah += 1
    print(f"{ditambah} data contoh dimuat.")


# ---------------------------------------------------------------------------
# Program utama
# ---------------------------------------------------------------------------

def main():
    aksi_menu = {
        "1": menu_tambah_tiket,
        "2": menu_tampilkan_semua,
        "3": menu_cari_tiket,
        "4": menu_update_status,
        "5": menu_filter_jenis,
        "6": menu_hapus_tiket,
        "7": menu_muat_data_contoh,
    }
    while True:
        tampilan.tampilkan_menu()
        pilihan = input("Pilih menu: ").strip()
        if pilihan == "0":
            print("Terima kasih. Program selesai.")
            break
        elif pilihan in aksi_menu:
            aksi_menu[pilihan]()
        else:
            print("Pilihan tidak valid. Masukkan angka 0-7.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram dihentikan.")