# Gmaps Lead Scraper 🗺️

Sebuah script Python canggih yang dirancang untuk membantu tim **Business Development (Bisdev)**, sales, dan peneliti pasar mengumpulkan daftar prospek klien yang sangat detail dan otomatis dari Google Maps.

Script ini menggunakan **Selenium** untuk mengotomatisasi interaksi browser dan **Pandas** untuk mengolah data menjadi output Excel yang bersih, terurut, dan siap pakai.

-----

## ✨ Fitur Unggulan

  * **🚀 Otomatisasi Penuh**: Cukup masukkan *keyword*, script akan membuka browser, mencari, dan men-scroll halaman secara otomatis.
  * **🕵️ Social Media Hunter**: Script secara otomatis akan **mengunjungi setiap website** yang ditemukan untuk mencari dan mengekstrak tautan ke akun **Instagram** dan **Facebook** bisnis tersebut.
  * **🧠 Logika Berhenti Cerdas**: Berhenti men-scroll secara otomatis jika sudah mencapai akhir daftar, membuat proses lebih efisien.
  * **🎯 Strategi Multi-Selector**: Menggunakan kombinasi beberapa selector untuk menjaring kuantitas data semaksimal mungkin.
  * **📱 Parsing Kontak & Website Canggih**: Mampu mendeteksi berbagai format nomor telepon dan secara akurat mengidentifikasi URL website asli, bukan link internal Google.
  * **📊 Output Excel Lengkap & Terurut**: Data output (Nama, Kontak, Website, Link IG, Link FB) secara otomatis diurutkan berdasarkan prioritas dan dibersihkan dari duplikat.
  * **📂 Penamaan File Dinamis**: File Excel hasil akan disimpan dengan nama yang dinamis, contoh: `perusahaan_it_jakarta_20251016.xlsx`.

-----

## ⚙️ Instalasi

1.  **Clone repository ini:**

    ```bash
    git clone https://github.com/rotiawan/Gmaps-Lead-Scraper.git
    ```

2.  **Masuk ke direktori proyek:**

    ```bash
    cd Gmaps-Lead-Scraper
    ```

3.  **Install semua library yang dibutuhkan:**

    ```bash
    pip install -r requirements.txt
    ```

    *(Pastikan kamu punya file `requirements.txt` dengan isi di bawah ini)*

    **Isi file `requirements.txt`:**

    ```
    pandas
    selenium
    webdriver-manager
    openpyxl
    ```

-----

## 🚀 Cara Menjalankan

1.  Buka terminal atau Command Prompt di dalam direktori proyek.

2.  Jalankan script dengan perintah:

    ```bash
    python gmaps_scraper.py
    ```

3.  Script akan memintamu untuk memasukkan dua hal:

      * **Kata kunci pencarian**: Contoh -\> `perusahaan eksportir di bandung`
      * **Batas maksimal scroll**: Contoh -\> `20` (atau tekan Enter untuk default 15).

4.  Tunggu hingga proses selesai. Browser akan berjalan dan tertutup secara otomatis.

    ⚠️ **PENTING:** Karena script sekarang mengunjungi setiap website, prosesnya akan berjalan **jauh lebih lambat** dari versi sebelumnya. Mohon bersabar\!

-----

## 📁 Output

Hasil scraping akan tersimpan dalam sebuah file **Excel (`.xlsx`)** di direktori yang sama. File ini akan berisi lima kolom: `Nama Perusahaan`, `Nomor Kontak`, `Website`, `Link_IG`, dan `Link_FB`.

-----

## ⚠️ Disclaimer
  * Struktur HTML Google Maps dan website target dapat berubah sewaktu-waktu, yang mungkin menyebabkan script perlu diperbarui.
