Tentu, ini dia draf lengkap isi file `README.md` yang keren dan informatif buat repo GitHub kamu. Tinggal *copy-paste* aja\!

-----

# Gmaps Lead Scraper 🗺️

Sebuah script Python yang dirancang untuk membantu tim **Business Development (Bisdev)**, sales, dan peneliti pasar mengumpulkan daftar prospek klien secara efisien dan otomatis dari Google Maps.

Script ini menggunakan **Selenium** untuk mengotomatisasi interaksi browser dan **Pandas** untuk mengolah data menjadi output Excel yang bersih dan siap pakai.

## ✨ Fitur Unggulan

  * **🚀 Otomatisasi Penuh**: Cukup masukkan *keyword* pencarian, script akan membuka browser, melakukan pencarian, dan men-scroll halaman secara otomatis.
  * **🧠 Logika Berhenti Cerdas**: Script akan berhenti men-scroll secara otomatis jika sudah mencapai akhir daftar hasil pencarian, membuat proses lebih efisien.
  * **🎯 Strategi Multi-Selector**: Menggunakan kombinasi beberapa selector untuk menjaring kuantitas data semaksimal mungkin, menangkap hasil yang mungkin terlewat oleh metode biasa.
  * **📱 Parsing Nomor Kontak Canggih**: Mampu mendeteksi dan mengekstrak berbagai format nomor telepon, baik nomor HP (08xx) maupun telepon kantor ((0xx)).
  * **📊 Output Excel yang Rapi & Terurut**: Data output secara otomatis diurutkan berdasarkan prioritas (nomor HP terlebih dahulu) dan dibersihkan dari duplikat.
  * **📂 Penamaan File Dinamis**: File Excel hasil akan disimpan dengan nama yang dinamis berdasarkan *keyword* pencarian dan tanggal, contoh: `perusahaan_it_jakarta_20251015.xlsx`.

-----

## 📋 Prasyarat

  * Python 3.7+
  * Google Chrome terinstall di komputermu.

## ⚙️ Instalasi

1.  **Clone repository ini:**

    ```bash
    git clone https://github.com/NAMAPENGGUNAANDA/NAMA-REPO-ANDA.git
    ```

2.  **Masuk ke direktori proyek:**

    ```bash
    cd NAMA-REPO-ANDA
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
      * **Batas maksimal scroll**: Contoh -\> `20` (atau tekan Enter untuk menggunakan default 15).

4.  Tunggu hingga proses selesai. Browser akan berjalan dan tertutup secara otomatis.

-----

## 📁 Output

Hasil scraping akan tersimpan dalam sebuah file **Excel (`.xlsx`)** di direktori yang sama. File ini akan berisi dua kolom: `Nama Perusahaan` dan `Nomor Kontak`, dengan data yang sudah bersih dan terurut.

## ⚠️ Disclaimer

  * Script ini dibuat untuk tujuan edukasi dan membantu otomatisasi pekerjaan profesional.
  * Struktur HTML Google Maps dapat berubah sewaktu-waktu tanpa pemberitahuan, yang mungkin menyebabkan script perlu diperbarui.
  * Gunakan dengan bijak dan bertanggung jawab. Jangan melakukan permintaan dalam jumlah masif dalam waktu singkat untuk menghormati kebijakan Google.

## 📄 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT.
