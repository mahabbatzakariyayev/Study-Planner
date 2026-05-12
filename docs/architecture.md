# Architecture - AI Study Planner

## 1. Client-Server Architecture
This project follows a three-layer distributed architecture:

1. **Next.js Client**
2. **FastAPI REST API Server**
3. **SQLite Database**

The client and server run as separate applications and communicate over HTTP.

## 2. Request/Response Flow
1. User submits form in Next.js UI.
2. Client calls backend endpoint using Fetch API (`lib/api.ts`).
3. FastAPI router validates input via Pydantic schemas.
4. Service layer executes business rules (priority, schedule, notifications).
5. CRUD layer reads/writes through SQLAlchemy ORM.
6. JSON response is returned to client.
7. Client renders updated UI state.

## 3. JSON Payload Example
Task creation request:
```json
{
  "student_id": 1,
  "title": "Study FastAPI endpoints",
  "deadline": "2026-05-20",
  "difficulty": 4,
  "estimated_hours": 5,
  "is_exam_related": true,
  "status": "pending"
}
```

Task response:
```json
{
  "id": 10,
  "student_id": 1,
  "title": "Study FastAPI endpoints",
  "deadline": "2026-05-20",
  "difficulty": 4,
  "estimated_hours": 5,
  "is_exam_related": true,
  "status": "pending",
  "priority_score": 7.3
}
```

## 4. Backend Responsibility
Backend owns all critical logic:
- Validation and error handling
- Priority score calculation
- Schedule generation with capacity constraints
- Exam revision planning
- Notification generation
- Analytics aggregation
- Database access

## 5. Database Layer
SQLite is accessed only through SQLAlchemy in backend code.

Tables:
- `students`
- `tasks`
- `exams`
- `study_sessions`

## 6. Why Frontend Does Not Access DB Directly
The frontend is intentionally isolated from persistence to enforce distributed principles:
- Security: DB credentials never exposed to browser.
- Maintainability: business logic centralized server-side.
- Scalability: backend can be swapped to another DB without frontend rewrite.
- Academic objective: clear API-based distributed communication.

## 7. Distributed Programming Concepts Demonstrated
- Process separation (client and API server)
- Stateless HTTP JSON communication
- Contract-based endpoints (request/response schemas)
- Service-layer business logic decomposition
- Centralized backend orchestration for multiple entities (tasks/exams/sessions)
- Independent client and server deployment capability
