from pydantic import BaseModel
from tax_data import TaxValues, TaxEntry, TaxFlatValues
from typing import Optional


class TaxData(BaseModel):
    brutto: float
    insurance: float
    tax: float
    netto: Optional[float]


class WorkerTaxSummary(BaseModel):
    monthly: TaxData
    vacation: TaxData
    christmas: TaxData
    yearly: TaxData

class FreelanceTaxSummary(BaseModel):
    total: TaxData

def calc_freelance_taxes(income: float, tax_values: TaxValues) -> FreelanceTaxSummary:
    insurance = 0 # TODO
    taxable = income - insurance
    tax = _calc_with_entries_stacked(taxable, tax_values)
    total = TaxData(brutto=income, insurance=insurance, tax=tax)
    total.netto = _calc_netto(total)

    # TODO: flag if also an employee

    # Umsatzsteuer?
    # Ausgaben? Pauschalisierung?
    # Gewinnfreibetrag

    return FreelanceTaxSummary(total=total)


def calc_work_taxes(income: float, tax_values: TaxValues) -> WorkerTaxSummary:
    insurance = _calc_insurance(income, tax_values.insurance_work)
    work_tax = _calc_work_tax(
        income - insurance, tax_values.tax_work, tax_values.flat)
    monthly = TaxData(brutto=income, insurance=insurance, tax=work_tax)
    monthly.netto = _calc_netto(monthly)

    other_insurance = _calc_insurance(income, tax_values.insurance_work_other)
    vacation_tax = _calc_with_entries_stacked(
        income - other_insurance, tax_values.tax_work_other)
    total_other_tax = _calc_with_entries_stacked(
        (income - other_insurance) * 2, tax_values.tax_work_other)
    christmas_tax = total_other_tax - vacation_tax

    vacation = TaxData(
        brutto=income, insurance=other_insurance, tax=vacation_tax)
    vacation.netto = _calc_netto(vacation)
    christmas = TaxData(
        brutto=income, insurance=other_insurance, tax=christmas_tax)
    christmas.netto = _calc_netto(christmas)

    return WorkerTaxSummary(
        monthly=monthly,
        vacation=vacation,
        christmas=christmas,
        yearly=_calc_yearly(monthly, vacation, christmas)
    )


def _calc_netto(data: TaxData) -> float:
    return data.brutto - data.insurance - data.tax


def _calc_yearly(monthly: TaxData, vacation: TaxData, christmas: TaxData):
    brutto = monthly.brutto * 12 + vacation.brutto + christmas.brutto
    insurance = monthly.insurance * 12 + \
        vacation.insurance + christmas.insurance
    tax = monthly.tax * 12 + vacation.tax + christmas.tax
    data = TaxData(brutto=brutto, insurance=insurance, tax=tax)
    data.netto = _calc_netto(data)
    return data


def _calc_insurance(value: float, tax_entries: list[TaxEntry]) -> float:
    entry = _find_entry_for_value(value, tax_entries)
    if entry.absolute:
        return entry.absolute
    return value * entry.percentage


def _calc_work_tax(value: float, tax_entries: list[TaxEntry], flat: TaxFlatValues) -> float:
    entry = _find_entry_for_value(value, tax_entries)
    taxes = value * entry.percentage

    # Assuming no AVAB, not considering children
    if entry.absolute:
        taxes -= entry.absolute

    taxes -= flat.verkehr / 12
    return taxes


def _find_entry_for_value(value: float, tax_entries: list[TaxEntry]) -> TaxEntry:
    for entry in tax_entries:
        if entry.range_from <= value and (entry.range_to == None or entry.range_to >= value):
            return entry
    return None


def _calc_with_entries_stacked(value: float, tax_entries: list[TaxEntry]) -> float:
    curr = value
    last = 0
    total = 0
    for entry in tax_entries:
        range = entry.range_to - last
        curr -= range

        taxable_value = (range + curr) if curr <= 0 else range
        total += taxable_value * entry.percentage

        if curr <= 0:
            break

        last = entry.range_to

    return total
