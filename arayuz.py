import tkinter as tk
from tkinter import scrolledtext
import mysql.connector

# Veritabanı bağlantısı
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="gmz7042",
    database="gamze_minikod"
)
cursor = conn.cursor()

# Ana pencere
pencere = tk.Tk()
pencere.title("Sipariş Takip Arayüzü")
pencere.geometry("1000x1000")
pencere.config(bg="#e0e0e0")

# Başlık etiketi
baslik = tk.Label(pencere, text="Sipariş Takip Sistemi", font=("Arial", 18, "bold"), bg="#e0e0e0")
baslik.pack(pady=10)

# Sonuçların gösterileceği scroll'lu metin kutusu
sonuc_kutu = scrolledtext.ScrolledText(pencere, width=180, height=30)
sonuc_kutu.pack(padx=10, pady=10)

genel_toplam_frame = tk.Frame(pencere, bg="#e0e0e0")
genel_toplam_frame.pack(pady=(0,10))

genel_toplam_yazi = tk.Label(genel_toplam_frame, text="Genel Toplam: ", font=("Arial", 14), bg="#e0e0e0")
genel_toplam_yazi.pack(side=tk.LEFT)

genel_toplam_deger = tk.Label(genel_toplam_frame, text="0 TL", font=("Arial", 14, "bold"), fg="green", bg="#e0e0e0")
genel_toplam_deger.pack(side=tk.LEFT)

# Metin kutusunu temizleme fonksiyonu
def temizle():
    sonuc_kutu.delete(1.0, tk.END)

def verileri_getir():
    temizle()
    cursor.execute("SELECT * FROM orders")
    veriler = cursor.fetchall()
    for kayit in veriler:
        sonuc_kutu.insert(tk.END, f"{kayit}\n")

def verileri_yazdir_normalize():
    temizle()
    cursor.execute("SELECT * FROM orders")
    veriler = cursor.fetchall()
    for kayit in veriler:
        satir = (
            f"Sipariş No: {kayit[0]} | Ürün: {kayit[1]} | Kategori: {kayit[4]} | "
            f"Fiyat: {kayit[2]} TL | Tarih: {kayit[3]} | Müşteri: {kayit[5]} | "
            f"Satılan Adet: {kayit[6]} | Stok: {kayit[7]}"
        )
        sonuc_kutu.insert(tk.END, satir + "\n")

def toplami_yazdir():
    temizle()
    cursor.execute("SELECT SUM(`satılan_adet` * `fiyat`) FROM orders")
    toplam = cursor.fetchone()[0]
    if toplam is None:
        toplam = 0
    sonuc_kutu.insert(tk.END, f"Genel Toplam Tutar: {toplam} TL\n")
    genel_toplam_deger.config(text=f"{toplam} TL")

def kalan_stok_yazdir():
    temizle()
    cursor.execute("SELECT urun_adi, stok - satılan_adet AS kalan_stok FROM orders")
    kalanlar = cursor.fetchall()
    for urun, kalan in kalanlar:
        sonuc_kutu.insert(tk.END, f"{urun}: Kalan Stok = {kalan}\n")

def satilan_urun():
    temizle()
    cursor.execute("SELECT urun_adi, satılan_adet * fiyat AS toplam_tutar FROM orders")
    urunler = cursor.fetchall()
    for urun, toplam in urunler:
        sonuc_kutu.insert(tk.END, f"{urun}: Satılan Ürün Toplam Tutarı = {toplam} TL\n")

def yapilan_kar():
    temizle()
    cursor.execute("SELECT urun_adi, (fiyat - maliyet) * satılan_adet AS kar FROM orders")
    karlar = cursor.fetchall()
    for urun, kar in karlar:
        sonuc_kutu.insert(tk.END, f"{urun}: Yapılan Kar = {kar} TL\n")

def satilmayan_urunler():
    temizle()
    cursor.execute("SELECT * FROM orders WHERE satılan_adet = 0")
    urunler = cursor.fetchall()
    if len(urunler) == 0:
        sonuc_kutu.insert(tk.END, "Tüm ürünler satılmış.\n")
    else:
        for kayit in urunler:
            sonuc_kutu.insert(tk.END, f"{kayit}\n")

# Butonlar Frame
btn_frame = tk.Frame(pencere, bg="#e0e0e0")
btn_frame.pack(pady=10)

btn2 = tk.Button(btn_frame, text="Verileri Yazdır", command=verileri_yazdir_normalize, width=20, bg="#81BCEC", fg="black")
btn2.grid(row=0, column=0, padx=5, pady=5)

btn3 = tk.Button(btn_frame, text="Genel Toplam", command=toplami_yazdir, width=20, bg="#E8BE80", fg="black")
btn3.grid(row=0, column=2, padx=5, pady=5)

btn4 = tk.Button(btn_frame, text="Kalan Stok", command=kalan_stok_yazdir, width=20, bg="#E07EF2", fg="black")
btn4.grid(row=1, column=0, padx=5, pady=5)

btn5 = tk.Button(btn_frame, text="Satılan Ürün", command=satilan_urun, width=20, bg="#8BE7DE", fg="black")
btn5.grid(row=0, column=1, padx=5, pady=5)

btn6 = tk.Button(btn_frame, text="Yapılan Kar", command=yapilan_kar, width=20, bg="#E29D84", fg="black")
btn6.grid(row=1, column=2, padx=5, pady=5)

btn7 = tk.Button(btn_frame, text="Satılmayan Ürünler", command=satilmayan_urunler, width=20, bg="#b56761", fg="black")
btn7.grid(row=1, column=1, padx=5, pady=5)

# Arama Alanı 
arama_frame = tk.Frame(pencere, bg="#e0e0e0")
arama_frame.pack(pady=(0, 10))

arama_label = tk.Label(arama_frame, font=("Arial", 12), bg="#e0e0e0")
arama_label.pack(side=tk.LEFT)

arama_entry = tk.Entry(arama_frame, font=("Arial", 12), width=30)
arama_entry.pack(side=tk.LEFT, padx=10)

def arama_yap():
    aranan = arama_entry.get().lower()
    sonuc_kutu.delete(1.0, tk.END)
    cursor.execute("SELECT * FROM orders")
    veriler = cursor.fetchall()
    bulundu = False
    for kayit in veriler:
        kayit_str = ' '.join(map(str, kayit)).lower()
        if aranan in kayit_str:
            satir = (
                f"Sipariş No: {kayit[0]} | Ürün: {kayit[1]} | Kategori: {kayit[4]} | "
                f"Fiyat: {kayit[2]} TL | Tarih: {kayit[3]} | Müşteri: {kayit[5]} | "
                f"Satılan Adet: {kayit[6]} | Stok: {kayit[7]}"
            )
            sonuc_kutu.insert(tk.END, satir + "\n")
            bulundu = True
    if not bulundu:
        sonuc_kutu.insert(tk.END, "Aranan kriterlere uygun kayıt bulunamadı.\n")

arama_buton = tk.Button(arama_frame, text="Ara", command=arama_yap, bg="#81C784", fg="black", font=("Arial", 11))
arama_buton.pack(side=tk.LEFT)

# Ana döngü
pencere.mainloop()



