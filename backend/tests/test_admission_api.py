import pytest

from app.config import settings
from app.models.student import Student
from conftest import TestingSessionLocal


def valid_application():
    """Return a fresh, valid admission payload for each test."""
    return {
        "full_name": "Test Applicant",
        "email": "applicant@example.com",
        "phone_number": "9876543210",
        "course_applied": "B.Tech",
        "branch_applied": "Computer Science",
    }


def create_admission(client):
    response = client.post(
        "/api/v1/admissions",
        json=valid_application(),
    )
    assert response.status_code == 201, response.text
    return response.json()["id"]


def approve_test_admission(client, headers, monkeypatch):
    """Create and approve an admission using an existing staff token."""
    monkeypatch.setattr(settings, "enable_dev_review_endpoints", True)
    admission_id = create_admission(client)

    response = client.post(
        f"/api/v1/admissions/{admission_id}/approve",
        json={"remarks": "Approved for registration."},
        headers=headers,
    )
    assert response.status_code == 200, response.text
    return admission_id


# ---------------------------------------------------------------------------
# Admission API tests
# ---------------------------------------------------------------------------

def test_submit_admission(client):
    response = client.post(
        "/api/v1/admissions",
        json=valid_application(),
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["full_name"] == "Test Applicant"
    assert data["status"] == "submitted"
    assert data["application_number"].startswith("APP-")
    assert data["id"] is not None


def test_list_admissions(client, auth_headers):
    client.post("/api/v1/admissions", json=valid_application())

    response = client.get(
        "/api/v1/admissions",
        headers=auth_headers(),
    )

    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["full_name"] == "Test Applicant"


def test_get_admission_details(client, auth_headers):
    admission_id = create_admission(client)

    response = client.get(
        f"/api/v1/admissions/{admission_id}",
        headers=auth_headers(),
    )

    assert response.status_code == 200, response.text
    assert response.json()["id"] == admission_id


def test_missing_admission_returns_404(client, auth_headers):
    response = client.get(
        "/api/v1/admissions/99999",
        headers=auth_headers(),
    )

    assert response.status_code == 404


def test_invalid_email_is_rejected(client):
    payload = valid_application()
    payload["email"] = "not-an-email"

    response = client.post("/api/v1/admissions", json=payload)

    assert response.status_code == 422


def test_list_admissions_supports_pagination(client, auth_headers):
    client.post("/api/v1/admissions", json=valid_application())

    response = client.get(
        "/api/v1/admissions?offset=0&limit=1",
        headers=auth_headers(),
    )

    assert response.status_code == 200, response.text
    assert len(response.json()) == 1


def test_approve_admission(client, auth_headers, monkeypatch):
    monkeypatch.setattr(settings, "enable_dev_review_endpoints", True)
    admission_id = create_admission(client)

    response = client.post(
        f"/api/v1/admissions/{admission_id}/approve",
        json={"remarks": "Documents reviewed."},
        headers=auth_headers(),
    )

    assert response.status_code == 200, response.text
    assert response.json()["status"] == "approved"
    assert response.json()["review_remarks"] == "Documents reviewed."


def test_reject_admission(client, auth_headers, monkeypatch):
    monkeypatch.setattr(settings, "enable_dev_review_endpoints", True)
    admission_id = create_admission(client)

    response = client.post(
        f"/api/v1/admissions/{admission_id}/reject",
        json={"remarks": "Eligibility criteria not met."},
        headers=auth_headers(),
    )

    assert response.status_code == 200, response.text
    assert response.json()["status"] == "rejected"


def test_cannot_review_admission_twice(client, auth_headers, monkeypatch):
    monkeypatch.setattr(settings, "enable_dev_review_endpoints", True)
    headers = auth_headers()
    admission_id = create_admission(client)

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

    assert first_response.status_code == 200, first_response.text
    assert second_response.status_code == 409, second_response.text


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
    admission_id = create_admission(client)

    response = client.post(
        f"/api/v1/admissions/{admission_id}/approve",
        json={"remarks": "Test."},
        headers=auth_headers(),
    )

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Student API tests
# ---------------------------------------------------------------------------

def create_test_student(client):
    """Create a student record directly for student endpoint tests."""
    admission_id = create_admission(client)

    with TestingSessionLocal() as db:
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
        student_id = student.id

    return student_id


def test_list_students(client, auth_headers):
    create_test_student(client)

    response = client.get(
        "/api/v1/students",
        headers=auth_headers(),
    )

    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["full_name"] == "Test Applicant"


def test_get_student_details(client, auth_headers):
    student_id = create_test_student(client)

    response = client.get(
        f"/api/v1/students/{student_id}",
        headers=auth_headers(),
    )

    assert response.status_code == 200, response.text
    assert response.json()["id"] == student_id
    assert response.json()["student_number"] == "STU-TEST-001"


def test_missing_student_returns_404(client, auth_headers):
    response = client.get(
        "/api/v1/students/99999",
        headers=auth_headers(),
    )

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

    assert response.status_code == 200, response.text
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


# ---------------------------------------------------------------------------
# Admission-to-student registration tests
# ---------------------------------------------------------------------------

def test_register_student_from_approved_admission(client, auth_headers, monkeypatch):
    headers = auth_headers()
    admission_id = approve_test_admission(client, headers, monkeypatch)

    response = client.post(
        f"/api/v1/students/register-from-admission/{admission_id}",
        json={"current_year": 2},
        headers=headers,
    )

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["admission_id"] == admission_id
    assert data["full_name"] == "Test Applicant"
    assert data["email"] == "applicant@example.com"
    assert data["phone_number"] == "9876543210"
    assert data["course"] == "B.Tech"
    assert data["branch"] == "Computer Science"
    assert data["current_year"] == 2
    assert data["student_number"].startswith("STU-")


def test_registration_rejects_pending_admission(client, auth_headers):
    admission_id = create_admission(client)

    response = client.post(
        f"/api/v1/students/register-from-admission/{admission_id}",
        json={"current_year": 1},
        headers=auth_headers(),
    )

    assert response.status_code == 409


def test_registration_rejects_rejected_admission(client, auth_headers, monkeypatch):
    headers = auth_headers()
    monkeypatch.setattr(settings, "enable_dev_review_endpoints", True)
    admission_id = create_admission(client)

    rejected = client.post(
        f"/api/v1/admissions/{admission_id}/reject",
        json={"remarks": "Not eligible."},
        headers=headers,
    )
    assert rejected.status_code == 200, rejected.text

    response = client.post(
        f"/api/v1/students/register-from-admission/{admission_id}",
        json={"current_year": 1},
        headers=headers,
    )

    assert response.status_code == 409


def test_registration_missing_admission_returns_404(client, auth_headers):
    response = client.post(
        "/api/v1/students/register-from-admission/99999",
        json={"current_year": 1},
        headers=auth_headers(),
    )

    assert response.status_code == 404


def test_repeated_registration_does_not_create_duplicate(client, auth_headers, monkeypatch):
    headers = auth_headers()
    admission_id = approve_test_admission(client, headers, monkeypatch)
    url = f"/api/v1/students/register-from-admission/{admission_id}"
    payload = {"current_year": 1}

    first = client.post(url, json=payload, headers=headers)
    second = client.post(url, json=payload, headers=headers)

    assert first.status_code == 201, first.text
    assert second.status_code == 200, second.text
    assert second.json()["id"] == first.json()["id"]

    with TestingSessionLocal() as db:
        matching_students = (
            db.query(Student)
            .filter(Student.admission_id == admission_id)
            .count()
        )

    assert matching_students == 1


def test_registration_rejects_invalid_current_year(client, auth_headers):
    admission_id = create_admission(client)

    response = client.post(
        f"/api/v1/students/register-from-admission/{admission_id}",
        json={"current_year": 0},
        headers=auth_headers(),
    )

    assert response.status_code == 422


def test_registration_requires_authentication(client, auth_headers, monkeypatch):
    headers = auth_headers()
    admission_id = approve_test_admission(client, headers, monkeypatch)

    response = client.post(
        f"/api/v1/students/register-from-admission/{admission_id}",
        json={"current_year": 1},
    )

    assert response.status_code == 401


def test_student_role_cannot_register_student(client, auth_headers, monkeypatch):
    staff_headers = auth_headers()
    admission_id = approve_test_admission(client, staff_headers, monkeypatch)

    # Give the student-role user a distinct email so the fixture does not
    # attempt to create a duplicate staff@example.com user.
    student_headers = auth_headers(
        role="student",
        email="student-role@example.com",
    )

    response = client.post(
        f"/api/v1/students/register-from-admission/{admission_id}",
        json={"current_year": 1},
        headers=student_headers,
    )

    assert response.status_code == 403
