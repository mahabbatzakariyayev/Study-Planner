# AI Study Planner

AI Study Planner is a full-stack **Distributed Programming** university project.

## Project Objective
Build a distributed student planning system where:
- a **Next.js client** sends HTTP JSON requests,
- a **FastAPI backend** applies business logic,
- and a **SQLite database** stores data.

The frontend never touches the database directly.

## Why This Is a Distributed Programming Project
The project demonstrates clear service separation:
- Client and server are separate processes.
- Communication happens through REST endpoints over HTTP.
- Data persistence is isolated behind backend APIs and ORM.

## Architecture Diagram
```text
Next.js React Client (frontend)
        |
        | HTTP JSON REST API
        v
FastAPI Backend Server (business logic, validation, scheduling)
        |
        | SQLAlchemy ORM
        v
SQLite Database (study_planner.db)
```

## Repository Structure
- `backend/`: FastAPI app, models, services, tests.
- `frontend/`: Next.js App Router client with TypeScript and Tailwind.
- `docs/`: Architecture, API endpoints, testing queries, report materials.

## Backend Setup
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

API base URL: `http://127.0.0.1:8000`

Swagger docs: `http://127.0.0.1:8000/docs`

## Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:3000`

Set environment variable in `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Run Tests
### Backend automated tests
```bash
cd backend
.venv\Scripts\python -m pytest -q
```

### Manual API client test
Start backend first, then:
```bash
cd backend
.venv\Scripts\python tests/manual_client.py
```

## Demo Flow
1. Start backend and open `/docs`.
2. Show REST endpoints: students, tasks, exams, schedules, notifications, analytics.
3. Start frontend and open `http://localhost:3000`.
4. Create/select demo student.
5. Add tasks and exams.
6. Generate schedule.
7. Show notifications and analytics.
8. Explain distributed architecture and backend-owned business logic.

## Technologies Used
- Backend: FastAPI, SQLAlchemy, SQLite, Pydantic, pytest
- Frontend: Next.js App Router, React, TypeScript, Tailwind CSS
- Communication: REST API over HTTP JSON

## Additional Documentation
- [Architecture](./docs/architecture.md)
- [API Endpoints](./docs/api_endpoints.md)
- [Test Queries](./docs/test_queries.md)
- [Project Explanation](./docs/project_explanation.md)
- [Presentation Speech](./docs/presentation_speech.md)
- [Report Outline](./docs/report_outline.md)
"# Study-Planner" 
