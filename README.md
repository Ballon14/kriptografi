# Secure File Vault

Secure File Vault adalah aplikasi desktop sederhana untuk mengenkripsi dan mendekripsi file menggunakan kombinasi RSA-2048 dan AES-256. Aplikasi ini cocok untuk melindungi file sensitif dengan format output `.filevault`.

## Fitur

- Enkripsi file normal menjadi file `.filevault`
- Dekripsi file `.filevault` kembali ke file asli
- Menggunakan pasangan kunci RSA secara otomatis
- Menyimpan hasil enkripsi di folder `encrypted`
- Menyimpan hasil dekripsi di folder `decrypted`

## Persyaratan

Pastikan sistem Anda sudah memiliki:

- Python 3.10 atau lebih tinggi
- Git
- PowerShell / terminal

## Cara Clone Repository

Jika Anda belum memiliki salinan repo, jalankan:

```bash
git clone https://github.com/Ballon14/kriptografi.git
cd kriptografi
```

## Cara Pull Update Terbaru

Jika repository sudah ada dan ingin mengambil update terbaru:

```bash
git pull origin main
```

> Jika branch yang Anda gunakan bukan `main`, sesuaikan dengan branch yang aktif.

## Instalasi Dependensi

Buat virtual environment (opsional tapi disarankan):

```bash
python -m venv .venv
```

Aktifkan environment:

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install kebutuhan aplikasi:

```bash
pip install -r requirements.txt
```

## Cara Menjalankan Aplikasi

Jalankan file utama aplikasi:

```bash
python app.py
```

Atau jika Anda menggunakan virtual environment yang sudah aktif:

```bash
python app.py
```

## Cara Menggunakan Aplikasi

1. Jalankan aplikasi dengan perintah di atas.
2. Buka menu `Security` lalu pilih `Generate RSA key`.
3. Pilih file yang ingin Anda enkripsi:
   - File normal untuk enkripsi
   - File `.filevault` untuk dekripsi
4. Klik tombol `Encrypt` atau `Decrypt` sesuai kebutuhan.

## Lokasi Hasil Output

- Hasil enkripsi akan disimpan di folder `encrypted`
- Hasil dekripsi akan disimpan di folder `decrypted`
- Kunci RSA akan dibuat di folder `keys`

## Catatan Penting

- Pastikan Anda telah membuat kunci RSA sebelum melakukan enkripsi.
- File yang akan didekripsi harus berupa file berekstensi `.filevault`.
- Jika aplikasi tidak berjalan karena policy PowerShell, Anda bisa menjalankan:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

## Pengembangan

Untuk menjalankan test:

```bash
pytest
```
