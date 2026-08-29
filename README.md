# Namma Chikmagaluru — E-Commerce Web Application

Premium coffee and Malabar black pepper e-commerce store built with **Django**, **Python**, **HTML**, **CSS**, and **JavaScript**. Fully responsive for web, iOS (PWA), and Android (APK via Capacitor).

## Features

- **Product catalog** — Coffee & Black Pepper categories with search, filters, and sorting
- **Shopping cart** — Add, update, remove items (works for guests and logged-in users)
- **Checkout** — Address, payment methods (COD/UPI/Card), coupon codes
- **User accounts** — Sign up, login, profile, saved addresses
- **Orders** — Order history, tracking, cancellation
- **Wishlist** — Save favourite products
- **Reviews & ratings** — Product reviews from customers
- **Admin dashboard** — Staff/superuser can manage products and view orders
- **Django Admin** — Full backend management at `/admin/`
- **Responsive UI** — Auto-adjusts to any screen size (mobile, tablet, desktop)
- **Animations** — Hero carousel, scroll animations, floating particles, animated scenes
- **PWA** — Installable on iOS via "Add to Home Screen"
- **Android APK** — Installable via Package Installer

## Quick Start

### 1. Install dependencies

```bash
cd "E commerce web Application"
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Set up database

```bash
python manage.py migrate
python manage.py seed_data
```

### 3. Run the server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000**

### Default Admin Login

| Field    | Value      |
|----------|------------|
| Username | `admin`    |
| Password | `admin123` |

- **Website admin dashboard:** http://127.0.0.1:8000/dashboard/
- **Django admin panel:** http://127.0.0.1:8000/admin/

## Project Structure

```
E commerce web Application/
├── config/           # Django settings, URLs, WSGI
├── shop/             # Main app (models, views, forms, admin)
├── templates/        # HTML templates
├── static/           # CSS, JS, images, PWA manifest
├── app/              # Capacitor mobile shell (generated)
├── scripts/          # Android patch & APK verify
├── .github/workflows/# CI + APK build
├── manage.py
├── requirements.txt
├── build_mobile.py   # Prepare Capacitor app
├── capacitor.config.json
└── package.json
```

## Mobile App (Android APK)

### Build locally

```bash
npm install
python build_mobile.py
npx cap add android
python scripts/patch_android.py
npx cap sync android
cd android && gradlew assembleDebug
```

APK output: `android/app/build/outputs/apk/debug/app-debug.apk`

### Install on Android

1. Go to **http://your-server/install/** or open `/static/install.html`
2. Tap **Download APK**
3. Open the downloaded file — Android Package Installer will prompt to install
4. Allow "Install unknown apps" for your browser if prompted

### iOS

Open the site in Safari → Share → **Add to Home Screen**

## Deploy to GitHub

```bash
git init
git add -A
git commit -m "Initial commit: Namma Chikmagaluru e-commerce"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/namma-chikmagaluru.git
git push -u origin main
```

### GitHub Actions

- **CI** — Runs on every push (migrations, Django check, seed data)
- **Build Android APK** — Go to Actions → "Build Android APK" → Run workflow

Set repository variable `APP_SERVER_URL` to your deployed site URL (e.g. `https://your-app.onrender.com`) so the APK loads your live store.

## Deploy Web App

Recommended free hosts for Django:

- **Render** — Connect GitHub repo, set build: `pip install -r requirements.txt && python manage.py migrate && python manage.py seed_data && python manage.py collectstatic --noinput`, start: `gunicorn config.wsgi:application`
- **Railway** — Similar setup with environment variables

Environment variables for production:

```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com
```

## Coupon Codes (Demo)

| Code             | Discount | Min Order |
|------------------|----------|-----------|
| CHIKMAGALURU10   | 10%      | ₹299      |
| FIRST50          | 50%      | ₹999      |

## Tech Stack

- **Backend:** Django 5, Python, SQLite
- **Frontend:** HTML5, CSS3 (responsive + animations), JavaScript
- **Mobile:** Capacitor 6, PWA (Service Worker + Manifest)
- **Static files:** WhiteNoise
- **Images:** Unsplash URLs for coffee & pepper product photos

## License

MIT — Free to use and modify.
