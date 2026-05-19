# AI Study Planner

AI Study Planner is a full-stack Distributed Programming project with a strict API-first architecture:

- **Client:** Next.js (React + TypeScript)
- **Server:** FastAPI (REST API)
- **Database:** SQLite via SQLAlchemy ORM

The frontend does **not** access the database directly. All business logic and persistence go through the backend API.

## 1. Architecture

```text
Next.js Client
    |
    | HTTP JSON requests
    v
FastAPI Backend
    |
    | SQLAlchemy ORM
    v
SQLite Database
```

## 2. Core Features

- Student CRUD
- Task CRUD + automatic priority score
- Exam CRUD
- Schedule generation with constraints (hours/day, split sessions, deadlines)
- Notifications (deadlines, exams, high-priority, sessions)
- Analytics dashboard

## 3. Tech Stack

### Backend
- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- python-dotenv
- pytest

### Frontend
- Next.js (App Router)
- React
- TypeScript
- Tailwind CSS

### Database
- SQLite

## 4. Project Structure

```text
ai-study-planner/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── types/
│   ├── package.json
│   └── .env.local.example
├── docs/
├── PROJECT_STATUS.md
└── README.md
```

## 5. Run the Backend

### Windows (PowerShell)

```powershell
cd "c:\Users\MahabbatZakariyayevN\Desktop\Workprojects\AI Study Planner\ai-study-planner\backend"
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Linux / macOS

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### If you run from repo root

```powershell
cd "c:\Users\MahabbatZakariyayevN\Desktop\Workprojects\AI Study Planner\ai-study-planner"
.\backend\.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --app-dir backend
```

## 6. Swagger and API Docs

After backend is running:

- Health: `http://127.0.0.1:8000/health`
- Swagger UI: `http://127.0.0.1:8000/docs`
- Swagger alias: `http://127.0.0.1:8000/swagger`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI JSON: `http://127.0.0.1:8000/openapi.json`

## 7. Run the Frontend

```powershell
cd "c:\Users\MahabbatZakariyayevN\Desktop\Workprojects\AI Study Planner\ai-study-planner\frontend"
npm install
npm run dev
```

Frontend URL:
- `http://localhost:3000`

## 8. Environment Variables

### Backend (`backend/.env`)

Copy from `backend/.env.example`:

```env
DATABASE_URL=sqlite:///./study_planner.db
BACKEND_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Frontend (`frontend/.env.local`)

Copy from `frontend/.env.local.example`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

If backend runs on another port (example: `8010`), set:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8010
```

## 9. Testing

### Backend automated tests

```powershell
cd "c:\Users\MahabbatZakariyayevN\Desktop\Workprojects\AI Study Planner\ai-study-planner\backend"
.\.venv\Scripts\python -m pytest -q
```

### Manual API flow script

```powershell
cd "c:\Users\MahabbatZakariyayevN\Desktop\Workprojects\AI Study Planner\ai-study-planner\backend"
.\.venv\Scripts\python tests\manual_client.py
```

## 10. Demo Flow

1. Start backend.
2. Open Swagger (`/docs` or `/swagger`).
3. Start frontend.
4. Create/select student.
5. Add tasks.
6. Add exams.
7. Generate schedule.
8. Show notifications.
9. Show analytics.

## 11. Common Issues (Quick Fix)

### `ModuleNotFoundError: No module named 'app'`
Run Uvicorn from `backend/` folder, or use `--app-dir backend` from root.

### Frontend says `Cannot reach backend...`
- Ensure backend is running.
- Open `http://127.0.0.1:8000/health` directly in browser.
- Ensure `frontend/.env.local` has correct `NEXT_PUBLIC_API_URL`.
- Restart frontend after changing `.env.local`.

### Port 8000 busy
Use another port (e.g. `8010`) and update frontend env.

## 12. Distributed Programming Justification

This project demonstrates distributed programming by:

- Separating client and server into independent processes
- Using HTTP/JSON contracts between components
- Keeping business logic centralized in backend services
- Isolating persistence behind API + ORM

## 13. Known Limitations

- Rule-based priority scoring (not ML model)
- No calendar integration yet
- No authentication layer
- SQLite used for simplicity (PostgreSQL recommended for production)

## 14. Additional Documentation

- `docs/architecture.md`
- `docs/api_endpoints.md`
- `docs/test_queries.md`
- `docs/project_explanation.md`
- `docs/presentation_speech.md`
- `docs/report_outline.md`
- `PROJECT_STATUS.md`
