import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def init_db():
    conn = sqlite3.connect("prediksi_diabetes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pasien (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_pasien TEXT,
            usia INTEGER,
            gula_darah REAL,
            bmi REAL,
            riwayat_ortu TEXT,
            hasil_prediksi TEXT
        )
    """)
    conn.commit()
    conn.close()

def proses_prediksi():
    nama = entry_nama.get().strip()
    usia_str = entry_usia.get().strip()
    gula_str = entry_gula.get().strip()
    bmi_str = entry_bmi.get().strip()
    riwayat = combo_riwayat.get()

    if not nama or not usia_str or not gula_str or not bmi_str or not riwayat:
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
        return
    try:
        usia = int(usia_str)
        gula = float(gula_str)
        bmi = float(bmi_str)
    except ValueError:
        messagebox.showerror(
            "Error",
            "Usia harus bilangan bulat, Gula Darah & BMI harus berupa angka!",
        )
        return

    if usia <= 0 or gula <= 0 or bmi <= 0:
        messagebox.showerror(
            "Error", "Nilai Usia, Gula Darah, dan BMI harus lebih dari 0!"
        )
        return

    if gula >= 200:
        if bmi >= 30 or riwayat == "Ya":
            hasil = "Sangat Tinggi"
            warna = "darkred"
        else:
            hasil = "Tinggi"
            warna = "red"
    elif 140 <= gula <= 199:
        if bmi >= 30 or riwayat == "Ya":
            hasil = "Tinggi"
            warna = "red"
        else:
            hasil = "Sedang"
            warna = "orange"
    else:  # Gula darah < 140
        if bmi >= 30:
            if riwayat == "Ya":
                hasil = "Sedang"
                warna = "orange"
            else:
                hasil = "Waspada"
                warna = "goldenrod"
        else:  # BMI < 30
            if riwayat == "Ya":
                hasil = "Waspada"
                warna = "goldenrod"
            else:
                hasil = "Rendah"
                warna = "green"
    label_hasil.config(text=f"Hasil Prediksi: Risiko {hasil}", fg=warna)

    # Menyimpan data ke SQLite
    conn = sqlite3.connect("prediksi_diabetes.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO pasien (nama_pasien, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (nama, usia, gula, bmi, riwayat, hasil),
    )
    conn.commit()
    conn.close()

    messagebox.showinfo("Sukses", "Data pasien berhasil disimpan ke database!")

def lihat_data():
    jendela_data = tk.Toplevel(root)
    jendela_data.title("Riwayat Data Pasien")
    jendela_data.geometry("650x300")

    kolom = ("id", "nama", "usia", "gula", "bmi", "riwayat", "hasil")
    tree = ttk.Treeview(jendela_data, columns=kolom, show="headings")

    tree.heading("id", text="ID")
    tree.heading("nama", text="Nama Pasien")
    tree.heading("usia", text="Usia")
    tree.heading("gula", text="Gula Darah")
    tree.heading("bmi", text="BMI")
    tree.heading("riwayat", text="Riwayat Ortu")
    tree.heading("hasil", text="Hasil Prediksi")

    tree.column("id", width=30)
    tree.column("nama", width=150)
    tree.column("usia", width=50)
    tree.column("gula", width=80)
    tree.column("bmi", width=60)
    tree.column("riwayat", width=90)
    tree.column("hasil", width=110)

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    conn = sqlite3.connect("prediksi_diabetes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pasien")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)



init_db()

root = tk.Tk()
root.title("Aplikasi Prediksi Risiko Diabetes")
root.geometry("350x350")

tk.Label(root, text="Nama Pasien:").grid(
    row=0, column=0, padx=10, pady=5, sticky="w"
)
entry_nama = tk.Entry(root)
entry_nama.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Usia:").grid(
    row=1, column=0, padx=10, pady=5, sticky="w"
)
entry_usia = tk.Entry(root)
entry_usia.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Gula Darah (mg/dL):").grid(
    row=2, column=0, padx=10, pady=5, sticky="w"
)
entry_gula = tk.Entry(root)
entry_gula.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="BMI:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_bmi = tk.Entry(root)
entry_bmi.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Riwayat Ortu:").grid(
    row=4, column=0, padx=10, pady=5, sticky="w"
)
combo_riwayat = ttk.Combobox(
    root, values=["Ya", "Tidak"], state="readonly", width=17
)
combo_riwayat.grid(row=4, column=1, padx=10, pady=5)

btn_prediksi = tk.Button(
    root, text="Prediksi & Simpan", command=proses_prediksi
)
btn_prediksi.grid(row=5, column=0, columnspan=2, pady=10)

btn_lihat = tk.Button(root, text="Lihat Data", command=lihat_data)
btn_lihat.grid(row=6, column=0, columnspan=2, pady=5)

label_hasil = tk.Label(
    root, text="Hasil Prediksi: -", font=("Arial", 11, "bold")
)
label_hasil.grid(row=7, column=0, columnspan=2, pady=15)

root.mainloop()