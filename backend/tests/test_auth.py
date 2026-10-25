from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy import select

from app.config import settings
from app.models.user import User
from app.security import create_access_token, hash_password, verify_password
from conftest import TestingSessionLocal, TEST_JWT_SECRET


def test_password_hash_is_not_plaintext_and_verifies():
    stored = hash_password("Correct-Horse-Battery-123")
    assert stored != "Correct-Horse-Battery-123"
    assert verify_password("Correct-Horse-Battery-123", stored)
    assert not verify_password("wrong-password", stored)


def test_password_hash_rejects_short_password():
    try:
        hash_password("short")
    except ValueError as exc:
        assert "12 characters" in str(exc)
    else:
        raise AssertionError("Short password should be rejected")


def test_login_returns_bearer_token(client, make_user):
    make_user(email="login@example.com", role="admission_staff")
    # Replace fixture's known test password hash with a known credential.
    with TestingSessionLocal() as db:
        user = db.scalar(select(User).where(User.email == "login@example.com"))
        user.password_hash = hash_password("A-strong-test-password-123")
        db.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "A-strong-test-password-123"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["expires_in"] == settings.jwt_access_token_expire_minutes * 60

    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {response.json()['access_token']}"})
    assert me.status_code == 200
    assert me.json()["email"] == "login@example.com"
    assert me.json()["role"] == "admission_staff"


def test_login_rejects_wrong_password(client, make_user):
    make_user(email="login@example.com")
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "not-the-password"},
    )
    assert response.status_code == 401


def test_login_rejects_unknown_user(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "missing@example.com", "password": "not-the-password"},
    )
    assert response.status_code == 401


def test_protected_admission_list_requires_login(client):
    response = client.get("/api/v1/admissions")
    assert response.status_code == 401


def test_student_role_cannot_list_admissions(client, auth_headers):
    response = client.get("/api/v1/admissions", headers=auth_headers(role="student", student_id=None))
    assert response.status_code == 403


def test_invalid_token_is_rejected(client):
    response = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid-token"})
    assert response.status_code == 401


def test_expired_token_is_rejected(client, make_user):
    user_id = make_user()
    token = jwt.encode(
        {"sub": str(user_id), "role": "admin", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
        TEST_JWT_SECRET,
        algorithm="HS256",
    )
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_inactive_user_cannot_use_token(client, auth_headers):
    # A valid token is not sufficient if the account has since been deactivated.
    headers = auth_headers(email="inactive@example.com", active=False)
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 401


def test_student_can_only_access_linked_record(client, auth_headers):
    from app.models.student import Student
    from app.models.admission import Admission

    # Seed two linked admission/student records in the temporary test database.
    with TestingSessionLocal() as db:
        admissions = []
        for index in (1, 2):
            admission = Admission(
                application_number=f"APP-AUTH-{index}",
                full_name=f"Student {index}",
                email=f"student{index}@example.com",
                phone_number="9876543210",
                course_applied="B.Tech",
                branch_applied="Computer Science",
                status="submitted",
            )
            db.add(admission)
            db.flush()
            student = Student(
                student_number=f"STU-AUTH-{index}",
                admission_id=admission.id,
                full_name=f"Student {index}",
                email=f"student{index}@example.com",
                phone_number="9876543210",
                course="B.Tech",
                branch="Computer Science",
                current_year=1,
            )
            db.add(student)
            db.flush()
            admissions.append(student.id)
        db.commit()

    own_id, other_id = admissions
    headers = auth_headers(email="student1-login@example.com", role="student", student_id=own_id)
    assert client.get(f"/api/v1/students/{own_id}", headers=headers).status_code == 200
    assert client.get(f"/api/v1/students/{other_id}", headers=headers).status_code == 403
    denied_update = client.patch(
        f"/api/v1/students/{own_id}",
        json={"current_year": 2},
        headers=headers,
    )
    assert denied_update.status_code == 403
