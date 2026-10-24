import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.main import app
from app.models.base import Base
from app.models.admission import Admission
from app.models.student import Student
from app.config import settings

# Temporary database used only for these tests.
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


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


def test_list_admissions(client):
    client.post("/api/v1/admissions", json=valid_application())

    response = client.get("/api/v1/admissions")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["full_name"] == "Test Applicant"


def test_get_admission_details(client):
    created = client.post(
        "/api/v1/admissions",
        json=valid_application(),
    )
    admission_id = created.json()["id"]

    response = client.get(f"/api/v1/admissions/{admission_id}")

    assert response.status_code == 200
    assert response.json()["id"] == admission_id


def test_missing_admission_returns_404(client):
    response = client.get("/api/v1/admissions/99999")

    assert response.status_code == 404


def test_invalid_email_is_rejected(client):
    payload = valid_application()
    payload["email"] = "not-an-email"

    response = client.post("/api/v1/admissions", json=payload)

    assert response.status_code == 422


def test_list_admissions_supports_pagination(client):
    client.post("/api/v1/admissions", json=valid_application())

    response = client.get("/api/v1/admissions?offset=0&limit=1")

    assert response.status_code == 200
    assert len(response.json()) == 1
    
def test_approve_admission(client):
    created = client.post("/api/v1/admissions", json=valid_application())
    admission_id = created.json()["id"]

    response = client.post(
        f"/api/v1/admissions/{admission_id}/approve",
        json={"remarks": "Documents reviewed."},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "approved"
    assert response.json()["review_remarks"] == "Documents reviewed."


def test_reject_admission(client):
    created = client.post("/api/v1/admissions", json=valid_application())
    admission_id = created.json()["id"]

    response = client.post(
        f"/api/v1/admissions/{admission_id}/reject",
        json={"remarks": "Eligibility criteria not met."},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "rejected"


def test_cannot_review_admission_twice(client):
    created = client.post("/api/v1/admissions", json=valid_application())
    admission_id = created.json()["id"]

    first_response = client.post(
        f"/api/v1/admissions/{admission_id}/approve",
        json={"remarks": "Approved."},
    )
    second_response = client.post(
        f"/api/v1/admissions/{admission_id}/reject",
        json={"remarks": "Rejected."},
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 409


def test_review_missing_admission_returns_404(client):
    response = client.post(
        "/api/v1/admissions/99999/approve",
        json={"remarks": "Test."},
    )

    assert response.status_code == 404


def test_review_endpoints_disabled_returns_404(client, monkeypatch):
    monkeypatch.setattr(settings, "enable_dev_review_endpoints", False)

    created = client.post("/api/v1/admissions", json=valid_application())
    admission_id = created.json()["id"]

    response = client.post(
        f"/api/v1/admissions/{admission_id}/approve",
        json={"remarks": "Test."},
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


def test_list_students(client):
    create_test_student(client)

    response = client.get("/api/v1/students")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["full_name"] == "Test Applicant"


def test_get_student_details(client):
    student_id = create_test_student(client)

    response = client.get(f"/api/v1/students/{student_id}")

    assert response.status_code == 200
    assert response.json()["id"] == student_id
    assert response.json()["student_number"] == "STU-TEST-001"


def test_missing_student_returns_404(client):
    response = client.get("/api/v1/students/99999")

    assert response.status_code == 404


def test_update_student_contact_details(client):
    student_id = create_test_student(client)

    response = client.patch(
        f"/api/v1/students/{student_id}",
        json={
            "email": "updated@example.com",
            "phone_number": "9123456789",
        },
    )

    assert response.status_code == 200
    assert response.json()["email"] == "updated@example.com"
    assert response.json()["phone_number"] == "9123456789"


def test_empty_student_update_returns_422(client):
    student_id = create_test_student(client)

    response = client.patch(
        f"/api/v1/students/{student_id}",
        json={},
    )

    assert response.status_code == 422