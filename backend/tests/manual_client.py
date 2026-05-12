from __future__ import annotations

from datetime import date, timedelta
from pprint import pprint

import requests

BASE_URL = "http://127.0.0.1:8000"


def print_step(title: str, response: requests.Response) -> None:
    print(f"\n=== {title} ===")
    print(f"Status: {response.status_code}")
    try:
        pprint(response.json())
    except ValueError:
        print(response.text)


def main() -> None:
    health = requests.get(f"{BASE_URL}/health", timeout=10)
    print_step("1) Health", health)

    student_payload = {
        "name": "Demo Student",
        "email": "demo@student.com",
        "study_hours_per_day": 4,
        "preferred_start_time": "09:00",
        "preferred_end_time": "18:00",
    }

    student_resp = requests.post(f"{BASE_URL}/students", json=student_payload, timeout=10)
    if student_resp.status_code == 400:
        students_resp = requests.get(f"{BASE_URL}/students", timeout=10)
        students = students_resp.json()
        student = next((s for s in students if s["email"] == "demo@student.com"), students[0])
        print_step("2) Create demo student (already exists, using existing)", students_resp)
    else:
        print_step("2) Create demo student", student_resp)
        student = student_resp.json()

    student_id = student["id"]

    # Keep manual demo runs reproducible by clearing previous demo data first.
    existing_tasks_resp = requests.get(f"{BASE_URL}/tasks/student/{student_id}", timeout=10)
    if existing_tasks_resp.status_code == 200:
        for task in existing_tasks_resp.json():
            requests.delete(f"{BASE_URL}/tasks/{task['id']}", timeout=10)

    existing_exams_resp = requests.get(f"{BASE_URL}/exams/student/{student_id}", timeout=10)
    if existing_exams_resp.status_code == 200:
        for exam in existing_exams_resp.json():
            requests.delete(f"{BASE_URL}/exams/{exam['id']}", timeout=10)

    requests.delete(f"{BASE_URL}/schedules/student/{student_id}", timeout=10)

    tasks = [
        {
            "title": "Prepare Distributed Programming REST API",
            "description": "Define endpoints and payload schemas",
            "course_name": "Distributed Programming",
            "deadline": (date.today() + timedelta(days=2)).isoformat(),
            "difficulty": 5,
            "estimated_hours": 8,
            "is_exam_related": True,
        },
        {
            "title": "Study FastAPI endpoints",
            "description": "Review routers, validation and error responses",
            "course_name": "Distributed Programming",
            "deadline": (date.today() + timedelta(days=4)).isoformat(),
            "difficulty": 4,
            "estimated_hours": 5,
            "is_exam_related": True,
        },
        {
            "title": "Write project report",
            "description": "Draft project explanation and architecture",
            "course_name": "Distributed Programming",
            "deadline": (date.today() + timedelta(days=6)).isoformat(),
            "difficulty": 3,
            "estimated_hours": 4,
            "is_exam_related": False,
        },
        {
            "title": "Prepare final presentation",
            "description": "Create slides and rehearse",
            "course_name": "Distributed Programming",
            "deadline": (date.today() + timedelta(days=7)).isoformat(),
            "difficulty": 3,
            "estimated_hours": 3,
            "is_exam_related": False,
        },
    ]

    for index, task in enumerate(tasks, start=1):
        payload = {"student_id": student_id, "status": "pending", **task}
        response = requests.post(f"{BASE_URL}/tasks", json=payload, timeout=10)
        print_step(f"3.{index}) Create task", response)

    exams = [
        {
            "subject": "Distributed Programming",
            "course_name": "CS401",
            "exam_date": (date.today() + timedelta(days=8)).isoformat(),
            "importance": 5,
            "estimated_revision_hours": 5,
        },
        {
            "subject": "Machine Learning",
            "course_name": "ML501",
            "exam_date": (date.today() + timedelta(days=12)).isoformat(),
            "importance": 4,
            "estimated_revision_hours": 6,
        },
    ]

    for index, exam in enumerate(exams, start=1):
        payload = {"student_id": student_id, **exam}
        response = requests.post(f"{BASE_URL}/exams", json=payload, timeout=10)
        print_step(f"4.{index}) Create exam", response)

    tasks_resp = requests.get(f"{BASE_URL}/tasks/student/{student_id}", timeout=10)
    print_step("5) Get tasks", tasks_resp)

    generate_resp = requests.post(f"{BASE_URL}/schedules/generate/{student_id}", timeout=10)
    print_step("6) Generate schedule", generate_resp)

    schedule_resp = requests.get(f"{BASE_URL}/schedules/student/{student_id}", timeout=10)
    print_step("7) Get schedule", schedule_resp)

    notif_resp = requests.get(f"{BASE_URL}/notifications/student/{student_id}", timeout=10)
    print_step("8) Get notifications", notif_resp)

    analytics_resp = requests.get(f"{BASE_URL}/analytics/dashboard/{student_id}", timeout=10)
    print_step("9) Get analytics", analytics_resp)


if __name__ == "__main__":
    main()
