# Backend - AI Study Planner API

This backend is a FastAPI REST service for the AI Study Planner project.

## Responsibilities
- Validate request payloads with Pydantic
- Execute business logic (priority, schedule generation, notifications)
- Access data via SQLAlchemy ORM
- Persist data in SQLite

## Run Backend
```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API URL: `http://127.0.0.1:8000`

Swagger docs: `http://127.0.0.1:8000/docs`

## Environment Variables
Copy `.env.example` to `.env` and adjust if needed:
```env
DATABASE_URL=sqlite:///./study_planner.db
BACKEND_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## Database
- Engine: SQLite
- Default file: `backend/study_planner.db`
- ORM: SQLAlchemy
- Tables: `students`, `tasks`, `exams`, `study_sessions`

## Testing
Automated tests:
```bash
cd backend
.venv\Scripts\python -m pytest -q
```

Manual HTTP test script:
```bash
cd backend
.venv\Scripts\python tests/manual_client.py
```

## Backend Modules
- `app/main.py`: app startup, middleware, router registration
- `app/models.py`: SQLAlchemy ORM models
- `app/schemas.py`: request/response models
- `app/crud.py`: database operations
- `app/services/priority_service.py`: priority score formulas
- `app/services/schedule_service.py`: schedule generation algorithm
- `app/services/notification_service.py`: reminder generation rules
- `app/routers/*.py`: endpoint definitions
