import pytest
from fastapi.testclient import TestClient
from main import app
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


client = TestClient(app)

def test_create_service_entry_success():
    # Arrange: Prepare a valid service entry payload
    payload = {
        "number_plate": "WP-CA-1234",
        "vehicle_type": "car",
        "service_types": ["oil_change", "filter_change"],
        "amount": 251.0,
        "date": "2028-08-30",
        "start_time": "09:30",
        "end_time": "10:15",
        "telephone_number": "0771234567"
    }

    # Act: Send POST request
    response = client.post("/service-entry", json=payload)
    data = response.json()

    # Assert: Check response status and content
    assert response.status_code == 200
    assert data["status"] == "success"
    assert "RevenueProcessor" in data["analytics"]

def test_create_service_entry_missing_field():
    # Arrange: Payload missing 'vehicle_type'
    payload = {
        "number_plate": "WP-CA-1234",
        "service_types": ["oil_change", "filter_change"],
        "amount": 251.0,
        "date": "2028-08-30",
        "start_time": "09:30",
        "end_time": "10:15",
        "telephone_number": "0771234567"
    }

    # Act: Send POST request
    response = client.post("/service-entry", json=payload)
    data = response.json()

    # Assert: Should return 422 Unprocessable Entity due to missing field
    assert response.status_code == 422
    assert "detail" in data
