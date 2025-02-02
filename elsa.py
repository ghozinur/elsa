import pyautogui
import cv2
import numpy as np
from time import sleep, time
from progress.spinner import MoonSpinner
from colorama import Fore, Style, init

# Inisialisasi colorama untuk warna konsol
init(autoreset=True)

class AutoGUI:
    def __init__(self):
        self.spinner = None
        self.current_action = ""
        
    def refresh(self):
        """Refresh kembali ke layar"""
        pyautogui.press('f5')
    
    def _update_spinner(self, message):
        """Mengupdate spinner dengan pesan baru"""
        if self.spinner:
            self.spinner.message = Fore.LIGHTYELLOW_EX + message
            self.spinner.next()
        else:
            self.spinner = MoonSpinner(Fore.LIGHTYELLOW_EX + message)
            
    def _stop_spinner(self):
        """Menghentikan spinner"""
        if self.spinner:
            self.spinner.finish()
            self.spinner = None

    def log_info(self, message):
        """Log informasi dengan warna biru"""
        print(Fore.LIGHTBLUE_EX + "[*] " + message + Style.RESET_ALL)
        
    def log_success(self, message):
        """Log sukses dengan warna hijau"""
        print(Fore.LIGHTGREEN_EX + "[+] " + message + Style.RESET_ALL)
        
    def log_error(self, message):
        """Log error dengan warna merah"""
        print(Fore.LIGHTRED_EX + "[-] " + message + Style.RESET_ALL)

    def find_image(self, image_path, timeout=30, confidence=0.8):
        """
        Mencari gambar di layar dengan spinner dan timeout
        """
        start_time = time()
        self._update_spinner(f"Mencari {image_path}...")
        
        try:
            while time() - start_time < timeout:
                try:
                    position = pyautogui.locateOnScreen(image_path, confidence=confidence)
                    if position:
                        x = position.left + (position.width // 2)
                        y = position.top + (position.height // 2)
                        self._stop_spinner()
                        self.log_success(f"Ditemukan {image_path} di ({x}, {y})")
                        return (x, y)
                        
                    sleep(0.5)  # Interval pencarian lebih pendek
                    self._update_spinner(f"Mencari {image_path} ({int(timeout - (time() - start_time))}s tersisa)...")
                    
                except Exception as e:
                    # self.log_error(f"Error saat mencari {image_path}: {str(e)}")
                    sleep(1)
                    
            self._stop_spinner()
            self.log_error(f"Gagal menemukan {image_path} dalam {timeout} detik")
            return 1, 1
            
        except KeyboardInterrupt:
            self._stop_spinner()
            self.log_error("Pencarian dihentikan pengguna")
            return None

    def click_and_type(self, coords, text, delay=1):
        """Melakukan klik dan input text"""
        try:
            pyautogui.click(coords)
            self.log_info(f"Klik di {coords}")
            sleep(delay/2)
            
            pyautogui.write(text)
            if len(text) > 0:
                self.log_info(f"Input text: {text}")
            sleep(delay/2)
            
            return True
        except Exception as e:
            self.log_error(f"Gagal melakukan operasi: {str(e)}")
            return False

def garap():
    # Konfigurasi
    CONFIG = {
        "KE1": "1.png",
        "KE2": "2.png",
        "KE3": "3.png",
        "KE4": "4.png",
        "YES": "yes.png",
        "WAIT_TIME": 3,
        "TIMEOUT": 20,
        "TEXT_TO_TYPE": "send 0.001$ eth OP to ADDRESS ENTE"
    }

    auto_gui = AutoGUI()
    
    try:
        auto_gui.log_info("Memulai proses automasi...")
        auto_gui.log_info(f"Persiapan {CONFIG['WAIT_TIME']} detik...")
        sleep(CONFIG['WAIT_TIME'])
        target = auto_gui.find_image(CONFIG["KE1"], CONFIG["TIMEOUT"])
        if target:
            auto_gui.refresh()
        sleep(CONFIG['WAIT_TIME'])
        # Step 1: Cari tombol pertama
        target = auto_gui.find_image(CONFIG["KE1"], CONFIG["TIMEOUT"])
        if not target:
            return

        # Step 2: Klik dan input text
        if auto_gui.click_and_type(target, CONFIG["TEXT_TO_TYPE"]):
            # Step 3: Cari tombol submit
            submit = auto_gui.find_image(CONFIG["KE2"], CONFIG["TIMEOUT"])
            if submit:
                auto_gui.click_and_type(submit, "")
                
                # yes = auto_gui.find_image(CONFIG["YES"], CONFIG["TIMEOUT"])
                # if yes:
                    
                # auto_gui.click_and_type(yes, "")
                # Step 4: Cari tombol send
                send = auto_gui.find_image(CONFIG["KE3"], CONFIG["TIMEOUT"])
                if send:
                    auto_gui.click_and_type(send, "")
                    
                    # Step 5: Cari tombol confirm
                    confirm = auto_gui.find_image(CONFIG["KE4"], CONFIG["TIMEOUT"])
                    if confirm:
                        auto_gui.click_and_type(confirm, "")
                        auto_gui.log_success("Proses selesai dengan sukses!")
        
    except KeyboardInterrupt:
        auto_gui.log_error("Proses dihentikan oleh pengguna")
    except Exception as e:
        auto_gui.log_error(f"Terjadi kesalahan: {str(e)}")
    finally:
        auto_gui.log_info("Program selesai dijalankan")


def main():    
    for i in range(6969):
        garap()
        sleep(7)
        
main()
