import pytest
from app.config import settings
from app.models.student import Student
from conftest import TestingSessionLocal

def valid_application():
    return {
        "full_name": "Test Applicant",
        "email": "applicant@example.com",
        "phone_number": "9876543210",
        "course_applied": "B.Tech",
        "branch_applied": "Computer Science",
    }


def test_submit_admission(client):
    response = client.post(
        "/api/v1/admissions",
        json=valid_application(),
    )

    assert response.status_code == 201

    data = response.json()
    assert data["full_name"] == "Test Applicant"
    assert data["status"] == "submitted"
    assert data["application_number"].startswith("APP-")
    assert data["id"] is not None


def test_list_admissions(client, auth_headers):
    client.post("/api/v1/admissions", json=valid_application())

    response = client.get("/api/v1/admissions", headers=auth_headers())

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["full_name"] == "Test Applicant"


def test_get_admission_details(client, auth_headers):
    created = client.post(
        "/api/v1/admissions",
        json=valid_application(),
    )
    admission_id = created.json()["id"]

    response = client.get(f"/api/v1/admissions/{admission_id}", headers=auth_headers())

    assert response.status_code == 200
    assert response.json()["id"] == admission_id


def test_missing_admission_returns_404(client, auth_headers):
    response = client.get("/api/v1/admissions/99999", headers=auth_headers())

    assert response.status_code == 404


def test_invalid_email_is_rejected(client):
    payload = valid_application()
    payload["email"] = "not-an-email"

    response = client.post("/api/v1/admissions", json=payload)

    assert response.status_code == 422


def test_list_admissions_supports_pagination(client, auth_headers):
    client.post("/api/v1/admissions", json=valid_application())

    response = client.get("/api/v1/admissions?offset=0&limit=1", headers=auth_headers())

    assert response.status_code == 200
    assert len(response.json()) == 1
    
def test_approve_admission(client, auth_headers, monkeypatch):
    monkeypatch.setattr(settings, "enable_dev_review_endpoints", True)
    created = client.post("/api/v1/admissions", json=valid_application())
    admission_id = created.json()["id"]

    response = client.post(
        f"/api/v1/admissions/{admission_id}/approve",
        json={"remarks": "Documents reviewed."},
        headers=auth_headers(),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "approved"
    assert response.json()["review_remarks"] == "Documents reviewed."


def test_reject_admission(client, auth_headers, monkeypatch):
    monkeypatch.setattr(settings, "enable_dev_review_endpoints", True)
    created = client.post("/api/v1/admissions", json=valid_application())
    admission_id = created.json()["id"]

    response = client.post(
        f"/api/v1/admissions/{admission_id}/reject",
        json={"remarks": "Eligibility criteria not met."},
        headers=auth_headers(),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "rejected"


def test_cannot_review_admission_twice(client, auth_headers, monkeypatch):
    monkeypatch.setattr(settings, "enable_dev_review_endpoints", True)
    created = client.post("/api/v1/admissions", json=valid_application())
    admission_id = created.json()["id"]

    headers = auth_headers()

    first_response = client.post(
        f"/api/v1/admissions/{admission_id}/approve",
        json={"remarks": "Approved."},
        headers=headers,
    )
    second_response = client.post(
        f"/api/v1/admissions/{admission_id}/reject",
        json={"remarks": "Rejected."},
        headers=headers,
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 409


def test_review_missing_admission_returns_404(client, auth_headers, monkeypatch):
    monkeypatch.setattr(settings, "enable_dev_review_endpoints", True)
    response = client.post(
        "/api/v1/admissions/99999/approve",
        json={"remarks": "Test."},
        headers=auth_headers(),
    )

    assert response.status_code == 404


def test_review_endpoints_disabled_returns_404(client, monkeypatch, auth_headers):
    monkeypatch.setattr(settings, "enable_dev_review_endpoints", False)

    created = client.post("/api/v1/admissions", json=valid_application())
    admission_id = created.json()["id"]

    response = client.post(
        f"/api/v1/admissions/{admission_id}/approve",
        json={"remarks": "Test."},
        headers=auth_headers(),
    )

    assert response.status_code == 404


def create_test_student(client):
    created = client.post("/api/v1/admissions", json=valid_application())
    assert created.status_code == 201

    admission_id = created.json()["id"]

    # Create a linked test student directly in the temporary test database.
    db = TestingSessionLocal()
    try:
        student = Student(
            student_number="STU-TEST-001",
            admission_id=admission_id,
            full_name="Test Applicant",
            email="applicant@example.com",
            phone_number="9876543210",
            course="B.Tech",
            branch="Computer Science",
            current_year=1,
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        return student.id
    finally:
        db.close()


def test_list_students(client, auth_headers):
    create_test_student(client)

    response = client.get("/api/v1/students", headers=auth_headers())

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["full_name"] == "Test Applicant"


def test_get_student_details(client, auth_headers):
    student_id = create_test_student(client)

    response = client.get(f"/api/v1/students/{student_id}", headers=auth_headers())

    assert response.status_code == 200
    assert response.json()["id"] == student_id
    assert response.json()["student_number"] == "STU-TEST-001"


def test_missing_student_returns_404(client, auth_headers):
    response = client.get("/api/v1/students/99999", headers=auth_headers())

    assert response.status_code == 404


def test_update_student_contact_details(client, auth_headers):
    student_id = create_test_student(client)

    response = client.patch(
        f"/api/v1/students/{student_id}",
        json={
            "email": "updated@example.com",
            "phone_number": "9123456789",
        },
        headers=auth_headers(),
    )

    assert response.status_code == 200
    assert response.json()["email"] == "updated@example.com"
    assert response.json()["phone_number"] == "9123456789"


def test_empty_student_update_returns_422(client, auth_headers):
    student_id = create_test_student(client)

    response = client.patch(
        f"/api/v1/students/{student_id}",
        json={},
        headers=auth_headers(),
    )

    assert response.status_code == 422