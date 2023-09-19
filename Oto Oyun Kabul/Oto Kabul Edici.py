import cv2
import numpy as np
import pyautogui
import threading
import tkinter as tk
import time
import sys
import webbrowser


class EkranIzlemeUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Ekran İzleme Uygulaması")
        self.root.geometry("540x200")
        
        self.etiket = tk.Label(root, text="", font=("Helvetica", 16))
        self.etiket.pack(pady=20)
        
        self.baslat_button = tk.Button(root, text="Başlat", command=self.baslat)
        self.baslat_button.pack(pady=10)
        
        self.durdur_button = tk.Button(root, text="Durdur", state=tk.DISABLED, command=self.durdur)
        self.durdur_button.pack(pady=10)
        
        self.leaddy_etiket = tk.Label(root, text="Coded By Leaddy", font=("Helvetica", 12), fg="red", cursor="hand2")
        self.leaddy_etiket.pack()
        self.leaddy_etiket.bind("<Button-1>", self.ac_leaddy_link)

        self.thread = None
        self.calisiyor = False
        self.kabul_et_bulundu = False
        self.bekleme_suresi = 10
        self.bekleme_sayaci = self.bekleme_suresi

    def baslat(self):
        self.calisiyor = True
        self.baslat_button.config(state=tk.DISABLED)
        self.durdur_button.config(state=tk.NORMAL)
        self.thread = threading.Thread(target=self.ekrani_izle_ve_kabul_et)
        self.thread.start()

    def durdur(self):
        self.calisiyor = False
        self.baslat_button.config(state=tk.NORMAL)
        self.durdur_button.config(state=tk.DISABLED)

    def ekrani_izle_ve_kabul_et(self):
        self.etiket.config(text="Ekran izleniyor...")

        while self.calisiyor:
            tespit_koordinatlar = self.tespit_et_kabul_et()

            if tespit_koordinatlar:
                self.etiket.config(text="KABUL ET yazısı tespit edildi. Tıklanıyor...")
                self.kabul_et_tikla(tespit_koordinatlar)
                self.kabul_et_bulundu = True
                self.bekleme_sayaci = self.bekleme_suresi
            else:
                if self.kabul_et_bulundu:
                    if self.bekleme_sayaci > 0:
                        self.etiket.config(text=f"KABUL ET yazısı kayboldu. {self.bekleme_sayaci} saniye bekleniyor...")
                        self.bekleme_sayaci -= 1
                    else:
                        self.etiket.config(text="KABUL ET yazısı tekrar görülmedi. Uygulama kapatılıyor...")
                        self.durdur()
                        self.root.after(2000, self.kapat)  # 2 saniye bekledikten sonra uygulamayı kapat
                        self.kabul_et_bulundu = False
                        self.bekleme_sayaci = self.bekleme_suresi

            time.sleep(1)

    def tespit_et_kabul_et(self):
        ekran_goruntusu = pyautogui.screenshot()
        ekran_goruntu_np = np.array(ekran_goruntusu)
        ekran_goruntu_bgr = cv2.cvtColor(ekran_goruntu_np, cv2.COLOR_RGB2BGR)

        kabul_et_kalip = cv2.imread('kabul_et_kalip.png', cv2.IMREAD_COLOR)

        sonuc = cv2.matchTemplate(ekran_goruntu_bgr, kabul_et_kalip, cv2.TM_CCOEFF_NORMED)
        _, _, _, maksimum_lokasyon = cv2.minMaxLoc(sonuc)

        threshold_degeri = 0.8
        if sonuc[maksimum_lokasyon[1], maksimum_lokasyon[0]] >= threshold_degeri:
            x, y = maksimum_lokasyon
            x += 75
            y += 40
            return (x, y)
        else:
            return None

    def kabul_et_tikla(self, koordinatlar):
        x, y = koordinatlar
        pyautogui.click(x, y)

    def kapat(self):
        self.root.destroy()

    def ac_leaddy_link(self, event):
        webbrowser.open("https://linktr.ee/leaddy")


if __name__ == "__main__":
    root = tk.Tk()
    uygulama = EkranIzlemeUygulamasi(root)
    root.mainloop()
