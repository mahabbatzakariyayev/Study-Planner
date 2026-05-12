# Project Explanation

## 1. Introduction
AI Study Planner is a distributed full-stack system designed for student task and exam planning. The project is intentionally structured for a Distributed Programming course where API-based communication is the core objective.

## 2. General Description of Chosen Theme
Students often manage multiple assignments and exams with overlapping deadlines. This system centralizes planning by:
- collecting tasks and exams,
- computing priority automatically,
- generating constrained study sessions,
- producing reminders and analytics.

## 3. Chosen Technologies
- **FastAPI**: REST API framework.
- **SQLAlchemy ORM**: persistence abstraction.
- **SQLite**: lightweight relational storage for project scope.
- **Pydantic**: request/response validation.
- **Next.js + React + TypeScript**: separated client application.
- **Tailwind CSS**: UI styling.
- **pytest + TestClient**: automated backend verification.

## 4. REST API Design
API design follows resource-based endpoints:
- `/students` for student profiles
- `/tasks` for assignments
- `/exams` for exams
- `/schedules` for generated sessions
- `/notifications` for reminders
- `/analytics` for dashboard metrics

Endpoints are stateless and exchange JSON payloads.

## 5. Endpoint Definition
Each endpoint defines:
- HTTP method and route
- input schema validation
- backend business execution
- JSON response or meaningful HTTP error

Details are documented in `docs/api_endpoints.md`.

## 6. Design Decisions
1. **Strict backend ownership** of business logic.
2. **Centralized API client** in frontend (`lib/api.ts`) for maintainability.
3. **Service layer separation** for priority, schedule, notifications.
4. **Database isolation** behind CRUD methods.
5. **LocalStorage active student context** for practical demo workflow.

## 7. Implementation Details
Backend modules:
- `models.py`: Student, Task, Exam, StudySession
- `schemas.py`: request/response contracts
- `crud.py`: ORM operations
- `services/priority_service.py`: priority formula and labels
- `services/schedule_service.py`: generation algorithm with daily capacity
- `services/notification_service.py`: reminder rules
- routers: endpoint grouping and HTTP error mapping

Frontend modules:
- App Router pages for all required views
- reusable forms/lists/cards
- centralized API wrappers
- loading/error/empty states on each page

## 8. Priority Calculation Method
Task priority score range: 0-10.

Formula:
`priority = urgency*0.40 + difficulty*0.25 + exam_related*0.20 + estimated_hours*0.15`

Urgency is based on days until deadline; difficulty and estimated hours are normalized; exam-related tasks get higher weighting.

## 9. Schedule Generation Method
Generation process:
1. Validate student exists.
2. Clear old sessions.
3. Fetch active tasks and recalculate priorities.
4. Sort tasks by priority then deadline.
5. Allocate sessions from today to deadline.
6. Enforce limits: max 2h per session, max study_hours_per_day.
7. Add exam revision sessions before exam dates.
8. Save sessions and return warnings if unscheduled hours remain.

## 10. Tests
Automated tests cover:
- health endpoint
- student CRUD flow
- task creation, priority, status update, delete
- exam CRUD flow
- schedule generation/get/complete/delete
- notifications and analytics endpoints

Manual script (`tests/manual_client.py`) executes real HTTP requests against a running server.

## 11. Client Implementation
The Next.js client:
- manages active student context,
- submits forms to backend,
- displays schedule warnings,
- visualizes notifications and analytics,
- never accesses SQLite directly.

## 12. Conclusion
The project demonstrates distributed programming through strict separation between presentation layer (Next.js), service/API layer (FastAPI), and persistence layer (SQLite). The architecture is extensible for authentication, calendar integration, and production-grade databases in future iterations.
