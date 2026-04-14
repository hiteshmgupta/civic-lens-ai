# CivicLens — Setup Guide

How to install everything and run CivicLens locally.

---

## Prerequisites

Install these before starting:

| Tool | Version | Download |
|---|---|---|
| Java (JDK) | 21 | [adoptium.net](https://adoptium.net/) |
| Maven | 3.9+ | [maven.apache.org](https://maven.apache.org/download.cgi) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org/) |
| Python | 3.11+ | [python.org](https://www.python.org/downloads/) |
| Git | Any | [git-scm.com](https://git-scm.com/) |

Make sure to check "Add to PATH" during installation for Java, Maven, Node.js, and Python.

Verify everything is installed:
```bash
java --version      # should show 21.x
mvn --version       # should show 3.9+
node --version      # should show v18+
python --version    # should show 3.11+
git --version
```

---

## Running the Project

You need 3 terminals open at the same time.

### Terminal 1 — Backend

```bash
cd civiclens-backend
mvn spring-boot:run
```

First run takes a few minutes (downloads dependencies). Runs on **http://localhost:8080**.

### Terminal 2 — AI Service

```bash
cd civiclens-ai

# Set up Python virtual environment (first time only)
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Mac/Linux

pip install -r requirements.txt

# Set your HuggingFace token (get one free at huggingface.co/settings/tokens)
set HF_API_TOKEN=hf_your_token_here          # Windows CMD
# export HF_API_TOKEN=hf_your_token_here     # Mac/Linux

python -m uvicorn main:app --port 8000
```

Runs on **http://localhost:8000**.

### Terminal 3 — Frontend

```bash
cd civiclens-frontend
npm install
npm run dev
```

Runs on **http://localhost:5173**. Open this in your browser.

---

## Deployment

We deployed using:

- **Frontend** → Vercel (just connect the repo, set root to `civiclens-frontend`)
- **Backend** → Render (Docker, uses `civiclens-backend/Dockerfile`)
- **AI Service** → Render (Docker, uses `civiclens-ai/Dockerfile`)
- **Mobile** → Expo EAS Build (`eas build -p android --profile preview`)

Environment variables to set on each platform:

| Service | Variable | Value |
|---|---|---|
| Backend | `JWT_SECRET` | any secret string |
| Backend | `AI_SERVICE_URL` | URL of your AI service |
| Backend | `CORS_ALLOWED_ORIGINS` | your frontend URL |
| AI Service | `HF_API_TOKEN` | your HuggingFace token |
| Frontend | `VITE_API_URL` | your backend URL |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `java: command not found` | Install Java 21, restart terminal |
| `mvn: command not found` | Install Maven, add to PATH, restart terminal |
| `JAVA_HOME is not set` | Set it to your JDK install folder |
| `No module named 'fastapi'` | Activate the venv first: `.venv\Scripts\activate` |
| Frontend can't reach backend | Make sure backend is running on port 8080 |

