# ScanTrac — Platform QR Dinamis untuk UMKM Indonesia

## Tech Stack
- **Backend**: Python 3.10+ / Flask
- **Database**: MySQL 8+
- **QR Generator**: `qrcode` + `Pillow`
- **Frontend**: Jinja2 HTML Templates + Vanilla JS

---

## Struktur Project

```
scantrac/
├── app.py                  # App factory (create_app)
├── run.py                  # Entry point
├── requirements.txt
├── .env.example            # Salin ke .env dan isi
├── database.sql            # Schema MySQL
│
├── models/
│   ├── user.py             # Model User (login, plan)
│   ├── product.py          # Model Produk + custom fields schema
│   ├── batch.py            # Model Batch + qr_token + field_data
│   └── scan_log.py         # Log setiap scan QR
│
├── routes/
│   ├── auth.py             # /auth/login, /auth/register, /auth/logout
│   ├── dashboard.py        # /dashboard/
│   ├── product.py          # /product/ CRUD
│   ├── qr.py               # /qr/batch/new, view, download
│   └── public.py           # / (landing), /scan/<token>
│
├── utils/
│   └── qr_generator.py     # Generate QR Code PNG dengan styled
│
├── static/
│   ├── css/base.css        # Design system CSS
│   ├── js/main.js
│   └── qrcodes/            # Folder output QR PNG
│
└── templates/
    ├── base.html           # Base HTML (head, scripts)
    ├── app_base.html       # Layout dengan sidebar (halaman login)
    ├── landing.html        # Halaman publik /
    ├── auth/               # login.html, register.html
    ├── dashboard/          # index.html
    ├── product/            # list.html, new.html, edit.html
    ├── qr/                 # new_batch.html, view_batch.html
    └── public/             # product_detail.html (halaman scan konsumen)
```

---

## Setup & Menjalankan

### 1. Clone & Install Dependencies
```bash
git clone <repo>
cd scantrac
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Setup Database MySQL
```bash
mysql -u root -p < database.sql
```

### 3. Konfigurasi .env
```bash
cp .env.example .env
# Edit .env sesuai konfigurasi MySQL kamu
```

Isi file `.env`:
```
FLASK_SECRET_KEY=ganti-dengan-string-acak-panjang
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=passwordmu
DB_NAME=scantrac_db
BASE_URL=http://localhost:5000
```

### 4. Jalankan
```bash
python run.py
```

Buka browser: `http://localhost:5000`

---

## Alur Penggunaan

```
[UMKM] Daftar → Login → Tambah Produk → Definisi Field Kustom
     → Buat Batch → Generate QR Code → Download PNG → Tempel di Kemasan

[Konsumen] Scan QR → Halaman Detail Produk (real-time, selalu update)
```

---

## Cara Kerja QR Dinamis

- Setiap batch punya `qr_token` unik (UUID hex 32 karakter)
- QR Code mengarah ke: `http://yourdomain.com/scan/<qr_token>`
- UMKM bisa **update data produk kapanpun** di dashboard
- Saat konsumen scan → server ambil data terbaru dari database
- QR fisik di kemasan **tidak perlu diganti**

---

## API Endpoint Summary

| Method | URL | Keterangan |
|--------|-----|------------|
| GET/POST | `/auth/register` | Daftar akun |
| GET/POST | `/auth/login` | Login |
| GET | `/auth/logout` | Logout |
| GET | `/dashboard/` | Dashboard utama |
| GET | `/product/` | List produk |
| GET/POST | `/product/new` | Tambah produk |
| GET/POST | `/product/<id>/edit` | Edit produk |
| POST | `/product/<id>/delete` | Hapus produk |
| GET/POST | `/qr/batch/new/<product_id>` | Buat batch + generate QR |
| GET | `/qr/batch/<id>` | Lihat QR & info batch |
| GET | `/qr/batch/<id>/download` | Download QR PNG |
| GET | `/scan/<token>` | **Halaman publik konsumen** |

---

## Deployment (Production)

```bash
# Install gunicorn
pip install gunicorn

# Jalankan dengan gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

Untuk production, gunakan **Nginx** sebagai reverse proxy dan set `BASE_URL` ke domain kamu.

---

## Pengembangan Selanjutnya

- [ ] Dashboard analytics chart (Chart.js)
- [ ] Upload foto produk
- [ ] Fitur rating & review konsumen
- [ ] Export laporan PDF/Excel
- [ ] REST API untuk integrasi eksternal
- [ ] Notifikasi email saat ada scan
