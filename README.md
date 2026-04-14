# CivicLens

A platform where citizens can read proposed legislative amendments, vote on them, leave comments, and see how the public feels through sentiment analysis. Admins get a dashboard showing trends, controversy scores, and auto-generated policy briefs.

Built as an academic project.

> **Live demo:** [civic-lens-ai-bay.vercel.app](https://civic-lens-ai-bay.vercel.app)

---

## Tech Stack

- **Frontend** — React + Vite + Tailwind CSS (hosted on Vercel)
- **Backend** — Spring Boot 4 + Spring Security + JPA (hosted on Render)
- **AI Service** — Python FastAPI microservice using HuggingFace models (hosted on Render)
- **Mobile** — React Native Expo wrapper with WebView
- **Database** — PostgreSQL (Render managed)

---

## Features

- Sentiment analysis on every comment (positive / negative / neutral)
- Controversy scoring using a custom formula: `C(a) = S · P · D · √E`
- Topic extraction using TF-IDF + KMeans clustering
- Zero-shot argument classification (support / oppose / neutral)
- Automated policy brief generation (BART-large-CNN)
- Admin dashboard with global analytics
- PDF report export
- Mobile app (Android APK via Expo EAS)

---

## How to Run Locally

You need: **Java 21**, **Maven 3.9+**, **Node.js 18+**, **Python 3.11+**, **Git**

```bash
# Clone
git clone https://github.com/hiteshmgupta/civic-lens-ai.git
cd civic-lens-ai
```

**Terminal 1 — Backend:**
```bash
cd civiclens-backend
mvn spring-boot:run
# Runs on http://localhost:8080
```

**Terminal 2 — AI Service:**
```bash
cd civiclens-ai
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
set HF_API_TOKEN=your_token   # Get free token from huggingface.co/settings/tokens
python -m uvicorn main:app --port 8000
# Runs on http://localhost:8000
```

**Terminal 3 — Frontend:**
```bash
cd civiclens-frontend
npm install
npm run dev
# Runs on http://localhost:5173
```

**Demo login:** `admin@gmail.com` / `admin@123` (admin) or `user@gmail.com` / `user@123` (user)

> Backend on Render free tier may take ~30s to wake up on first request.

---

## Project Structure

```
civic-lens-ai/
├── civiclens-frontend/   React + Vite app
├── civiclens-backend/    Spring Boot REST API
├── civiclens-ai/         Python FastAPI service
├── civiclens-mobile/     Expo mobile wrapper
├── scripts/              Dataset prep scripts
└── SETUP.md              Detailed setup guide
```

The backend auto-seeds 7 amendments, 220+ comments, and 20 test users on first start. See [scripts/README.md](scripts/README.md) for details on the dataset.

---

## Architecture

```
React Frontend (Vercel)  ──>  Spring Boot API (Render)  ──>  FastAPI AI Service (Render)
                                                                      │
Expo Mobile App ─────────────────────┘                     HuggingFace Inference API
```

---

## Environment Variables

| Variable | Where | Description |
|---|---|---|
| `JWT_SECRET` | Backend | JWT signing key |
| `AI_SERVICE_URL` | Backend | URL of the AI service (default: `http://localhost:8000`) |
| `CORS_ALLOWED_ORIGINS` | Backend | Allowed frontend URLs |
| `HF_API_TOKEN` | AI Service | HuggingFace API token (required) |
| `VITE_API_URL` | Frontend | Backend URL |

---

