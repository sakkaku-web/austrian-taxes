from flask import Flask, request
from tax_data import get_tax_values
from tax_calc import calc_work_taxes, calc_freelance_taxes
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

app = Flask(__name__)


class CalculationRequest(BaseModel):
    income: float
    year: Optional[int]


def _parse_request() -> CalculationRequest:
    data = request.json
    year = data['year'] if 'year' in data else datetime.now().year
    return CalculationRequest(income=data['income'], year=year)


@app.post("/api/tax-freelance")
def calc_tax_freelance():
    req = _parse_request()
    tax_values = get_tax_values(req.year)
    if tax_values:
        return calc_freelance_taxes(req.income, tax_values).dict()

    return {'message': f'No tax information for year {req.year}'}, 400


@app.post("/api/tax-employee")
def calc_tax_employee():
    req = _parse_request()
    tax_values = get_tax_values(req.year)
    if tax_values:
        return calc_work_taxes(req.income, tax_values).dict()

    return {'message': f'No tax information for year {req.year}'}, 400


@app.get("/api/tax/<int:year>")
def tax_value(year):
    return get_tax_values(year).dict()
