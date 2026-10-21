
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

import app.main as main

client = TestClient(main.app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_database_health_connected(monkeypatch):
    def fake_database_check():
        return None

    monkeypatch.setattr(
        main,
        "check_database_connection",
        fake_database_check,
    )

    response = client.get("/health/db")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": "connected",
    }


def test_database_health_unavailable(monkeypatch):
    def fake_database_failure():
        raise SQLAlchemyError("Simulated database failure")

    monkeypatch.setattr(
        main,
        "check_database_connection",
        fake_database_failure,
    )

    response = client.get("/health/db")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Database connection unavailable"
    }
