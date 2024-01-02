import tkinter as tk
from tkinter import simpledialog
import sqlite3
import os

class ProductEntryWindow(tk.Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        self.attributes('-fullscreen', True)

        self.barcode = None
        self.isim = None
        self.fiyat = None

        self.create_widgets()

    def create_widgets(self):
        logo_path = "logo.png"  # Logo dosya yolunu değiştirin
        if os.path.exists(logo_path):
            logo_image = tk.PhotoImage(file=logo_path)
            logo_label = tk.Label(self, image=logo_image)
            logo_label.image = logo_image  # Referansı tutmak için bu satır gereklidir
            logo_label.pack(pady=10)
        
        tk.Label(self, text="Ürünün Barkod Bilgisi:").pack(pady=5)
        self.barcode_entry = tk.Entry(self)
        self.barcode_entry.pack(pady=5)

        tk.Label(self, text="Ürün Bilgileri:").pack(pady=5)
        self.isim_entry = tk.Entry(self)
        self.isim_entry.pack(pady=5)

        tk.Label(self, text="Ürün Fiyatı:").pack(pady=5)
        self.fiyat_entry = tk.Entry(self)
        self.fiyat_entry.pack(pady=5)

        tk.Button(self, text="Kaydet", command=self.save_data).pack(pady=10)

        # Exit butonu ekleyerek pencereyi kapat
        tk.Button(self, text="Exit", command=self.destroy).pack(pady=10)

        # Bilgi gösterme için bir etiket
        self.info_label = tk.Label(self, text="")
        self.info_label.pack(pady=10)

    def save_data(self):
        self.barcode = self.barcode_entry.get()
        self.isim = self.isim_entry.get()
        self.fiyat = self.fiyat_entry.get()

        if self.barcode and self.isim and self.fiyat:
            # Veritabanına ekle
            cursor.execute("INSERT INTO urunler VALUES (?, ?, ?)", (self.barcode, self.isim, self.fiyat))
            conn.commit()

            info_text = f"Ürün bilgileri veritabanına eklendi:\nBarkod: {self.barcode}\nİsim: {self.isim}\nFiyat: {self.fiyat}"
            self.info_label.config(text=info_text)

class ProductReadWindow(tk.Toplevel):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.title(title)
        self.attributes('-fullscreen', True)

        self.create_widgets()

    def create_widgets(self):
        logo_path = "logo.png"  # Logo dosya yolunu değiştirin
        if os.path.exists(logo_path):
            logo_image = tk.PhotoImage(file=logo_path)
            logo_label = tk.Label(self, image=logo_image)
            logo_label.image = logo_image  # Referansı tutmak için bu satır gereklidir
            logo_label.pack(pady=10)

        tk.Label(self, text="Ürün Barcode:").pack(pady=5)
        self.barcode_entry = tk.Entry(self)
        self.barcode_entry.pack(pady=5)

        tk.Button(self, text="Oku", command=self.read_data).pack(pady=10)

        # Exit butonu ekleyerek pencereyi kapat
        tk.Button(self, text="Exit", command=self.destroy).pack(pady=10)

        # Bilgi gösterme için bir etiket
        self.info_label = tk.Label(self, text="")
        self.info_label.pack(pady=10)

    def read_data(self):
        barcode = self.barcode_entry.get()
        if barcode:
            # Veritabanından oku
            cursor.execute("SELECT * FROM urunler WHERE barcode=?", (barcode,))
            result = cursor.fetchone()

            if result:
                info_text = f"Ürün Bilgileri\nBarkod: {result[0]}\nİsim: {result[1]}\nFiyat: {result[2]}"
                self.info_label.config(text=info_text)
            else:
                # Ürün bulunamadı mesajını etiket üzerine yaz
                self.info_label.config(text="Ürün bulunamadı.")


def button_click(button_number):
    if button_number == 1:
        entry_window = ProductEntryWindow(root, "Ürün Bilgileri Girişi")
        root.wait_window(entry_window)

        # Bilgi etiketini sıfırla
        entry_window.info_label.config(text="")
    elif button_number == 2:
        read_window = ProductReadWindow(root, "Ürün Bilgileri Okuma")
        root.wait_window(read_window)

def exit_program():
    root.destroy()

def read_price_window():
    barcode = simpledialog.askstring("Fiyat Okuma", "Ürün Barcode:")
    if barcode is not None:
        # Veritabanından oku
        cursor.execute("SELECT * FROM urunler WHERE barcode=?", (barcode,))
        result = cursor.fetchone()

        if result:
            display_info(result)
        else:
            # Ürün bulunamadı mesajını etiket üzerine yaz
            info_window = tk.Toplevel(root)
            info_window.title("Ürün Bilgileri")
            tk.Label(info_window, text="Ürün bulunamadı.").pack(pady=10)
            tk.Button(info_window, text="Exit", command=info_window.destroy).pack(pady=10)

def display_info(info):
    info_text = f"Ürün Bilgileri\nBarkod: {info[0]}\nİsim: {info[1]}\nFiyat: {info[2]}"

    # Yeni bir pencere aç ve ürün bilgilerini göster
    info_window = tk.Toplevel(root)
    info_window.title("Ürün Bilgileri")
    tk.Label(info_window, text=info_text).pack(pady=10)
    tk.Button(info_window, text="Exit", command=info_window.destroy).pack(pady=10)

    # Fiyat Okuma penceresini tam ekran yap
    info_window.attributes('-fullscreen', True)

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Fiyat Yazma ve Okuma Örneği")
# Logo ekleyin (eğer istiyorsanız)
logo_path = "logo.png"  # Logo dosya yolunu değiştirin
if os.path.exists(logo_path):
     logo_image = tk.PhotoImage(file=logo_path)
     logo_label = tk.Label(root, image=logo_image)
     logo_label.image = logo_image  # Referansı tutmak için bu satır gereklidir
     logo_label.pack(pady=10)

# Ekran boyutunu al
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Pencere boyutunu ve konumunu ekran boyutuna ayarla
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Pencereyi tam ekran yap
root.attributes('-fullscreen', True)

# Veritabanı bağlantısını oluştur
conn = sqlite3.connect("urunler.db")
cursor = conn.cursor()

# Tablo oluştur
cursor.execute('''
    CREATE TABLE IF NOT EXISTS urunler (
        barcode TEXT PRIMARY KEY,
        isim TEXT,
        fiyat REAL
    )
''')
conn.commit()

# İlk düğme (Fiyat Yazma)
button1 = tk.Button(root, text="Fiyat Yazma", command=lambda: button_click(1))
button1.pack(pady=10)

# İkinci düğme (Fiyat Okuma)
button2 = tk.Button(root, text="Fiyat Okuma", command=lambda: button_click(2))
button2.pack(pady=10)

# Çıkış düğmesi
exit_button = tk.Button(root, text="Exit", command=exit_program)
exit_button.place(x=980, y=500, anchor="se")

# Pencereyi göster
root.mainloop()

# Veritabanı bağlantısını kapat
conn.close()