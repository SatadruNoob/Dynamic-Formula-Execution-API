from fastapi import FastAPI
from app.models import FormulaPayload
from app.services import execute_formulas

app = FastAPI()

@app.post("/api/execute-formula")
async def execute_formula(payload: FormulaPayload):
    result = execute_formulas(payload)
    return result
