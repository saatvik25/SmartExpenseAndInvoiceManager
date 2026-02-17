import pytest

def test_summary_financial_accuracy(client):
    """Business Logic: Verify precise aggregation and category grouping"""
    # Seed specific data
    test_data = [
        {"title": "Coffee", "amount": 5.25, "category": "Food", "date": "2026-03-01"},
        {"title": "Lunch", "amount": 15.75, "category": "Food", "date": "2026-03-05"},
        {"title": "Fuel", "amount": 50.00, "category": "Transport", "date": "2026-03-10"},
        {"title": "Other Month", "amount": 100.00, "category": "Food", "date": "2026-04-01"},
    ]
    
    for item in test_data:
        client.post("/expenses/", json=item)
        
    response = client.get("/expenses/summary?month=3&year=2026")
    assert response.status_code == 200
    data = response.json()
    
    # Verify total (5.25 + 15.75 + 50.00 = 71.00)
    assert data["total_spent"] == 71.00
    
    # Verify breakdown
    categories = {item["category"]: item["total"] for item in data["breakdown"]}
    assert len(categories) == 2
    assert categories["Food"] == 21.00
    assert categories["Transport"] == 50.00

def test_summary_empty_results(client):
    """Business Logic: Ensure summary returns 0s instead of erroring for empty months"""
    response = client.get("/expenses/summary?month=12&year=2020")
    assert response.status_code == 200
    data = response.json()
    assert data["total_spent"] == 0
    assert data["breakdown"] == []

def test_summary_invalid_query_params(client):
    """API Validation: Verify invalid month/year ranges are rejected"""
    # Month > 12
    response = client.get("/expenses/summary?month=13&year=2026")
    assert response.status_code == 422
    
    # Year in wrong range (if restricted)
    response = client.get("/expenses/summary?month=1&year=1900")
    assert response.status_code == 422

def test_summary_float_precision(client):
    """QA/Financial: Verify handling of high-precision floats to avoid rounding errors in aggregation"""
    payload1 = {"title": "Tiny 1", "amount": 0.01, "category": "Misc", "date": "2026-05-01"}
    payload2 = {"title": "Tiny 2", "amount": 0.02, "category": "Misc", "date": "2026-05-01"}
    
    client.post("/expenses/", json=payload1)
    client.post("/expenses/", json=payload2)
    
    response = client.get("/expenses/summary?month=5&year=2026")
    assert response.status_code == 200
    assert response.json()["total_spent"] == 0.03
