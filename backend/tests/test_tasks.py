from datetime import date, timedelta


def _create_student(client):
    response = client.post(
        "/students",
        json={
            "name": "Task User",
            "email": "taskuser@example.com",
            "study_hours_per_day": 4,
            "preferred_start_time": "09:00",
            "preferred_end_time": "18:00",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_create_get_update_status_delete_task(client):
    student = _create_student(client)
    deadline = (date.today() + timedelta(days=1)).isoformat()

    create_response = client.post(
        "/tasks",
        json={
            "student_id": student["id"],
            "title": "Prepare REST API",
            "description": "Design and implement endpoints",
            "course_name": "Distributed Programming",
            "deadline": deadline,
            "difficulty": 5,
            "estimated_hours": 10,
            "is_exam_related": True,
            "status": "pending",
        },
    )
    assert create_response.status_code == 201
    task = create_response.json()
    assert task["priority_score"] == 9.6

    by_student_response = client.get(f"/tasks/student/{student['id']}")
    assert by_student_response.status_code == 200
    tasks = by_student_response.json()
    assert len(tasks) == 1

    task_id = task["id"]
    update_response = client.put(
        f"/tasks/{task_id}",
        json={"estimated_hours": 6, "difficulty": 4, "status": "in_progress"},
    )
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["status"] == "in_progress"
    assert updated_task["priority_score"] > 0

    patch_response = client.patch(f"/tasks/{task_id}/status", json={"status": "completed"})
    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == "completed"

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200

    get_deleted_response = client.get(f"/tasks/{task_id}")
    assert get_deleted_response.status_code == 404
