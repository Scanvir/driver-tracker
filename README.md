# Driver Tracker

Production-ready Driver Tracker with **FastAPI + PostgreSQL**, **React dashboard**, and **Google Forms integration**.

## Project structure

```text
driver-tracker/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── database.py
│   │   ├── routes/
│   │   │   ├── trips.py
│   │   │   ├── drivers.py
│   │   │   └── google_forms.py
│   │   └── utils.py
│   ├── tests/
│   ├── requirements.txt
│   ├── Procfile
│   ├── runtime.txt
│   ├── .env.example
│   └── run.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DriversTable.jsx
│   │   │   └── Stats.jsx
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   ├── .env.example
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Supported action types

- `departure` (Виїзд)
- `arrival` (Заїзд)
- `transfer` (Переміщення)

Default driver phone: `+380978600618`

## Backend setup (local)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Frontend setup (local)

```bash
cd frontend
cp .env.example .env
npm install
npm start
```

## Run all services with Docker Compose

```bash
docker compose up --build
```

- Frontend: `http://localhost:3000`
- Backend API docs: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

## Google Forms + Google Sheets integration

### 1) Create Google Form

Create fields:
- `action` (`departure|arrival|transfer`) or Ukrainian equivalents
- `time` (`HH:MM`)
- `odometer` (km)
- `route` (text)
- optional `phone` (if omitted, backend uses `+380978600618`)

### 2) Link Form to Google Sheets

In Google Form: **Responses → Link to Sheets**.

### 3) Publish CSV URL from Google Sheets

1. Open linked Google Sheet
2. File → Share → Publish to web
3. Select sheet with responses and publish as CSV
4. Put URL into `GOOGLE_SHEETS_CSV_URL` in backend env

### 4) Sync into PostgreSQL

Call backend endpoint:

```bash
curl -X POST http://localhost:8000/api/google-forms/sync
```

Or click **Sync Google Forms** in dashboard.

## Railway deployment guide (step-by-step)

### Backend on Railway

1. Create new Railway project from this GitHub repo
2. Add PostgreSQL plugin in Railway
3. Set backend service root to `backend/`
4. Add env vars (from `backend/.env.example`):
   - `DATABASE_URL` (Railway PostgreSQL connection string)
   - `GOOGLE_SHEETS_CSV_URL`
   - `DEFAULT_DRIVER_PHONE=+380978600618`
5. Start command is from `Procfile`:
   - `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend on Railway

1. Create second service from same repo with root `frontend/`
2. Set env:
   - `REACT_APP_API_URL=https://<backend-domain>/api`
3. Deploy (Dockerfile builds static app and serves via nginx)

### Cost note

Target hosting plan: Railway ~`$15/month` (depends on usage).

## WhatsApp distribution

Send Google Form link in WhatsApp to drivers. They submit trips, then sync from dashboard/API.
