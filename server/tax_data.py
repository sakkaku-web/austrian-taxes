from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from db import tax_values


class TaxEntry(BaseModel):
    range_from: float
    range_to: Optional[float]
    percentage: Optional[float]
    absolute: Optional[float]


class TaxFlatValues(BaseModel):
    werbung: float
    sonderausgaben: float
    verkehr: float
    freibetrag: float
    einschleifregelung: float


class TaxValues(BaseModel):
    tax_self: list[TaxEntry]
    tax_work: list[TaxEntry]
    tax_work_other: list[TaxEntry]
    insurance_work: list[TaxEntry]
    insurance_work_other: list[TaxEntry]
    flat: TaxFlatValues


def get_tax_values(year=datetime.now().year) -> TaxValues:
    if year in tax_values:
        data = tax_values[year]
        insurance_work = _parse_tax_entries(data['insurance-work'])
        insurance_work_other = _parse_tax_entries(data['insurance-other-work'])
        tax_self = _parse_tax_entries(data['tax-self'])
        tax_work = _parse_tax_entries(data['tax-work'])

        for i in range(0, len(tax_work)):
            tax_work[i].percentage = tax_self[i].percentage

        tax_work_other = _parse_tax_entries(data['tax-other'])
        flat_values = _parse_flat_values(data['flat'])

        return TaxValues(
            tax_self=tax_self,
            tax_work=tax_work,
            tax_work_other=tax_work_other,
            insurance_work=insurance_work,
            insurance_work_other=insurance_work_other,
            flat=flat_values
        )
    else:
        return None


def _parse_tax_entries(obj: dict) -> list[TaxEntry]:
    curr = 0
    percentage = 0
    absolute = None
    result = []
    for key in obj.keys():
        value = obj[key]
        result.append(TaxEntry(range_from=curr, range_to=key,
                      percentage=percentage, absolute=absolute))

        percentage = value if value <= 1 else None
        absolute = value if value > 1 else None
        curr = key
    
    result.append(TaxEntry(range_from=curr, range_to=None, percentage=percentage, absolute=absolute))

    return result


def _parse_flat_values(obj: dict) -> TaxFlatValues:
    return TaxFlatValues(
        werbung=obj['werbung'],
        sonderausgaben=obj['sonder'],
        verkehr=obj['verkehr'],
        freibetrag=obj['free'],
        einschleifregelung=obj['partial']
    )
