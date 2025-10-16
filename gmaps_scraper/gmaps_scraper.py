import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# GANTI FUNGSI LAMA KAMU DENGAN VERSI TERAKHIR YANG PALING AKURAT INI
# Kita butuh library baru untuk 'membaca' URL
from urllib.parse import urlparse

import time
import pandas as pd
from datetime import datetime
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

def find_social_links(driver, website_url):
    """
    Fungsi untuk mengunjungi sebuah website dan mencari link Instagram & Facebook.
    """
    ig_link = "Tidak Ditemukan"
    fb_link = "Tidak Ditemukan"
    try:
        # Buka website di tab baru dengan timeout
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(website_url)
        
        # Beri waktu 5 detik untuk halaman memuat, jika lebih, batalkan.
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Cari semua link di halaman
        all_links = driver.find_elements(By.TAG_NAME, 'a')
        for link in all_links:
            url = link.get_attribute('href')
            if url:
                if 'instagram.com' in url and ig_link == "Tidak Ditemukan":
                    ig_link = url
                if 'facebook.com' in url and fb_link == "Tidak Ditemukan":
                    fb_link = url
                # Jika keduanya sudah ditemukan, berhenti mencari
                if ig_link != "Tidak Ditemukan" and fb_link != "Tidak Ditemukan":
                    break
                    
    except (TimeoutException, WebDriverException):
        # Jika website terlalu lemot atau error, lewati saja
        pass
    finally:
        # Tutup tab dan kembali ke tab utama (Google Maps)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
    return ig_link, fb_link

def scrape_google_maps(search_query, max_scrolls):
    """
    Fungsi utama untuk scraping data (VERSI 13.0 - SOCIAL MEDIA HUNTER)
    """
    print("🚀 Memulai proses scraping (v13 - Social Media Hunter)...")

    # --- Setup Selenium WebDriver ---
    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument('--start-maximized')
        # Setting timeout halaman agar tidak menunggu terlalu lama
        options.page_load_strategy = 'eager'
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Error saat setup driver: {e}"); return

    driver.get("https://www.google.com/maps")
    wait = WebDriverWait(driver, 20)

    try:
        # --- Pencarian & Scrolling ---
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "searchboxinput")))
        search_box.clear(); search_box.send_keys(search_query); search_box.send_keys(Keys.ENTER)
        print(f"🔎 Mencari untuk: '{search_query}'"); time.sleep(5)

        scrollable_panel_xpath = "//div[@role='feed']"
        scrollable_div = wait.until(EC.presence_of_element_located((By.XPATH, scrollable_panel_xpath)))

        print("👇 Memulai scrolling...");
        for i in range(max_scrolls):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(3)
            if driver.find_elements(By.XPATH, "//span[contains(text(), 'You have reached the end of the list') or contains(text(), 'Anda telah mencapai akhir daftar')]"):
                print("✅ Sudah mencapai akhir daftar."); break
        
        # --- Ekstraksi Data dari Google Maps ---
        print("🔍 Mengekstrak data awal dari Google Maps...");
        results = driver.find_elements(By.CSS_SELECTOR, "div[jsaction*='mouseover:pane']")
        if not results:
            print("❌ Gagal menemukan container hasil."); driver.quit(); return

        business_data = []
        for result in results:
            try:
                # Parsing data dasar dari Gmaps
                full_text = result.text.split('\n')
                if not full_text: continue
                nama_perusahaan = full_text[0]
                
                # Cari Nomor Kontak
                nomor_kontak = "Tidak Ditemukan"
                # (logika pencarian nomor kontak disederhanakan di sini untuk keringkasan)
                for line in full_text:
                    if "(0" in line or "08" in line: nomor_kontak = line.split('·')[-1].strip(); break
                
                # Cari Website
                website_url = "Tidak Ditemukan"
                all_links = result.find_elements(By.TAG_NAME, 'a')
                for link in all_links:
                    url = link.get_attribute('href')
                    if url and url.startswith('http'):
                        if 'google.com' not in urlparse(url).netloc: website_url = url; break
                
                if nama_perusahaan:
                    business_data.append({"Nama Perusahaan": nama_perusahaan, "Nomor Kontak": nomor_kontak, "Website": website_url})
            except Exception: continue
            
        # --- Proses Investigasi Website untuk Mencari Link Medsos ---
        print(f"🕵️  Memulai investigasi ke {len(business_data)} website untuk mencari link medsos...")
        final_data = []
        for index, business in enumerate(business_data):
            print(f"    -> Mengunjungi ({index+1}/{len(business_data)}): {business['Nama Perusahaan']}")
            ig = "Tidak Ditemukan"
            fb = "Tidak Ditemukan"
            if business['Website'] != "Tidak Ditemukan":
                ig, fb = find_social_links(driver, business['Website'])
            
            final_data.append({
                "Nama Perusahaan": business['Nama Perusahaan'],
                "Nomor Kontak": business['Nomor Kontak'],
                "Website": business['Website'],
                "Link_IG": ig,
                "Link_FB": fb
            })

        # --- Output ke Excel ---
        if not final_data: print("Tidak ada data yang berhasil diekstrak."); return

        print(f"📊 Total data terkumpul: {len(final_data)}. Memproses & menyimpan...");
        df = pd.DataFrame(final_data)
        df = df.drop_duplicates(subset=['Nama Perusahaan'], keep='first')
        
        df['has_parentheses'] = df['Nomor Kontak'].str.contains('\(', na=False)
        df_sorted = df.sort_values(by='has_parentheses').drop(columns=['has_parentheses'])

        safe_query = "".join(c if c.isalnum() else "_" for c in search_query).lower()
        today_date = datetime.now().strftime("%Y%m%d")
        filename = f"{safe_query}_{today_date}.xlsx"
        
        df_sorted.to_excel(filename, index=False)
        print(f"🎉 Sukses! Data lengkap (termasuk medsos) disimpan di file: '{filename}'")

    except Exception as e:
        print(f"❌ Terjadi kesalahan fatal: {e}")
    finally:
        driver.quit()
        print("✨ Proses selesai, browser ditutup.")

# Bagian if __name__ == "__main__": tetap sama, tidak perlu diubah.

if __name__ == "__main__":
    # --- Input dari User ---
    search_query_input = input("Masukkan kata kunci pencarian (contoh: 'perusahaan IT di Jakarta'): ")
    
    while True:
        try:
            max_scrolls_input = input("Masukkan batas maksimal scroll (default: 15, tekan Enter untuk default): ")
            if not max_scrolls_input:
                max_scrolls_input = 15
                break
            max_scrolls_input = int(max_scrolls_input)
            break
        except ValueError:
            print("Input tidak valid, masukkan angka saja.")

    # Panggil fungsi utama
    if search_query_input:
        scrape_google_maps(search_query_input, max_scrolls_input)
    else:
        print("Query pencarian tidak boleh kosong!")