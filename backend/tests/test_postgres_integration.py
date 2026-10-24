import os
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.config import settings
from app.database import SessionLocal, engine, get_db
from app.main import app
from app.models.admission import Admission
from app.models.student import Student


pytestmark = pytest.mark.skipif(
    os.getenv("COLLEGE_ERP_RUN_PG_TESTS") != "1",
    reason="Set COLLEGE_ERP_RUN_PG_TESTS=1 to run PostgreSQL integration tests.",
)


@pytest.fixture
def pg_client():
    # Refuse to run destructive test cleanup against any other database.
    if engine.url.database != "college_erp_test":
        pytest.fail(
            "PostgreSQL integration tests require the college_erp_test database. "
            f"Current database: {engine.url.database!r}"
        )

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.pop(get_db, None)

        # Delete only records created by these integration tests.
        with SessionLocal() as db:
            test_email_pattern = "pg-integration-%@example.com"

            db.execute(
                delete(Student).where(
                    Student.email.like(test_email_pattern)
                )
            )
            db.execute(
                delete(Admission).where(
                    Admission.email.like(test_email_pattern)
                )
            )
            db.commit()


def valid_application():
    unique_id = uuid4().hex

    return {
        "full_name": "PostgreSQL Integration Applicant",
        "email": f"pg-integration-{unique_id}@example.com",
        "phone_number": "9876543210",
        "course_applied": "B.Tech",
        "branch_applied": "Computer Science",
    }


def test_postgres_admission_create_and_retrieve(pg_client):
    payload = valid_application()

    created = pg_client.post("/api/v1/admissions", json=payload)

    assert created.status_code == 201
    created_data = created.json()
    assert created_data["email"] == payload["email"]
    assert created_data["status"] == "submitted"

    retrieved = pg_client.get(
        f"/api/v1/admissions/{created_data['id']}"
    )

    assert retrieved.status_code == 200
    assert retrieved.json()["application_number"] == (
        created_data["application_number"]
    )


def test_postgres_admission_review(pg_client, monkeypatch):
    monkeypatch.setattr(settings, "enable_dev_review_endpoints", True)

    created = pg_client.post(
        "/api/v1/admissions",
        json=valid_application(),
    )

    assert created.status_code == 201
    admission_id = created.json()["id"]

    reviewed = pg_client.post(
        f"/api/v1/admissions/{admission_id}/approve",
        json={"remarks": "PostgreSQL integration test approval."},
    )

    assert reviewed.status_code == 200
    assert reviewed.json()["status"] == "approved"
    assert reviewed.json()["review_remarks"] == (
        "PostgreSQL integration test approval."
    )


def test_postgres_student_retrieval_and_update(pg_client):
    payload = valid_application()

    created_admission = pg_client.post(
        "/api/v1/admissions",
        json=payload,
    )

    assert created_admission.status_code == 201
    admission_id = created_admission.json()["id"]

    student_number = f"PG-TEST-{uuid4().hex[:16]}"

    with SessionLocal() as db:
        student = Student(
            student_number=student_number,
            admission_id=admission_id,
            full_name="PostgreSQL Integration Applicant",
            email=payload["email"],
            phone_number=payload["phone_number"],
            course="B.Tech",
            branch="Computer Science",
            current_year=1,
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        student_id = student.id

    retrieved = pg_client.get(f"/api/v1/students/{student_id}")

    assert retrieved.status_code == 200
    assert retrieved.json()["student_number"] == student_number

    updated = pg_client.patch(
        f"/api/v1/students/{student_id}",
        json={
            "email": f"pg-integration-updated-{uuid4().hex}@example.com",
            "phone_number": "9123456789",
        },
    )

    assert updated.status_code == 200
    assert updated.json()["phone_number"] == "9123456789"
    assert updated.json()["email"].startswith(
        "pg-integration-updated-"
    )
