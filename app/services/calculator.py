from app.schemas import (
    FutureValueInput, LoanEMIInput, SavingsPlanInput,
    MortgageInput, InvestmentReturnInput, CalculatorResult
)


def calculate_future_value(data: FutureValueInput) -> CalculatorResult:
    """Calculate future value with compound interest: A = P(1 + r/n)^(nt)"""
    P = data.principal
    r = data.rate / 100
    n = data.compounds_per_year
    t = data.time
    
    future_value = P * (1 + r / n) ** (n * t)
    total_interest = future_value - P
    
    result = {
        "principal": round(P, 2),
        "future_value": round(future_value, 2),
        "total_interest": round(total_interest, 2),
        "rate": data.rate,
        "time_years": t,
        "compounds_per_year": n
    }
    
    summary = f"An investment of ₹{P:,.2f} at {data.rate}% annual interest compounded {n} times per year for {t} years will grow to ₹{future_value:,.2f}. Total interest earned: ₹{total_interest:,.2f}"
    
    return CalculatorResult(result=result, summary=summary)


def calculate_loan_emi(data: LoanEMIInput) -> CalculatorResult:
    """Calculate EMI using formula: EMI = P * r * (1+r)^n / ((1+r)^n - 1)"""
    P = data.principal
    r = data.rate / 100 / 12  # Monthly rate
    n = data.tenure_months
    
    if r == 0:
        emi = P / n
    else:
        emi = P * r * (1 + r) ** n / ((1 + r) ** n - 1)
    
    total_payment = emi * n
    total_interest = total_payment - P
    
    result = {
        "loan_amount": round(P, 2),
        "monthly_emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
        "rate": data.rate,
        "tenure_months": n
    }
    
    summary = f"For a loan of ₹{P:,.2f} at {data.rate}% annual interest for {n} months, your monthly EMI will be ₹{emi:,.2f}. Total payment: ₹{total_payment:,.2f} (Interest: ₹{total_interest:,.2f})"
    
    return CalculatorResult(result=result, summary=summary)


def calculate_savings_plan(data: SavingsPlanInput) -> CalculatorResult:
    """Calculate savings growth with annual contributions"""
    initial = data.initial_savings
    annual = data.annual_contribution
    r = data.rate / 100
    years = data.years
    
    # Future value of initial savings
    fv_initial = initial * (1 + r) ** years
    
    # Future value of annual contributions (annuity)
    if r == 0:
        fv_contributions = annual * years
    else:
        fv_contributions = annual * ((1 + r) ** years - 1) / r
    
    total_value = fv_initial + fv_contributions
    total_contributions = initial + (annual * years)
    total_interest = total_value - total_contributions
    
    result = {
        "initial_savings": round(initial, 2),
        "annual_contribution": round(annual, 2),
        "total_contributions": round(total_contributions, 2),
        "future_value": round(total_value, 2),
        "total_interest": round(total_interest, 2),
        "rate": data.rate,
        "years": years
    }
    
    summary = f"Starting with ₹{initial:,.2f} and saving ₹{annual:,.2f} annually at {data.rate}% for {years} years, you'll accumulate ₹{total_value:,.2f}. Total interest earned: ₹{total_interest:,.2f}"
    
    return CalculatorResult(result=result, summary=summary)


def calculate_mortgage(data: MortgageInput) -> CalculatorResult:
    """Calculate mortgage with taxes and insurance"""
    home_price = data.home_price
    down_payment = data.down_payment
    loan_amount = home_price - down_payment
    r = data.rate / 100 / 12  # Monthly rate
    n = data.tenure_years * 12  # Total months
    
    # Monthly principal & interest
    if r == 0:
        monthly_pi = loan_amount / n
    else:
        monthly_pi = loan_amount * r * (1 + r) ** n / ((1 + r) ** n - 1)
    
    # Monthly taxes and insurance
    monthly_tax = (home_price * data.property_tax_rate / 100) / 12
    monthly_insurance = (home_price * data.insurance_rate / 100) / 12
    
    total_monthly = monthly_pi + monthly_tax + monthly_insurance
    total_payment = monthly_pi * n
    total_interest = total_payment - loan_amount
    
    result = {
        "home_price": round(home_price, 2),
        "down_payment": round(down_payment, 2),
        "loan_amount": round(loan_amount, 2),
        "monthly_principal_interest": round(monthly_pi, 2),
        "monthly_tax": round(monthly_tax, 2),
        "monthly_insurance": round(monthly_insurance, 2),
        "total_monthly_payment": round(total_monthly, 2),
        "total_interest": round(total_interest, 2),
        "rate": data.rate,
        "tenure_years": data.tenure_years
    }
    
    summary = f"For a ₹{home_price:,.2f} property with ₹{down_payment:,.2f} down payment, your monthly payment will be ₹{total_monthly:,.2f} (P&I: ₹{monthly_pi:,.2f}, Tax: ₹{monthly_tax:,.2f}, Insurance: ₹{monthly_insurance:,.2f})"
    
    return CalculatorResult(result=result, summary=summary)


def calculate_investment_return(data: InvestmentReturnInput) -> CalculatorResult:
    """Calculate simple investment returns"""
    P = data.principal
    r = data.rate / 100
    years = data.years
    
    future_value = P * (1 + r) ** years
    total_return = future_value - P
    cagr = ((future_value / P) ** (1 / years) - 1) * 100
    
    # Year-by-year breakdown
    yearly_values = []
    for year in range(1, years + 1):
        value = P * (1 + r) ** year
        yearly_values.append({"year": year, "value": round(value, 2)})
    
    result = {
        "principal": round(P, 2),
        "future_value": round(future_value, 2),
        "total_return": round(total_return, 2),
        "return_percentage": round((total_return / P) * 100, 2),
        "cagr": round(cagr, 2),
        "rate": data.rate,
        "years": years,
        "yearly_breakdown": yearly_values
    }
    
    summary = f"An investment of ₹{P:,.2f} at {data.rate}% annual return for {years} years will grow to ₹{future_value:,.2f}. Total return: ₹{total_return:,.2f} ({(total_return/P)*100:.1f}%)"
    
    return CalculatorResult(result=result, summary=summary)
