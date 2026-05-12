from datetime import date, timedelta


def _create_student(client):
    response = client.post(
        "/students",
        json={
            "name": "Notify User",
            "email": "notify@example.com",
            "study_hours_per_day": 4,
            "preferred_start_time": "09:00",
            "preferred_end_time": "18:00",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_notifications_and_analytics(client):
    student = _create_student(client)

    client.post(
        "/tasks",
        json={
            "student_id": student["id"],
            "title": "Urgent Task",
            "description": "Finish urgent task",
            "course_name": "DP",
            "deadline": (date.today() + timedelta(days=1)).isoformat(),
            "difficulty": 5,
            "estimated_hours": 8,
            "is_exam_related": True,
            "status": "pending",
        },
    )

    client.post(
        "/exams",
        json={
            "student_id": student["id"],
            "subject": "Distributed Programming",
            "course_name": "DP",
            "exam_date": (date.today() + timedelta(days=2)).isoformat(),
            "importance": 5,
            "estimated_revision_hours": 3,
        },
    )

    client.post(f"/schedules/generate/{student['id']}")

    notifications_response = client.get(f"/notifications/student/{student['id']}")
    assert notifications_response.status_code == 200
    notifications = notifications_response.json()
    assert len(notifications) > 0
    notification_types = {item["type"] for item in notifications}
    assert "task_deadline" in notification_types or "high_priority_task" in notification_types

    analytics_response = client.get(f"/analytics/dashboard/{student['id']}")
    assert analytics_response.status_code == 200
    stats = analytics_response.json()
    assert stats["total_tasks"] == 1
    assert stats["pending_tasks"] == 1
    assert stats["upcoming_exams"] == 1
    assert stats["generated_sessions"] >= 1
