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

# GANTI FUNGSI LAMA KAMU DENGAN VERSI KUANTITAS MAKSIMAL INI
def scrape_google_maps(search_query, max_scrolls):
    """
    Fungsi utama untuk melakukan scraping data nama bisnis dan nomor kontak
    dari Google Maps. (VERSI 9.0 - FOKUS PADA KUANTITAS MAKSIMAL)

    Args:
        search_query (str): Kata kunci yang akan dicari di Google Maps.
        max_scrolls (int): Jumlah maksimal scroll ke bawah pada panel hasil.
    """
    print("🚀 Memulai proses scraping (v9 - Max Quantity)...")

    # --- Setup Selenium WebDriver ---
    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        # options.add_argument('--headless')
        options.add_argument('--start-maximized')
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Error saat setup driver: {e}")
        return

    driver.get("https://www.google.com/maps")
    wait = WebDriverWait(driver, 20)

    try:
        # --- Melakukan Pencarian & Scrolling (Sama seperti sebelumnya) ---
        search_box = wait.until(EC.element_to_be_clickable((By.ID, "searchboxinput")))
        search_box.clear()
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.ENTER)
        print(f"🔎 Mencari untuk: '{search_query}'")
        time.sleep(5) 

        scrollable_panel_xpath = "//div[@role='feed']"
        scrollable_div = wait.until(EC.presence_of_element_located((By.XPATH, scrollable_panel_xpath)))
        
        print("👇 Memulai scrolling untuk memuat semua data...")
        for i in range(max_scrolls):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(3)
            end_of_list_xpath = "//span[contains(text(), 'You have reached the end of the list') or contains(text(), 'Anda telah mencapai akhir daftar')]"
            if driver.find_elements(By.XPATH, end_of_list_xpath):
                print("✅ Sudah mencapai akhir daftar. Menghentikan scroll.")
                break
        
        # --- Ekstraksi Data dengan Strategi Multi-Selector ---
        print("🔍 Mengekstrak data dengan strategi multi-selector...")
        
        # Jaring 1: Selector presisi (yang kita pakai sekarang)
        results_precise = driver.find_elements(By.CSS_SELECTOR, "div[jsaction*='mouseover:pane']")
        print(f"   > Jaring 1 (presisi) menangkap: {len(results_precise)} hasil.")

        # Jaring 2: Selector lebar (kembali ke 'role=article' sebagai cadangan)
        results_broad = driver.find_elements(By.CSS_SELECTOR, "div[role='article']")
        print(f"   > Jaring 2 (lebar) menangkap: {len(results_broad)} hasil.")

        # Gabungkan semua hasil ke dalam satu list
        all_results = results_precise + results_broad

        if not all_results:
            print("❌ Gagal menemukan container hasil dengan kedua selector.")
            driver.quit()
            return

        business_data = []
        for result in all_results:
            try:
                # Logika parsing tetap sama
                full_text = result.text.split('\n')
                if not full_text or len(full_text) < 2:
                    continue

                nama_perusahaan = full_text[0]
                nomor_kontak = "Tidak Ditemukan"
                nomor_ditemukan = False
                
                for line in full_text:
                    parts = line.split('·')
                    for part in parts:
                        potential_number = part.strip()
                        if potential_number.startswith('(0'):
                            nomor_kontak = potential_number; nomor_ditemukan = True; break
                        cleaned_part = potential_number.replace('-', '').replace(' ', '')
                        if cleaned_part.startswith('0') and cleaned_part.isdigit() and len(cleaned_part) >= 9:
                            nomor_kontak = potential_number; nomor_ditemukan = True; break
                    if nomor_ditemukan: break

                if nama_perusahaan:
                    business_data.append({
                        "Nama Perusahaan": nama_perusahaan,
                        "Nomor Kontak": nomor_kontak
                    })
            except Exception:
                continue

        # --- Output ke Excel dengan Deduplikasi & Sorting ---
        if not business_data:
            print("Tidak ada data yang berhasil diekstrak.")
            return

        print(f"📊 Total data mentah terkumpul: {len(business_data)}. Memproses & menyimpan...")
        df = pd.DataFrame(business_data)
        
        # 1. Buang duplikat berdasarkan Nama Perusahaan
        df = df.drop_duplicates(subset=['Nama Perusahaan'], keep='first')
        print(f"   > Setelah buang duplikat, tersisa: {len(df)} data unik.")

        # 2. Lakukan sorting seperti sebelumnya
        df['has_parentheses'] = df['Nomor Kontak'].str.contains('\(', na=False)
        df_sorted = df.sort_values(by='has_parentheses').drop(columns=['has_parentheses'])

        # 3. Simpan ke Excel
        safe_query = "".join(c if c.isalnum() else "_" for c in search_query).lower()
        today_date = datetime.now().strftime("%Y%m%d")
        filename = f"{safe_query}_{today_date}.xlsx"
        
        df_sorted.to_excel(filename, index=False)
        print(f"🎉 Sukses! Data kuantitas maksimal disimpan di file: '{filename}'")

    except Exception as e:
        print(f"❌ Terjadi kesalahan fatal saat proses scraping: {e}")
    finally:
        driver.quit()
        print("✨ Proses selesai, browser sudah ditutup.")

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