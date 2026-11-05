from fastapi import FastAPI
from projections import ProjectionRequest, project
app = FastAPI()

@app.post("/projections")
def create_projection(req: ProjectionRequest):
    rows = project(req)
    return {"final_balance": rows[-1]["balance"], "years": rows}