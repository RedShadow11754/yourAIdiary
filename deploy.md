# 🚀 MindWell Backend Deployment Guide (Render Free Tier)

## Architecture Overview

```
Render Free Web Service (Django + Gunicorn)
    ├── PostgreSQL (Render free — 30 day limit)
    ├── Upstash Redis (Celery broker — free tier)
    ├── Qdrant Cloud (vector DB — free tier)
    ├── Jina Embeddings API (embeddings — free tier)
    └── Groq API (LLM — free tier)
```

---

## Prerequisites

Before touching Render, set up these free-tier services:

### 1. Upstash Redis (Celery Broker)

1. Go to [upstash.com](https://upstash.com) → Sign up (GitHub login works)
2. Click **"Create Database"**
   - Name: `mindwell-redis`
   - Region: pick closest to your users
   - Type: **Regional** (not global)
3. Once created, copy the **`REDIS_URL`** from the connection details page
   - It looks like: `rediss://default:xxxxx@usw1-xxxx.upstash.io:6379`

### 2. Qdrant Cloud (Vector Database)

1. Go to [cloud.qdrant.io](https://cloud.qdrant.io) → Sign up
2. Create a **free cluster**
   - Name: `mindwell`
   - Region: pick closest to you
   - RAM: 1 GB (free tier)
3. Once ready, copy the **Cluster URL** from the dashboard
   - It looks like: `https://xxxxx.cloud.qdrant.io:6333`
4. Go to **API Keys** → Create an API key → copy it
5. Your `QDRANT_URL` will be: `https://<api-key>@xxxxx.cloud.qdrant.io:6333`

### 3. Jina Embeddings API

1. Go to [jina.ai](https://jina.ai) → Sign up
2. Go to **API Keys** → Create a new key
3. Copy the key — this is your `JINA_API_KEY`
4. Free tier: 1M tokens/month (plenty for v1)

### 4. Groq API (you likely already have this)

1. Go to [console.groq.com](https://console.groq.com)
2. Copy your API key if you haven't already
3. This is your `GROQ_API_KEY`

---

## Step-by-Step Render Deployment

### Step 1: Push Updated Code to GitHub

Make sure all the changes from this session are committed and pushed:

```bash
cd your-project-root

# Check what changed
git status

# Add all changes
git add requirements.txt build.sh render.yaml config/settings.py memory/embeddings.py

# Commit
git commit -m "Configure for Render deployment"

# Push
git push origin main
```

### Step 2: Create a Render Account

1. Go to [render.com](https://render.com)
2. Sign up with your **GitHub account**
3. Authorize Render to access your repositories

### Step 3: Create a PostgreSQL Database

1. From the Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Fill in:
   - **Name**: `mindwell-db`
   - **Database**: `mindwell`
   - **Plan**: Free
3. Click **"Create Database"**
4. Wait for it to become "Available" (~1 min)
5. Copy the **Internal Database URL** (you'll need this later)

### Step 4: Create the Web Service

1. From the Dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository:
   - Select your repo
   - Click **"Connect"**
3. Configure the service:
   - **Name**: `mindwell-api`
   - **Runtime**: Python
   - **Build Command**:
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command**:
     ```
     gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
     ```
   - **Plan**: Free

4. **Add Environment Variables** (click "Advanced" → "Add Env Var"):

   | Key | Value |
   |-----|-------|
   | `DJANGO_SECRET_KEY` | *(click "Generate")* |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `mindwell-api.onrender.com` |
   | `DATABASE_URL` | *(paste the PostgreSQL Internal URL from Step 3)* |
   | `REDIS_URL` | *(paste your Upstash REDIS_URL from Prerequisites)* |
   | `GROQ_API_KEY` | *(your Groq API key)* |
   | `JINA_API_KEY` | *(your Jina API key from Prerequisites)* |
   | `QDRANT_URL` | *(your Qdrant Cloud URL from Prerequisites)* |
   | `EMAIL_HOST_USER` | *(your Gmail address)* |
   | `EMAIL_HOST_PASSWORD` | *(your Gmail App Password)* |
   | `GOOGLE_CLIENT_ID` | *(your Google OAuth client ID)* |
   | `GOOGLE_CLIENT_SECRET` | *(your Google OAuth client secret)* |
   | `GOOGLE_REDIRECT_URI` | `https://mindwell-api.onrender.com/api/auth/google/callback/` |
   | `FRONTEND_URL` | `https://your-frontend-domain.com` |
| `CORS_ALLOWED_ORIGINS` | `https://your-frontend-domain.com` |

5. Click **"Create Web Service"**

6. Render will now:
   - Pull your code
   - Install dependencies
   - Run `collectstatic`
   - Run `migrate`
   - Start the server

7. Wait for the deploy to succeed (~3-5 min for first deploy)

### Step 5: Verify the Deployment

Once the service shows "Live", test it:

```bash
# Test the root endpoint
curl https://mindwell-api.onrender.com/

# Test admin (should show login page)
curl https://mindwell-api.onrender.com/admin/
```

### Step 6: Create a Superuser

You need a superuser to access the admin panel. Since Render doesn't give you shell access to the running service, do this:

1. **Option A — One-off command on Render:**
   - Go to your web service → **"Shell"** tab (if available)
   - Or use **"Manual Deploy"** → **"Clear build cache & deploy"** and add to build command:
     ```
     python manage.py createsuperuser --noinput
     ```
     (but this requires env vars like `DJANGO_SUPERUSER_PASSWORD`)

2. **Option B — Run locally against the Render database:**
   ```bash
   # Set the DATABASE_URL env var locally to point to Render's PostgreSQL
   export DATABASE_URL="postgres://mindwell:xxxxx@xxxxx.onrender.com:5432/mindwell"
   python manage.py createsuperuser
   ```

### Step 7: Update Google OAuth Redirect URI

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **APIs & Services** → **Credentials**
3. Edit your OAuth 2.0 Client ID
4. Add to **Authorized redirect URIs**:
   ```
   https://mindwell-api.onrender.com/api/auth/google/callback/
   ```
5. Save

### Step 8: Update Frontend API URL

In your frontend code, update the API base URL to:
```
https://mindwell-api.onrender.com
```

---

## Optional: Add Celery Worker (Background Tasks)

If you want memory extraction and diary generation to run in the background:

### Create a Background Worker Service

1. On Render Dashboard, click **"New +"** → **"Background Worker"**
2. Connect the same repo
3. Configure:
   - **Name**: `mindwell-celery-worker`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `celery -A config worker -l info`
   - **Plan**: Free
4. Add the **same environment variables** as the web service
5. Click **"Create Background Worker"**

### Create a Celery Beat Scheduler (for periodic tasks)

1. Click **"New +"** → **"Background Worker"**
2. Configure:
   - **Name**: `mindwell-celery-beat`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `celery -A config beat -l info`
   - **Plan**: Free
3. Add the **same environment variables**
4. Create

> **Note**: On free tier, background workers spin down too. For v1, you can skip Celery and the background tasks will just not run until you add workers.

---

## Important Notes for Free Tier

### ⚡ Cold Starts
Free web services spin down after **15 minutes** of no traffic. The first request after spin-down takes **30-60 seconds**. This is normal for free tier.

### 🗄️ PostgreSQL Expiry
Free Render PostgreSQL databases **expire after 30 days**. For v1 testing this is fine. When you're ready for production, upgrade to the $6/mo Basic plan.

### 💾 512MB RAM Limit
The free tier gives 512MB RAM. Your app should be fine since we removed sentence-transformers (which needed ~2GB).

### 🔒 Environment Variables
Never commit `.env` to Git. All secrets are set via Render's environment variable panel.

---

## Troubleshooting

### "Application failed to respond"
- Check the **Logs** tab on Render
- Usually a missing environment variable or migration error

### "ModuleNotFoundError"
- Check that `requirements.txt` is correct
- Make sure the build command runs `pip install -r requirements.txt`

### Database connection errors
- Make sure `DATABASE_URL` is set correctly
- The Render PostgreSQL URL includes the `postgres://` protocol

### CORS errors from frontend
- Make sure `CORS_ALLOWED_ORIGINS` is set to your frontend domain
- The `django-cors-headers` package is already configured

### Jina embeddings failing
- Check that `JINA_API_KEY` is set
- Free tier has rate limits — if hitting them, add retry logic

---

## Environment Variables Summary

| Variable | Where to get it | Required |
|----------|----------------|----------|
| `DJANGO_SECRET_KEY` | Render auto-generates | ✅ |
| `DEBUG` | Set to `False` | ✅ |
| `ALLOWED_HOSTS` | Your Render URL | ✅ |
| `DATABASE_URL` | Render PostgreSQL | ✅ |
| `REDIS_URL` | Upstash dashboard | ✅ (for Celery) |
| `GROQ_API_KEY` | console.groq.com | ✅ |
| `JINA_API_KEY` | jina.ai dashboard | ✅ |
| `QDRANT_URL` | cloud.qdrant.io | ✅ |
| `EMAIL_HOST_USER` | Your Gmail | ✅ |
| `EMAIL_HOST_PASSWORD` | Gmail App Password | ✅ |
| `GOOGLE_CLIENT_ID` | Google Cloud Console | Optional |
| `GOOGLE_CLIENT_SECRET` | Google Cloud Console | Optional |
| `GOOGLE_REDIRECT_URI` | Set to Render callback URL | Optional |
| `FRONTEND_URL` | Your frontend domain | Optional |
| `CORS_ALLOWED_ORIGINS` | Your frontend domain | ✅ (for cross-origin requests) |
