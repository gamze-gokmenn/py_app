import mysql.connector
# import random
# from datetime import datetime
# from faker import Faker

conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="gmz7042",
    database="gamze_minikod"
)
cursor=conn.cursor()
def verileri_getir():
    cursor.execute("select * from orders")
    sonuc=cursor.fetchall()
    for kayit in sonuc:
        print(kayit)

# verileri_getir()

def yazdir(dosya_name,gelen):

    with open(dosya_name,"a",encoding="utf-8") as dosya:
        dosya.writelines(str(gelen)+"\n")

def verileri_yazdir():
    cursor.execute("select * from orders")
    sonuc=cursor.fetchall()
    with open("tüm_veriler.txt","w",encoding="utf-8") as dosya:
        dosya.write("")  
    for  kayit in sonuc:
        yazdir( "tüm_veriler.txt",kayit)  
    print("bitti") 

# verileri_yazdir()

def yazdir_normalize(kayit):
    satir = (
        f"Sipariş No: {kayit[0]} | "
        f"Ürün: {kayit[1]} | "
        f"Kategori: {kayit[4]} | "
        f"Fiyat: {kayit[2]} TL | "
        f"Tarih: {kayit[3]} | "
        f"Müşteri: {kayit[5]} | "
        f"Satılan Adet: {kayit[6]} | "
        f"Stok: {kayit[7]}"
    )

    with open("tüm_veriler_normalize.txt", "a", encoding="utf-8") as dosya:
        dosya.write(satir + "\n")

def verileri_yazdir_normalize():
    cursor.execute("SELECT * FROM orders")
    sonuc = cursor.fetchall()
    with open("tüm_veriler_normalize.txt","w",encoding="utf-8") as dosya:
        dosya.write("")  
    for kayit in sonuc:
        yazdir_normalize("tüm_veriler_normalize.txt",kayit)
    print("Normalize edilmiş veriler dosyaya yazıldı.")

# verileri_yazdir_normalize()

def toplami_yazdir():    #genel toplam 
    cursor.execute("SELECT SUM(satılan_adet * fiyat) AS toplam_tutar FROM orders;")
    sonuc = cursor.fetchall()
    with open("genel_toplam.txt", "w", encoding="utf-8") as dosya:
        dosya.write("")
    for kayit in sonuc:
        yazdir("genel_toplam.txt",kayit)
    print("genel toplam dosyaya yazdırıldı")

# toplami_yazdir()

def kalan_stok_yazdir():   #kalan stok
    cursor.execute("SELECT urun_adi, stok - satılan_adet AS kalan_stok FROM orders;")
    sonuc = cursor.fetchall()
    with open("kalan_stok", "w", encoding="utf-8") as dosya:
        dosya.write("")
    for kayit in sonuc:
        yazdir("kalan_stok",kayit)
    print("kalan stok dosyaya yazdırıldı")

# kalan_stok_yazdir()

def satilan_urun():  #satılan ürün
    cursor.execute("SELECT urun_adi, satılan_adet * fiyat AS toplam_tutar FROM orders;")
    sonuc = cursor.fetchall()
    with open("satilan_urun", "w", encoding="utf-8") as dosya:
        dosya.write("")
    for kayit in sonuc:
        yazdir("satilan_urun",kayit)
    print("satılan ürün dosyaya yazdırıldı")

# satilan_urun()

def yapilan_kar():
    cursor.execute("SELECT urun_adi, (fiyat - maliyet) * satılan_adet AS 'Yapılan Kar' FROM orders;")
    sonuc = cursor.fetchall()
    with open("urun_kar", "w", encoding="utf-8") as dosya:
        dosya.write("")
    for kayit in sonuc:
        yazdir("urun_kar",kayit)
    print("toplam kar dosyaya yazdırıldı")

# yapilan_kar()


def satilmayan_urunler():
    cursor.execute("SELECT * FROM orders WHERE satılan_adet = 0;")
    sonuc = cursor.fetchall()
    with open("satilmayan_urunler", "w", encoding="utf-8") as dosya:
        dosya.write("")
    for kayit in sonuc:
        yazdir("satilmayan_urunler",kayit)
    print("satılmayan ürünler dosyaya yazdırıldı")

# satilmayan_urunler()




    


