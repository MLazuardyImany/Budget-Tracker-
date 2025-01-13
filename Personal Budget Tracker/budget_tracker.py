import sqlite3
from datetime import datetime

# Koneksi ke database SQLite
conn = sqlite3.connect("budget_tracker.db")
cursor = conn.cursor()

# Membuat tabel jika belum ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    date TEXT
)
""")
conn.commit()

def add_transaction():
    try:
        amount = float(input("Masukkan jumlah: "))
        category = input("Masukkan kategori (contoh: Makanan, Transportasi): ")
        date = input("Masukkan tanggal (YYYY-MM-DD, tekan enter untuk hari ini): ")
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        cursor.execute("INSERT INTO transactions (amount, category, date) VALUES (?, ?, ?)", 
                       (amount, category, date))
        conn.commit()
        print("Transaksi berhasil ditambahkan!")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def view_transactions():
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    print("\n=== Semua Transaksi ===")
    for row in rows:
        print(f"ID: {row[0]}, Jumlah: {row[1]}, Kategori: {row[2]}, Tanggal: {row[3]}")
    print()

def filter_transactions():
    category = input("Masukkan kategori untuk filter: ")
    cursor.execute("SELECT * FROM transactions WHERE category = ?", (category,))
    rows = cursor.fetchall()
    print(f"\n=== Transaksi dengan Kategori '{category}' ===")
    for row in rows:
        print(f"ID: {row[0]}, Jumlah: {row[1]}, Kategori: {row[2]}, Tanggal: {row[3]}")
    print()

def monthly_report():
    month = input("Masukkan bulan (format YYYY-MM): ")
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE date LIKE ?", (f"{month}%",))
    total = cursor.fetchone()[0] or 0
    print(f"\n=== Laporan Bulanan {month} ===")
    print(f"Total Pengeluaran/Pemasukan: {total}\n")

def main():
    while True:
        print("\n=== Personal Budget Tracker ===")
        print("1. Tambah Transaksi")
        print("2. Tampilkan Semua Transaksi")
        print("3. Filter Transaksi")
        print("4. Laporan Bulanan")
        print("5. Keluar")
        
        choice = input("Pilih opsi: ")
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            filter_transactions()
        elif choice == "4":
            monthly_report()
        elif choice == "5":
            print("Keluar dari program. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")

if __name__ == "__main__":
    main()
