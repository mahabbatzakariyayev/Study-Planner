from datetime import date, timedelta


def _create_student(client):
    response = client.post(
        "/students",
        json={
            "name": "Schedule User",
            "email": "scheduleuser@example.com",
            "study_hours_per_day": 4,
            "preferred_start_time": "09:00",
            "preferred_end_time": "18:00",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_generate_get_complete_and_delete_schedule(client):
    student = _create_student(client)

    client.post(
        "/tasks",
        json={
            "student_id": student["id"],
            "title": "Prepare report",
            "description": "Write final report",
            "course_name": "Distributed Programming",
            "deadline": (date.today() + timedelta(days=2)).isoformat(),
            "difficulty": 4,
            "estimated_hours": 5,
            "is_exam_related": False,
            "status": "pending",
        },
    )
    client.post(
        "/tasks",
        json={
            "student_id": student["id"],
            "title": "Study FastAPI",
            "description": "Review routers and services",
            "course_name": "Distributed Programming",
            "deadline": (date.today() + timedelta(days=3)).isoformat(),
            "difficulty": 5,
            "estimated_hours": 4,
            "is_exam_related": True,
            "status": "pending",
        },
    )
    client.post(
        "/exams",
        json={
            "student_id": student["id"],
            "subject": "Machine Learning",
            "course_name": "ML501",
            "exam_date": (date.today() + timedelta(days=4)).isoformat(),
            "importance": 5,
            "estimated_revision_hours": 3,
        },
    )

    generate_response = client.post(f"/schedules/generate/{student['id']}")
    assert generate_response.status_code == 200
    generated = generate_response.json()
    assert generated["student_id"] == student["id"]
    assert generated["total_sessions"] > 0
    assert generated["total_hours"] > 0

    get_response = client.get(f"/schedules/student/{student['id']}")
    assert get_response.status_code == 200
    sessions = get_response.json()
    assert len(sessions) == generated["total_sessions"]

    first_session_id = sessions[0]["id"]
    complete_response = client.patch(f"/schedules/{first_session_id}/complete")
    assert complete_response.status_code == 200
    assert complete_response.json()["completed"] is True

    delete_response = client.delete(f"/schedules/student/{student['id']}")
    assert delete_response.status_code == 200

    empty_response = client.get(f"/schedules/student/{student['id']}")
    assert empty_response.status_code == 200
    assert empty_response.json() == []
