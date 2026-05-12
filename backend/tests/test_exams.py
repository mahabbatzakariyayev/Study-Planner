from datetime import date, timedelta


def _create_student(client):
    response = client.post(
        "/students",
        json={
            "name": "Exam User",
            "email": "examuser@example.com",
            "study_hours_per_day": 5,
            "preferred_start_time": "09:00",
            "preferred_end_time": "18:00",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_create_get_update_delete_exam(client):
    student = _create_student(client)
    exam_date = (date.today() + timedelta(days=5)).isoformat()

    create_response = client.post(
        "/exams",
        json={
            "student_id": student["id"],
            "subject": "Distributed Programming",
            "course_name": "CS401",
            "exam_date": exam_date,
            "importance": 5,
            "estimated_revision_hours": 6,
        },
    )
    assert create_response.status_code == 201
    exam = create_response.json()
    exam_id = exam["id"]

    list_response = client.get(f"/exams/student/{student['id']}")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.put(
        f"/exams/{exam_id}",
        json={"importance": 4, "estimated_revision_hours": 5},
    )
    assert update_response.status_code == 200
    assert update_response.json()["importance"] == 4

    delete_response = client.delete(f"/exams/{exam_id}")
    assert delete_response.status_code == 200

    get_deleted = client.get(f"/exams/{exam_id}")
    assert get_deleted.status_code == 404
