import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

RUN_POSTGRES_INTEGRATION_TESTS = (
    os.getenv("COLLEGE_ERP_RUN_PG_TESTS") == "1"
)
POSTGRES_TEST_DATABASE = "college_erp_test"

if RUN_POSTGRES_INTEGRATION_TESTS:
    os.environ["POSTGRES_DB"] = POSTGRES_TEST_DATABASE

from app.config import settings
from app.database import engine as postgres_engine
from app.database import get_db
from app.main import app
from app.models import Base, User
from app.security import create_access_token, hash_password

if (
    RUN_POSTGRES_INTEGRATION_TESTS
    and postgres_engine.url.database != POSTGRES_TEST_DATABASE
):
    raise pytest.UsageError(
        "PostgreSQL integration tests must use the college_erp_test database; "
        f"refusing to run against {postgres_engine.url.database!r}."
    )

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
TEST_JWT_SECRET = "test-only-signing-key-at-least-32-characters-long"


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(settings, "jwt_secret_key", TEST_JWT_SECRET)
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


@pytest.fixture
def make_user():
    def factory(email="staff@example.com", role="admission_staff", student_id=None, active=True):
        with TestingSessionLocal() as db:
            user = User(
                email=email,
                password_hash=hash_password("A-strong-test-password-123"),
                role=role,
                student_id=student_id,
                is_active=active,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user.id
    return factory


@pytest.fixture
def auth_headers(make_user):
    def factory(email="staff@example.com", role="admission_staff", student_id=None, active=True):
        user_id = make_user(email=email, role=role, student_id=student_id, active=active)
        token = create_access_token(user_id=user_id, role=role, student_id=student_id)
        return {"Authorization": f"Bearer {token}"}
    return factory
