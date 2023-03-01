from flask import Flask, request
from pydantic import BaseModel
from tax_service import get_tax_values

app = Flask(__name__)


@app.post("/api/tax-worker")
def calc_tax_worker():
    return {'test': True}


@app.get("/api/tax/<int:year>")
def tax_value(year):
    return get_tax_values(year).dict()
