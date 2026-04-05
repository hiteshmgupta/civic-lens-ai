# CivicLens — Complete Setup & Installation Guide

This guide covers how to install every tool from scratch, the exact versions used, and step-by-step commands to get CivicLens running locally. Follow this if you've never set up a development environment before.

---

## Table of Contents

1. [Exact Versions Used](#exact-versions-used)
2. [Install Java 21 (JDK)](#1-install-java-21-jdk)
3. [Install Maven 3.9+](#2-install-maven-39)
4. [Install PostgreSQL 14+](#3-install-postgresql-14)
5. [Install Node.js 18+](#4-install-nodejs-18)
6. [Install Python 3.11](#5-install-python-311)
7. [Install Git](#6-install-git)
8. [Clone & Run the Project](#7-clone--run-the-project)
9. [Python Virtual Environment Guide](#8-python-virtual-environment-guide)
10. [Deployment Details](#9-deployment-details)

---

## Exact Versions Used

These are the exact versions this project was built and tested with. Using different major versions may cause errors.

### System Tools

| Tool | Exact Version | Why This Version |
|---|---|---|
| Java (JDK) | **21** (Eclipse Temurin) | Required by Spring Boot 4.0. The Dockerfile uses `eclipse-temurin:21` |
| Maven | **3.9.x** | Required to build the Spring Boot backend. Dockerfile uses `maven:3.9` |
| PostgreSQL | **14+** | Database. Render uses managed PostgreSQL 14 |
| Node.js | **18 LTS** or **20 LTS** | Required for Vite 5 and Expo SDK 54 |
| npm | **9+** | Comes bundled with Node.js 18+ |
| Python | **3.11** | Exactly 3.11 — the Dockerfile and Render both use `python:3.11-slim` |
| Git | Any recent version | For cloning the repo |

### Backend Dependencies (Java — auto-installed by Maven)

| Dependency | Version | Managed By |
|---|---|---|
| Spring Boot | 4.0.0 | `pom.xml` parent |
| Spring Security | (auto) | Spring Boot BOM |
| Spring Data JPA | (auto) | Spring Boot BOM |
| Spring WebFlux (WebClient) | (auto) | Spring Boot BOM |
| PostgreSQL JDBC Driver | (auto) | Spring Boot BOM |
| Lombok | 1.18.32 | `pom.xml` |
| JJWT (JWT library) | 0.12.5 | `pom.xml` |
| OpenHTMLtoPDF (PDF export) | 1.0.10 | `pom.xml` |
| Jackson Databind | (auto) | Spring Boot BOM |
| H2 Database (tests only) | (auto) | Spring Boot BOM |
| Maven Compiler Plugin | 3.13.0 | `pom.xml` |

### Frontend Dependencies (Node.js — auto-installed by npm)

| Dependency | Version | Type |
|---|---|---|
| React | 18.2.0 | Runtime |
| React DOM | 18.2.0 | Runtime |
| React Router DOM | 6.22.3 | Runtime |
| Axios | 1.6.7 | Runtime |
| Recharts | 2.12.2 | Runtime |
| Vite | 5.1.6 | Dev |
| @vitejs/plugin-react | 4.2.1 | Dev |
| Tailwind CSS | 3.4.1 | Dev |
| PostCSS | 8.4.35 | Dev |
| Autoprefixer | 10.4.18 | Dev |

### AI Service Dependencies (Python — auto-installed by pip)

| Dependency | Version Range | Purpose |
|---|---|---|
| FastAPI | ≥0.109.0, <1.0 | Web framework |
| Uvicorn | ≥0.27.0, <1.0 | ASGI server |
| Pydantic | ≥2.6.0, <3.0 | Data validation |
| httpx | ≥0.27.0 | Async HTTP client for HuggingFace API |
| scikit-learn | ≥1.4.0 | Topic modeling (TF-IDF + KMeans) |
| NumPy | ≥1.26.0 | Numerical computations |

### Mobile App Dependencies (Node.js — auto-installed by npm)

| Dependency | Version | Purpose |
|---|---|---|
| Expo SDK | 54.0.33 | React Native framework |
| React Native | 0.81.5 | Mobile runtime |
| React | 19.1.0 | UI library |
| react-native-webview | 13.15.0 | WebView component |
| react-native-safe-area-context | 5.6.0 | Safe area handling |
| Expo Router | 6.0.23 | File-based routing |
| expo-status-bar | 3.0.9 | Status bar control |
| TypeScript | 5.9.2 | Type checking |

---

## 1. Install Java 21 (JDK)

The backend requires **Java 21** (specifically Eclipse Temurin, the same used in our Docker builds).

### Windows

1. Go to **https://adoptium.net/**
2. Click the big **"Latest LTS Release"** button — make sure it says **Temurin 21**
3. Download the `.msi` installer for Windows x64
4. Run the installer:
   - ✅ Check **"Set JAVA_HOME variable"**
   - ✅ Check **"Add to PATH"**
   - Click Install
5. **Restart your terminal** (close and reopen Command Prompt or PowerShell)
6. Verify:
   ```bash
   java --version
   # Should show: openjdk 21.x.x
   
   javac --version
   # Should show: javac 21.x.x
   ```

### macOS

```bash
# Using Homebrew:
brew install --cask temurin@21

# Verify:
java --version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y temurin-21-jdk

# Or manually:
sudo apt install -y openjdk-21-jdk

# Verify:
java --version
```

---

## 2. Install Maven 3.9+

Maven is the build tool for the Java backend. It downloads all Java dependencies automatically.

### Windows (Manual Install — Recommended)

1. Go to **https://maven.apache.org/download.cgi**
2. Under "Files", download **`apache-maven-3.9.9-bin.zip`** (the binary zip)
3. Extract the zip to a permanent location, e.g., `C:\Program Files\Maven\apache-maven-3.9.9`
4. **Add Maven to your PATH:**
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - Go to **Advanced** tab → **Environment Variables**
   - Under "System variables", find `Path` and click **Edit**
   - Click **New** and add: `C:\Program Files\Maven\apache-maven-3.9.9\bin`
   - Click OK on all dialogs
5. **Set JAVA_HOME** (if not already set by Java installer):
   - In the same Environment Variables window, click **New** under System variables
   - Variable name: `JAVA_HOME`
   - Variable value: `C:\Program Files\Eclipse Adoptium\jdk-21.x.x` (your JDK path)
6. **Restart your terminal** completely
7. Verify:
   ```bash
   mvn --version
   # Should show:
   # Apache Maven 3.9.9
   # Java version: 21.x.x
   ```

### macOS

```bash
brew install maven
mvn --version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y maven

# Or for latest version:
# Download from https://maven.apache.org/download.cgi and extract manually

mvn --version
```

### Common Maven Error

If you see `JAVA_HOME is not set`, it means Maven can't find Java:
```bash
# Windows — check your Java install path and set:
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-21.0.x.x-hotspot

# Verify JAVA_HOME is set:
echo %JAVA_HOME%
```

---

## 3. Install PostgreSQL 14+

### Windows

1. Go to **https://www.postgresql.org/download/windows/**
2. Click **"Download the installer"** (from EDB)
3. Download PostgreSQL **14** or **16** for Windows x86-64
4. Run the installer:
   - Set the **superuser password** (remember this — default in our project is `postgres`)
   - Keep the default port: **5432**
   - ✅ Check "Stack Builder" if prompted (optional)
5. After installation, open **pgAdmin** (installed with PostgreSQL) or use the command line:
   ```bash
   # Open psql (PostgreSQL command line):
   psql -U postgres
   # Enter your password when prompted
   
   # Create the database:
   CREATE DATABASE civiclens;
   
   # Verify:
   \l
   # Should show "civiclens" in the list
   
   # Exit:
   \q
   ```

### macOS

```bash
brew install postgresql@16
brew services start postgresql@16

# Create database:
createdb civiclens
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo systemctl start postgresql

# Create database:
sudo -u postgres createdb civiclens
```

---

## 4. Install Node.js 18+

### Windows

1. Go to **https://nodejs.org/**
2. Download the **LTS** version (18.x or 20.x)
3. Run the `.msi` installer with all default options
4. **Restart your terminal**
5. Verify:
   ```bash
   node --version
   # Should show: v18.x.x or v20.x.x
   
   npm --version
   # Should show: 9.x.x or 10.x.x
   ```

### macOS

```bash
brew install node@20
node --version
npm --version
```

### Linux (Ubuntu/Debian)

```bash
# Using NodeSource:
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

node --version
npm --version
```

---

## 5. Install Python 3.11

**Important:** Use exactly **Python 3.11** — this is what we use in Docker and on Render. Python 3.12+ may have compatibility issues with some of our dependencies.

### Windows

1. Go to **https://www.python.org/downloads/**
2. **Don't click the big button** — scroll down to "Looking for a specific release?"
3. Find **Python 3.11.x** (e.g., 3.11.9) and click it
4. Download the **Windows installer (64-bit)**
5. Run the installer:
   - ✅ **Check "Add python.exe to PATH"** (very important!)
   - Click "Install Now"
6. **Restart your terminal**
7. Verify:
   ```bash
   python --version
   # Should show: Python 3.11.x
   
   pip --version
   # Should show pip and the Python 3.11 path
   ```

**If `python` command doesn't work on Windows**, try `python3` or `py -3.11`.

### macOS

```bash
brew install python@3.11
python3.11 --version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-pip
python3.11 --version
```

---

## 6. Install Git

### Windows

1. Go to **https://git-scm.com/download/win**
2. Download and run the installer with default options
3. Verify:
   ```bash
   git --version
   ```

### macOS

```bash
# Usually pre-installed. If not:
brew install git
```

### Linux

```bash
sudo apt install -y git
```

---

## 7. Clone & Run the Project

Now that everything is installed, here's the complete flow:

### Step 1 — Clone

```bash
git clone https://github.com/your-username/civic-lens-ai.git
cd civic-lens-ai
```

### Step 2 — Create the Database

```bash
psql -U postgres
# Enter your password

CREATE DATABASE civiclens;
\q
```

### Step 3 — Start the Backend

Open a new terminal:

```bash
cd civic-lens-ai/civiclens-backend

# If your PostgreSQL password is NOT "postgres", set it:
# Windows CMD:     set DB_PASSWORD=your_password
# PowerShell:      $env:DB_PASSWORD="your_password"
# macOS/Linux:     export DB_PASSWORD=your_password

mvn spring-boot:run
```

First run downloads all Java dependencies (~5 minutes). Then you'll see:
```
Started CivicLensApplication in X.XX seconds
```
The backend is now running at **http://localhost:8080**. Leave this terminal open.

### Step 4 — Start the AI Service

Open a second terminal:

```bash
cd civic-lens-ai/civiclens-ai

# Create virtual environment (one-time)
python -m venv .venv

# Activate the virtual environment
# Windows CMD:
.venv\Scripts\activate
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# You should see (.venv) at the start of your prompt now

# Install Python packages (one-time, or after pulling new changes)
pip install -r requirements.txt

# Set HuggingFace token (get one free at https://huggingface.co/settings/tokens)
# Windows CMD:     set HF_API_TOKEN=hf_your_token_here
# PowerShell:      $env:HF_API_TOKEN="hf_your_token_here"
# macOS/Linux:     export HF_API_TOKEN=hf_your_token_here

# Start the AI server
python -m uvicorn main:app --port 8000
```

You'll see: `Uvicorn running on http://0.0.0.0:8000`. Leave this terminal open.

### Step 5 — Start the Frontend

Open a third terminal:

```bash
cd civic-lens-ai/civiclens-frontend

# Install Node packages (one-time, or after pulling new changes)
npm install

# Start the dev server
npm run dev
```

You'll see: `Local: http://localhost:5173/`. Open this URL in your browser.

### Summary — All Three Terminals

| Terminal | Folder | Command | URL |
|---|---|---|---|
| Terminal 1 | `civiclens-backend/` | `mvn spring-boot:run` | http://localhost:8080 |
| Terminal 2 | `civiclens-ai/` | `python -m uvicorn main:app --port 8000` | http://localhost:8000 |
| Terminal 3 | `civiclens-frontend/` | `npm run dev` | http://localhost:5173 |

---

## 8. Python Virtual Environment Guide

### What is a Virtual Environment?

A virtual environment (venv) is an isolated Python environment. It keeps this project's Python packages separate from your system Python and other projects, preventing version conflicts.

### When to Create One

**Once** — when you first set up the AI service. After that, you just activate it.

```bash
cd civiclens-ai

# Create the venv (one-time only):
python -m venv .venv
```

This creates a `.venv/` folder inside `civiclens-ai/`. The `.gitignore` already excludes it from Git.

### When to Activate

**Every time** you open a new terminal to work on the AI service. You must activate before running any `pip` or `python` commands.

```bash
# Windows Command Prompt:
.venv\Scripts\activate

# Windows PowerShell:
.venv\Scripts\Activate.ps1

# macOS / Linux:
source .venv/bin/activate
```

**How to tell it's activated:** Your terminal prompt will show `(.venv)` at the beginning:
```
(.venv) C:\Users\you\civic-lens-ai\civiclens-ai>
```

### When to Install Packages

- **First time** after creating the venv
- **After pulling new code** (if `requirements.txt` was updated)

```bash
# Make sure venv is activated first!
pip install -r requirements.txt
```

### When to Deactivate

When you're done working on the AI service:
```bash
deactivate
```

### Common Virtual Environment Issues

**"No module named 'fastapi'"** — You forgot to activate the venv:
```bash
.venv\Scripts\activate          # then try running again
```

**"python: command not found"** — Try `python3` or `py -3.11` instead.

**PowerShell "cannot be loaded because running scripts is disabled":**
```powershell
# Fix: Run this once in PowerShell as Administrator:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again:
.venv\Scripts\Activate.ps1
```

**"The virtual environment was not created successfully"** — Make sure you installed Python with the venv module:
```bash
# Linux:
sudo apt install python3.11-venv

# Then create the venv:
python3.11 -m venv .venv
```

---

## 9. Deployment Details

This section documents exactly how each service is deployed, so you can replicate it or troubleshoot issues.

### Frontend → Vercel

| Setting | Value |
|---|---|
| Platform | [Vercel](https://vercel.com) |
| Root Directory | `civiclens-frontend` |
| Framework | Vite |
| Build Command | `npm run build` |
| Output Directory | `dist` |
| Node.js Version | 18.x (Vercel default) |
| Environment Variable | `VITE_API_URL` = `https://civiclens-backend-j5q2.onrender.com` |

The `vercel.json` file contains a rewrite rule so all routes serve `index.html` (required for React Router SPA):
```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

### Backend → Render (Docker)

| Setting | Value |
|---|---|
| Platform | [Render](https://render.com) |
| Root Directory | `civiclens-backend` |
| Type | Web Service (Docker) |
| Dockerfile | `civiclens-backend/Dockerfile` |
| Docker Base Images | `maven:3.9-eclipse-temurin-21` (build), `eclipse-temurin:21-jre` (runtime) |
| Port | 8080 |

Environment variables on Render:

| Variable | Value |
|---|---|
| `DATABASE_URL` | `jdbc:postgresql://...` (Render managed PostgreSQL) |
| `DB_USERNAME` | (from Render PostgreSQL) |
| `DB_PASSWORD` | (from Render PostgreSQL) |
| `JWT_SECRET` | (your secret key) |
| `AI_SERVICE_URL` | `https://your-ai-service.onrender.com` |
| `PORT` | `8080` |
| `CORS_ALLOWED_ORIGINS` | `https://civic-lens-ai-bay.vercel.app` |

### AI Service → Render (Docker)

| Setting | Value |
|---|---|
| Platform | [Render](https://render.com) |
| Root Directory | `civiclens-ai` |
| Type | Web Service (Docker) |
| Dockerfile | `civiclens-ai/Dockerfile` |
| Docker Base Image | `python:3.11-slim` |
| Port | 8000 |

Environment variables on Render:

| Variable | Value |
|---|---|
| `HF_API_TOKEN` | `hf_your_token` |
| `PORT` | `8000` |

### Database → Render (Managed PostgreSQL)

| Setting | Value |
|---|---|
| Platform | Render |
| Plan | Free |
| PostgreSQL Version | 14+ |
| Connection | Internal URL provided by Render |

### Mobile App → EAS Build (Expo)

| Setting | Value |
|---|---|
| Platform | [Expo (EAS Build)](https://expo.dev) |
| Build Profile `preview` | Generates `.apk` (Android sideloading) |
| Build Profile `production` | Generates `.aab` (Play Store) |
| Build Server | Expo Cloud (free, 30 builds/month) |

```bash
# Install EAS CLI:
npm install -g eas-cli

# Login:
eas login

# Build APK:
cd civiclens-mobile
eas build -p android --profile preview
```

---

## Troubleshooting Quick Reference

| Problem | Solution |
|---|---|
| `java: command not found` | Install Java 21 from adoptium.net, restart terminal |
| `mvn: command not found` | Install Maven, add `bin/` to PATH, restart terminal |
| `JAVA_HOME is not set` | Set JAVA_HOME to your JDK folder (see Maven section) |
| `node: command not found` | Install Node.js from nodejs.org, restart terminal |
| `python: command not found` | Try `python3` or `py`. Install from python.org |
| `No module named 'fastapi'` | Activate venv: `.venv\Scripts\activate`, then `pip install -r requirements.txt` |
| `psql: command not found` | Install PostgreSQL, or use pgAdmin GUI instead |
| `FATAL: database "civiclens" does not exist` | Run `CREATE DATABASE civiclens;` in psql |
| Backend starts but frontend can't connect | Make sure backend is on port 8080, frontend uses Vite proxy |
| PowerShell "scripts disabled" error | Run: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `npm ERR! code ENOENT` | You're in the wrong folder. `cd` into the right directory |
| Render backend takes 30s to respond | Free tier servers sleep after 15 min of inactivity. First request wakes it up |
