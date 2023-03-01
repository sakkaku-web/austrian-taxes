from flask import Flask, request
from tax_data import get_tax_values
from tax_calc import calc_work_taxes
from datetime import datetime

app = Flask(__name__)


@app.post("/api/tax-worker")
def calc_tax_worker():
    data = request.json
    year = data['year'] if 'year' in data else datetime.now().year
    tax_values = get_tax_values(year)
    if tax_values:
        return calc_work_taxes(data['income'], tax_values).dict()

    return {'message': f'No tax information for year {year}'}, 400


@app.get("/api/tax/<int:year>")
def tax_value(year):
    return get_tax_values(year).dict()
