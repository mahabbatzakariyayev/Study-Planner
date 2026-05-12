def test_create_get_update_delete_student(client):
    create_payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "study_hours_per_day": 4,
        "preferred_start_time": "09:00",
        "preferred_end_time": "18:00",
    }
    create_response = client.post("/students", json=create_payload)
    assert create_response.status_code == 201
    student = create_response.json()
    assert student["name"] == "Alice"

    list_response = client.get("/students")
    assert list_response.status_code == 200
    students = list_response.json()
    assert len(students) == 1

    student_id = student["id"]
    get_response = client.get(f"/students/{student_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == "alice@example.com"

    update_response = client.put(
        f"/students/{student_id}",
        json={"study_hours_per_day": 6, "name": "Alice Updated"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["study_hours_per_day"] == 6

    delete_response = client.delete(f"/students/{student_id}")
    assert delete_response.status_code == 200
    assert "deleted successfully" in delete_response.json()["message"]

    not_found_response = client.get(f"/students/{student_id}")
    assert not_found_response.status_code == 404
