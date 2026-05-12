# Presentation Speech (5-7 Minutes)

Good day. Today I will present my Distributed Programming project called **AI Study Planner**.

The main problem I focused on is student workload management. Students usually have many assignments, exams, and deadlines at the same time, and they need a consistent way to prioritize and schedule study time. My solution is a full-stack distributed system that automatically calculates task priority, generates a realistic study plan, and provides reminders and analytics.

The key point for this course is architecture. I implemented a strict three-layer model:

1. A **Next.js React client** running on port 3000.
2. A **FastAPI backend server** running on port 8000.
3. A **SQLite database** accessed only by the backend through SQLAlchemy ORM.

The frontend never accesses the database directly. It always sends HTTP JSON requests to the FastAPI API. This is the core distributed programming concept in this project: separate processes communicating over a network protocol with defined contracts.

Now I will explain the backend design briefly.

I separated the backend into routers, schemas, CRUD, and services.

- Routers define the endpoints like `/students`, `/tasks`, `/exams`, `/schedules`, `/notifications`, and `/analytics`.
- Schemas define request and response structures and validation rules.
- CRUD handles database operations.
- Services contain business logic, especially three important modules:
  - `priority_service.py`
  - `schedule_service.py`
  - `notification_service.py`

The priority service computes a score from 0 to 10 for each task. The formula combines urgency, difficulty, whether the task is exam-related, and estimated hours. This means high-difficulty tasks with close deadlines get a higher score.

The schedule generation service is the most important feature. When we call `POST /schedules/generate/{student_id}`, the backend:

- validates the student,
- removes old generated sessions,
- recalculates task priorities,
- sorts tasks by priority and deadline,
- splits study work into sessions of maximum 2 hours,
- enforces daily capacity based on student study hours,
- adds exam revision sessions before exam dates,
- returns warnings if all hours cannot fit before deadlines.

This shows clear backend orchestration and non-trivial logic that a frontend should not perform.

The notification service generates reminder objects such as overdue tasks, deadlines due soon, exam reminders, high-priority warnings, and today’s study sessions. This endpoint returns structured notifications with type and severity so the frontend can render them cleanly.

On the frontend side, I built pages for:

- Dashboard
- Students
- Tasks
- Exams
- Schedule
- Notifications
- Analytics

The frontend uses a centralized API layer in `lib/api.ts`, so all HTTP calls are consistent and maintainable. It stores the selected student in localStorage and uses loading, error, and empty states for usability.

For testing, I implemented both automated and manual validation.

Automated tests use pytest with FastAPI TestClient and an isolated test SQLite database. They cover health checks, student/task/exam flows, schedule generation and completion, notifications, and analytics.

Manual testing is done with `tests/manual_client.py`, which runs real HTTP requests against the running server and prints responses for a demo scenario: creating a student, adding four tasks, adding two exams, generating schedule, and then fetching notifications and analytics.

In conclusion, this project satisfies the distributed programming objective because the architecture is explicitly separated and API-driven. The backend is responsible for all logic and persistence, while the frontend is a pure client application. The system is functional, testable, and extensible for future features like authentication, calendar integration, and migration from SQLite to PostgreSQL.

Thank you.
