# API Endpoints

Base URL: `http://127.0.0.1:8000`

## Endpoint Table

| Method | Endpoint | Description | Request Body Example | Response Example |
|---|---|---|---|---|
| GET | `/health` | Health check | - | `{ "status": "ok", "message": "AI Study Planner API is running" }` |
| POST | `/students` | Create student | `{ "name": "Demo", "email": "demo@student.com", "study_hours_per_day": 4 }` | Student object |
| GET | `/students` | Get all students | - | `[Student]` |
| GET | `/students/{student_id}` | Get one student | - | Student object |
| PUT | `/students/{student_id}` | Update student | `{ "study_hours_per_day": 5 }` | Updated student |
| DELETE | `/students/{student_id}` | Delete student | - | `{ "message": "Student 1 deleted successfully" }` |
| POST | `/tasks` | Create task + auto priority | `{ "student_id": 1, "title": "Task", "deadline": "2026-05-20", "difficulty": 4, "estimated_hours": 5, "is_exam_related": true, "status": "pending" }` | Task object with `priority_score` |
| GET | `/tasks` | Get all tasks | - | `[Task]` |
| GET | `/tasks/student/{student_id}` | Get tasks by student | - | `[Task]` |
| GET | `/tasks/{task_id}` | Get one task | - | Task object |
| PUT | `/tasks/{task_id}` | Update task + recalc priority | `{ "difficulty": 5, "estimated_hours": 8 }` | Updated task |
| PATCH | `/tasks/{task_id}/status` | Update only status | `{ "status": "completed" }` | Updated task |
| DELETE | `/tasks/{task_id}` | Delete task | - | `{ "message": "Task 1 deleted successfully" }` |
| POST | `/exams` | Create exam | `{ "student_id": 1, "subject": "Distributed Programming", "exam_date": "2026-05-25", "importance": 5, "estimated_revision_hours": 6 }` | Exam object |
| GET | `/exams` | Get all exams | - | `[Exam]` |
| GET | `/exams/student/{student_id}` | Get exams by student | - | `[Exam]` |
| GET | `/exams/{exam_id}` | Get one exam | - | Exam object |
| PUT | `/exams/{exam_id}` | Update exam | `{ "importance": 4 }` | Updated exam |
| DELETE | `/exams/{exam_id}` | Delete exam | - | `{ "message": "Exam 1 deleted successfully" }` |
| POST | `/schedules/generate/{student_id}` | Generate schedule | - | `{ "student_id":1,"total_sessions":5,"total_hours":9.5,"warnings":[],"sessions":[...] }` |
| GET | `/schedules/student/{student_id}` | Get generated schedule | - | `[StudySession]` |
| PATCH | `/schedules/{session_id}/complete` | Mark session completed | - | Updated study session |
| DELETE | `/schedules/student/{student_id}` | Delete schedule | - | `{ "message": "Deleted X session(s) for student Y" }` |
| GET | `/notifications/student/{student_id}` | Get notifications | - | `[Notification]` |
| GET | `/analytics/dashboard/{student_id}` | Get dashboard stats | - | `{ "total_tasks": 4, "completion_rate": 25.0, ... }` |

## Error Response Pattern
Example 404:
```json
{
  "detail": "Student with id 5 was not found"
}
```

Example 422 validation:
```json
{
  "detail": [
    {
      "loc": ["body", "difficulty"],
      "msg": "Input should be less than or equal to 5"
    }
  ]
}
```
