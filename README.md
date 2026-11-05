# Retirement Projection Service

A REST API that shows how contribution rate, employer match, and fees affect retirement savings over time.

## Problem

People often don't see how small changes, like contributing a bit more to capture a full employer match or paying a lower fee, compound over decades. This service takes a few inputs and returns a year-by-year projection of the balance.

## How it works

Send a `POST` request to `/projections` with:

| Field | Meaning |
|---|---|
| `current_age`, `retirement_age` | Ages in years (retirement must be after current) |
| `salary` | Current annual salary |
| `current_balance` | Existing savings |
| `employee_rate` | Share of salary the employee contributes (0.06 = 6%) |
| `match_rate` | Employer match on contributions (0.5 = 50 cents per dollar) |
| `match_cap` | Max share of salary the employer will match (0.06 = 6%) |
| `salary_growth` | Yearly raise (default 0.03) |
| `annual_return` | Yearly investment return (default 0.06) |
| `annual_fee` | Yearly fee as a share of the balance (default 0.005) |

The response contains `final_balance` and a `years` list with age, salary, employee contribution, employer contribution, and balance for each year.

Each year: contributions are added to the balance, then the balance grows by `annual_return - annual_fee`. The employer match applies only to contributions up to `match_cap`.

Invalid input, such as a negative salary or a retirement age at or below the current age, returns a 422 error.

## Assumptions and limitations

- Returns, raises, and fees are fixed every year. Real markets vary.
- No taxes, inflation, contribution limits, or withdrawals.
- Contributions are made once per year, not monthly.
- This is an educational project, not financial advice.

## Run it

```bash
pip install fastapi uvicorn pydantic pytest httpx
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` to try the API.

## Test it

```bash
pytest
```
