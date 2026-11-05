from pydantic import BaseModel, Field, model_validator

class ProjectionRequest(BaseModel):
    current_age: int = Field(ge=18, le=80)
    retirement_age: int = Field(gt=18, le=90)
    salary: float = Field(gt=0)
    current_balance: float = Field(ge=0)
    employee_rate: float = Field(ge=0, le=1)
    match_rate: float = Field(ge=0, le=1)
    match_cap: float = Field(ge=0, le=1)
    salary_growth: float = 0.03
    annual_return: float = 0.06
    annual_fee: float = 0.005
    
    @model_validator(mode="after")
    def check_ages(self):
        if self.retirement_age <= self.current_age:
            raise ValueError("retirement_age must be greater than current_age")
        return self

def project(req: ProjectionRequest):
    rows = []
    balance = req.current_balance
    salary = req.salary
    for age in range(req.current_age, req.retirement_age):
        employee = salary * req.employee_rate
        employer = salary * min(req.employee_rate, req.match_cap) * req.match_rate
        balance = (balance + employee + employer) * (1 + req.annual_return - req.annual_fee)
        rows.append({
            "age": age + 1,
            "salary": round(salary, 2),
            "employee": round(employee, 2),
            "employer": round(employer, 2),
            "balance": round(balance, 2),
        })
        salary *= 1 + req.salary_growth
    return rows