# Test Queries (curl)

Base URL:
```bash
BASE=http://127.0.0.1:8000
```

## Health
```bash
curl -X GET "$BASE/health"
```

## Students
```bash
curl -X POST "$BASE/students" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Demo Student",
    "email":"demo@student.com",
    "study_hours_per_day":4,
    "preferred_start_time":"09:00",
    "preferred_end_time":"18:00"
  }'

curl -X GET "$BASE/students"
curl -X GET "$BASE/students/1"

curl -X PUT "$BASE/students/1" \
  -H "Content-Type: application/json" \
  -d '{"study_hours_per_day":5}'

curl -X DELETE "$BASE/students/1"
```

## Tasks
```bash
curl -X POST "$BASE/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id":1,
    "title":"Prepare Distributed Programming REST API",
    "description":"Build endpoints",
    "course_name":"Distributed Programming",
    "deadline":"2026-05-20",
    "difficulty":5,
    "estimated_hours":8,
    "is_exam_related":true,
    "status":"pending"
  }'

curl -X GET "$BASE/tasks"
curl -X GET "$BASE/tasks/student/1"
curl -X GET "$BASE/tasks/1"

curl -X PUT "$BASE/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{"estimated_hours":6,"difficulty":4}'

curl -X PATCH "$BASE/tasks/1/status" \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'

curl -X DELETE "$BASE/tasks/1"
```

## Exams
```bash
curl -X POST "$BASE/exams" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id":1,
    "subject":"Distributed Programming",
    "course_name":"CS401",
    "exam_date":"2026-05-25",
    "importance":5,
    "estimated_revision_hours":6
  }'

curl -X GET "$BASE/exams"
curl -X GET "$BASE/exams/student/1"
curl -X GET "$BASE/exams/1"

curl -X PUT "$BASE/exams/1" \
  -H "Content-Type: application/json" \
  -d '{"importance":4}'

curl -X DELETE "$BASE/exams/1"
```

## Schedule
```bash
curl -X POST "$BASE/schedules/generate/1"
curl -X GET "$BASE/schedules/student/1"
curl -X PATCH "$BASE/schedules/1/complete"
curl -X DELETE "$BASE/schedules/student/1"
```

## Notifications
```bash
curl -X GET "$BASE/notifications/student/1"
```

## Analytics
```bash
curl -X GET "$BASE/analytics/dashboard/1"
```

## Manual Client Script
```bash
cd backend
.venv\Scripts\python tests/manual_client.py
```
