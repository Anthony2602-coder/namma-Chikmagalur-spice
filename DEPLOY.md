# Deploy Namma Chikmagaluru to GitHub

## Step 1 — Push to GitHub

```bash
cd "E commerce web Application"
git init
git add -A
git commit -m "Initial commit: Namma Chikmagaluru e-commerce"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/namma-chikmagaluru.git
git push -u origin main
```

## Step 2 — Build Android APK

1. Go to your GitHub repo → **Actions**
2. Select **Build Android APK**
3. Click **Run workflow**
4. After it completes, download `namma-chikmagaluru.apk` from Artifacts
5. Or visit `/install/` on your deployed site to download

## Step 3 — Deploy Web (Render example)

1. Create account at [render.com](https://render.com)
2. New **Web Service** → Connect GitHub repo
3. Settings:
   - **Build:** `pip install -r requirements.txt && python manage.py migrate && python manage.py seed_data && python manage.py collectstatic --noinput`
   - **Start:** `gunicorn config.wsgi:application`
4. Add environment variables:
   - `DJANGO_SECRET_KEY` = random secret string
   - `DJANGO_DEBUG` = False
   - `DJANGO_ALLOWED_HOSTS` = your-app.onrender.com

## Step 4 — Point APK to live site

In GitHub repo → **Settings → Variables**:

| Name            | Value                        |
|-----------------|------------------------------|
| APP_SERVER_URL  | https://your-app.onrender.com |

Re-run **Build Android APK** workflow. The APK will load your live store.
