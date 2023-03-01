from flask import Flask, request
from tax_data import get_tax_values
from tax_calc import calc_work_taxes

app = Flask(__name__)


@app.post("/api/tax-worker")
def calc_tax_worker():
    data = request.json
    tax_values = get_tax_values()

    return calc_work_taxes(data['income'], tax_values).dict()


@app.get("/api/tax/<int:year>")
def tax_value(year):
    return get_tax_values(year).dict()
