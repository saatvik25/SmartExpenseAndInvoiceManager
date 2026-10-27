import pytest
from datetime import date


def test_create_expense_success(client):
    """Functional: Verify expense creation with valid data"""
    payload = {
        "title": "Business Lunch",
        "amount": 45.50,
        "category": "Travel",
        "date": "2026-02-17"
    }
    response = client.post("/expenses/", json=payload)
    
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["amount"] == payload["amount"]
    assert data["category"] == payload["category"]
    assert data["date"] == payload["date"]
    assert "id" in data
    assert "created_at" in data

def test_read_expenses_persistence(client):
    """Integration: Ensure created expenses are persisted and retrievable"""
    payload = {"title": "Test Exp", "amount": 10.0, "category": "General", "date": "2026-02-17"}
    client.post("/expenses/", json=payload)
    
    response = client.get("/expenses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(item["title"] == "Test Exp" for item in data)

def test_create_expense_invalid_negative_amount(client):
    """Negative: Verify that negative amounts are rejected (Validation Layer)"""
    payload = {
        "title": "Invalid Lunch",
        "amount": -10.0,
        "category": "Food",
        "date": "2026-02-17"
    }
    response = client.post("/expenses/", json=payload)
    assert response.status_code == 422
    # Check that it's a validation error for 'amount'
    errors = response.json()["detail"]
    assert any(err["loc"][-1] == "amount" for err in errors)

def test_create_expense_missing_required_fields(client):
    """Negative: Verify missing required fields are caught"""
    payload = {"amount": 10.0} # Missing title, category, date
    response = client.post("/expenses/", json=payload)
    assert response.status_code == 422

def test_create_expense_invalid_date_format(client):
    """Negative: Verify invalid date formats are rejected"""
    payload = {
        "title": "Bad Date",
        "amount": 10.0,
        "category": "Misc",
        "date": "17-02-2026" # Wrong format (ISO 8601 expected)
    }
    response = client.post("/expenses/", json=payload)
    assert response.status_code == 422

def test_create_expense_wrong_types(client):
    """Negative: Verify wrong data types (e.g. amount as string) are handled if not castable"""
    payload = {
        "title": "String Amount",
        "amount": "not-a-number",
        "category": "Misc",
        "date": "2026-02-17"
    }
    response = client.post("/expenses/", json=payload)
    assert response.status_code == 422

def test_create_expense_large_values(client):
    """Functional/Edge: Verify handling of large financial values"""
    payload = {
        "title": "Large Purchase",
        "amount": 999999999.99,
        "category": "Investment",
        "date": "2026-02-17"
    }
    response = client.post("/expenses/", json=payload)
    assert response.status_code == 201
    assert response.json()["amount"] == 999999999.99
