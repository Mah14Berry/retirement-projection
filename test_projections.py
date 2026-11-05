import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from main import app
from projections import ProjectionRequest, project

client = TestClient(app)

def make_request(**overrides):
    data = {
        "current_age": 20,
        "retirement_age": 65,
        "salary": 60000,
        "current_balance": 0,
        "employee_rate": 0.06,
        "match_rate": 0.5,
        "match_cap": 0.06,
        "salary_growth": 0.03,
        "annual_return": 0.06,
        "annual_fee": 0.005,
    }
    data.update(overrides)
    return data

def test_zero_return_and_fee_is_simple_sum():
    req = ProjectionRequest(**make_request(
        current_age=30,
        retirement_age=32,
        salary=100000,
        employee_rate=0.10,
        match_rate=0,
        salary_growth=0,
        annual_return=0,
        annual_fee=0,
    ))
    rows = project(req)
    assert len(rows) == 2
    assert rows[-1]["balance"] == 20000

def test_match_is_capped():
    req = ProjectionRequest(**make_request(
        current_age=30,
        retirement_age=31,
        salary=100000,
        employee_rate=0.10,
        match_rate=0.5,
        match_cap=0.06,
        annual_return=0,
        annual_fee=0,
    ))
    rows = project(req)
    assert rows[0]["employer"] == 3000

def test_retirement_before_current_age_rejected():
    with pytest.raises(ValidationError):
        ProjectionRequest(**make_request(current_age=40, retirement_age=30))

def test_api_returns_projection():
    response = client.post("/projections", json=make_request())
    assert response.status_code == 200
    body = response.json()
    assert len(body["years"]) == 45
    assert body["final_balance"] == body["years"][-1]["balance"]

def test_api_rejects_bad_input():
    response = client.post("/projections", json=make_request(salary=-1))
    assert response.status_code == 422