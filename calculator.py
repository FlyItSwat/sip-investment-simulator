"""Pure calculation functions for SIP and lump-sum investment projections.

Assumptions: nominal annual return compounded monthly; contributions at month-end;
inflation applied monthly; no taxes, fees, or return volatility.
"""
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Projection:
    months: List[int]
    invested: List[float]
    nominal: List[float]
    real: List[float]

def project(monthly_sip: float, initial: float, years: int,
            annual_return: float, inflation: float = 0.0,
            annual_step_up: float = 0.0) -> Projection:
    """Return monthly projections; rates supplied as percentages (e.g. 12 for 12%)."""
    if monthly_sip < 0 or initial < 0:
        raise ValueError("Contributions must be non-negative")
    if not 1 <= years <= 60:
        raise ValueError("Years must be between 1 and 60")
    if annual_return <= -100 or inflation <= -100 or annual_step_up <= -100:
        raise ValueError("Percentage rates must exceed -100")
    months = [0]
    invested = [float(initial)]
    nominal = [float(initial)]
    real = [float(initial)]
    balance = float(initial)
    total_paid = float(initial)
    monthly_rate = annual_return / 1200
    inflation_factor = 1 + inflation / 1200
    for month in range(1, years * 12 + 1):
        year_index = (month - 1) // 12
        contribution = monthly_sip * (1 + annual_step_up / 100) ** year_index
        balance = balance * (1 + monthly_rate) + contribution
        total_paid += contribution
        months.append(month)
        invested.append(total_paid)
        nominal.append(balance)
        real.append(balance / (inflation_factor ** month))
    return Projection(months, invested, nominal, real)

def inr(amount: float) -> str:
    """Indian digit grouping for currency."""
    sign = "-" if amount < 0 else ""
    whole = f"{abs(amount):,.2f}"
    integer, decimal = whole.split(".")
    digits = integer.replace(",", "")
    if len(digits) > 3:
        integer = digits[:-3]
        groups = []
        while len(integer) > 2:
            groups.insert(0, integer[-2:])
            integer = integer[:-2]
        if integer:
            groups.insert(0, integer)
        integer = ",".join(groups) + "," + digits[-3:]
    else:
        integer = digits
    return f"{sign}₹{integer}.{decimal}"
