## CivicLens – Legislative Consultation Intelligence Platform

CivicLens is a full‑stack application for analyzing public feedback on legislation.  
The backend is a Spring Boot API, and the frontend is a React + Vite SPA.

---

## Tech stack & versions

- **Backend**
  - Java **17+** (tested with Java 22.0.1)
  - Spring Boot **3.2.5**
  - Maven **3.9+**
  - PostgreSQL **14+**

- **Frontend**
  - Node.js **18+** (or current LTS)
  - npm **9+**
  - React **18**
  - Vite **5**

---

## Project structure

- `civiclens-backend/` – Spring Boot REST API
- `civiclens-frontend/` – React + Vite frontend

---

## Backend – running locally

From the `civiclens-backend` folder:

```bash
# 1. Run tests and build the jar
mvn clean verify

# 2. Start the API
mvn spring-boot:run
# or, if you already built:
# java -jar target/civiclens-backend-0.1.0.jar
```

### Database configuration (PostgreSQL)

The backend expects a PostgreSQL database. Default connection (from `application.yml`):

- URL: `jdbc:postgresql://localhost:5432/civiclens`
- Username: `postgres`
- Password: `postgres`

You can override these with environment variables:

- `DATABASE_URL` – full JDBC URL (overrides all)
- `DB_USERNAME` – database username
- `DB_PASSWORD` – database password

**If registration or login fails:**  
Most often the backend is not fully started because the database connection failed.  
Check the backend logs for a line like:

- `FATAL: password authentication failed for user "postgres"`

If you see this, either:

1. Change your local PostgreSQL user/password to match the defaults, **or**
2. Keep your existing credentials and set environment variables before starting:

```bash
set DB_USERNAME=your_user
set DB_PASSWORD=your_password
rem optional:
set DATABASE_URL=jdbc:postgresql://localhost:5432/your_db

mvn spring-boot:run
```

Once the API is up (on `http://localhost:8080`), the `/api/auth/register` and `/api/auth/login` endpoints will work from the frontend.

### Other backend settings

These can also be overridden via environment variables:

- `JWT_SECRET` – secret key for signing JWTs (default is a development value; change in production)
- `AI_SERVICE_URL` – URL for the external AI service (default `http://localhost:8000`)

---

## Frontend – running locally

From the `civiclens-frontend` folder:

```bash
# 1. Install dependencies
npm install

# 2. Start the dev server
npm run dev
```

By default Vite runs on `http://localhost:5173`.

### API calls & auth

- All frontend API calls go to paths under `/api/...`.
- `vite.config.js` is configured with a dev proxy so that:
  - `/api` → `http://localhost:8080`
- The auth API endpoints on the backend are:
  - `POST /api/auth/register`
  - `POST /api/auth/login`

The frontend registration and login pages call these endpoints via `src/api/authApi.js`:

- Registration: sends `{ username, email, password }`
- Login: sends `{ email, password }`

The backend returns an `AuthResponse` JSON containing:

- `token` – JWT token
- `userId`
- `username`
- `email`
- `role`

The frontend `AuthContext` stores this in `localStorage` and attaches the JWT as `Authorization: Bearer <token>` on subsequent requests.

### Common reasons registration/login appear “broken”

1. **Backend not running or failing on startup**
   - Fix your PostgreSQL credentials as described above.

2. **Frontend running without dev proxy or wrong API base URL in production**
   - During `npm run dev`, the Vite proxy forwards `/api` to `http://localhost:8080` automatically.
   - For a production build served from a different host, set `VITE_API_URL` in an `.env` file:

     ```bash
     VITE_API_URL=http://your-backend-host:8080
     ```

3. **Validation errors from backend**
   - Backend enforces:
     - `username`: 3–50 characters, not blank
     - `email`: valid email, not blank
     - `password`: 6–100 characters, not blank
   - The frontend shows a message from `err.response.data.message` when available, or a generic “Registration failed” / “Login failed”.

---

## Building for production

### Backend

```bash
cd civiclens-backend
mvn clean package
# produces target/civiclens-backend-0.1.0.jar
```

Run the jar on your server:

```bash
java -jar civiclens-backend-0.1.0.jar
```

Ensure the environment variables for database and JWT secret are set appropriately.

### Frontend

```bash
cd civiclens-frontend
npm install
npm run build
```

The production files are generated in `dist/`. You can:

- Serve them via any static file server (Nginx, Apache, etc.), or
- Configure your own hosting (e.g. Netlify, Vercel, S3 + CloudFront).

For production, set `VITE_API_URL` so that the frontend talks to your deployed backend:

```bash
VITE_API_URL=https://api.your-domain.com
```

---

## Getting this project onto GitHub

From the project root (`civiclens-*` folders and `.gitignore` present):

```bash
git init
git add .
git commit -m "Initial CivicLens import"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

The root `.gitignore` already excludes:

- Maven `target/` folders
- Node `node_modules/` and `dist/`
- Environment files (`.env`, `.env.*`)
- Common IDE files (`.idea/`, `.vscode/`, `*.iml`, etc.)

