import re
from dataclasses import dataclass


@dataclass
class CalculatorResult:
    answer: str
    calculation_type: str



_NUMBER = r"[\d,]+(?:\.\d+)?"
_NUMBER_CAPTURE = rf"(?<![\w.])({_NUMBER})(?![\w.])"


def _to_float(raw: str) -> float:
    return float(raw.replace(",", ""))


def _find_number(text: str, patterns: list[str]) -> float | None:
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return _to_float(match.group(1))
    return None


def _parse_calculation_values(text: str) -> tuple[float, float, float] | None:
    amount = _find_number(
        text,
        [
            rf"(?:amount|loan|principal|borrow(?:ed)?)\s*(?:is|of|=)?\s*{_NUMBER_CAPTURE}",
            rf"{_NUMBER_CAPTURE}\s*(?:amount|loan|principal)",
            _NUMBER_CAPTURE,
        ],
    )
    rate = _find_number(
        text,
        [
            rf"{_NUMBER_CAPTURE}\s*(?:%|percent|per\s*cent)",
            rf"\brate\s*(?:of|is|=)?\s*{_NUMBER_CAPTURE}",
        ],
    )
    years = _find_number(text, [rf"{_NUMBER_CAPTURE}\s*years?"])

    if amount is None or rate is None or years is None:
        return None
    if amount <= 0 or rate < 0 or years <= 0:
        return None
    return amount, rate, years


def try_emi_calculation(text: str) -> CalculatorResult | None:
    lower = text.lower()
    emi_keywords = ["emi", "loan", "installment"]
    if not any(word in lower for word in emi_keywords):
        return None

    values = _parse_calculation_values(lower)
    if values is None:
        return None
    principal, rate_percent, years = values

    monthly_rate = rate_percent / 12 / 100
    months = years * 12

    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** months
            / ((1 + monthly_rate) ** months - 1)
        )

    total_paid = emi * months
    total_interest = total_paid - principal

    answer = (
        f"For a loan of {principal:,.0f} at {rate_percent:g}% annual interest over {years:g} years, "
        f"your estimated EMI would be about {emi:,.2f} per month. "
        f"Over the full term, you'd pay roughly {total_interest:,.2f} in total interest, "
        f"for a total repayment of about {total_paid:,.2f}. "
        f"This is an estimate; your actual bank may calculate slightly differently."
    )
    return CalculatorResult(answer=answer, calculation_type="emi")


def try_savings_calculation(text: str) -> CalculatorResult | None:
    """
    Looks for a savings/compound-interest question containing an
    amount, a rate, and a duration in years.
    """
    lower = text.lower()
    savings_keywords = ["interest", "saving", "save", "deposit", "grow", "invest"]
    if not any(word in lower for word in savings_keywords):
        return None

    values = _parse_calculation_values(lower)
    if values is None:
        return None
    principal, rate_percent, years = values

    final_amount = principal * (1 + rate_percent / 100) ** years
    interest_earned = final_amount - principal

    answer = (
        f"If you save {principal:,.0f} at {rate_percent:g}% annual interest (compounded yearly) "
        f"for {years:g} years, it would grow to about {final_amount:,.2f}, "
        f"earning roughly {interest_earned:,.2f} in interest. "
        f"This is a simplified estimate; real accounts may compound monthly or daily, "
        f"and rates can change over time."
    )
    return CalculatorResult(answer=answer, calculation_type="savings")


def try_calculate(text: str) -> CalculatorResult | None:
    """Tries each calculator in turn; returns the first that matches."""
    return try_emi_calculation(text) or try_savings_calculation(text)