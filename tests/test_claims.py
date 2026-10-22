
from datetime import date
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=test_engine)

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
    Base.metadata.drop_all(bind=test_engine)


def valid_claim(reference="CLM-TEST-1001"):
    return {
        "claim_reference": reference,
        "patient_reference": "PAT-TEST-1001",
        "service_date": "2026-10-20",
        "service_category": "consultation",
        "claim_amount": "250.00",
        "diagnosis_code": "DIA-101",
    }


def test_create_claim(client):
    response = client.post(
        "/api/v1/claims",
        json=valid_claim(),
    )

    assert response.status_code == 201
    body = response.json()
    assert body["claim_reference"] == "CLM-TEST-1001"
    assert body["id"] > 0
    assert body["status"] == "submitted"


def test_list_claims(client):
    client.post("/api/v1/claims", json=valid_claim())

    response = client.get("/api/v1/claims")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_existing_claim(client):
    created = client.post(
        "/api/v1/claims",
        json=valid_claim(),
    ).json()

    response = client.get(f"/api/v1/claims/{created['id']}")

    assert response.status_code == 200
    assert response.json()["claim_reference"] == "CLM-TEST-1001"


def test_missing_claim_returns_404(client):
    response = client.get("/api/v1/claims/999999")

    assert response.status_code == 404


def test_invalid_amount_is_rejected(client):
    payload = valid_claim()
    payload["claim_amount"] = "-10.00"

    response = client.post("/api/v1/claims", json=payload)

    assert response.status_code == 422
