from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.database import get_db
from app.schemas import (
    FutureValueInput, LoanEMIInput, SavingsPlanInput,
    MortgageInput, InvestmentReturnInput, CalculatorResult
)
from app.services.calculator import (
    calculate_future_value, calculate_loan_emi, calculate_savings_plan,
    calculate_mortgage, calculate_investment_return
)
from app.services.auth import get_current_user
from app.models.user import User, CalculatorHistory

router = APIRouter(prefix="/calculator", tags=["Financial Calculators"])


async def save_calculation(
    db: AsyncSession,
    user: User,
    calc_type: str,
    inputs: dict,
    result: dict
):
    """Save calculation to history if user is logged in"""
    if user:
        history = CalculatorHistory(
            user_id=user.id,
            calculator_type=calc_type,
            inputs=json.dumps(inputs),
            result=json.dumps(result)
        )
        db.add(history)
        await db.commit()


@router.post("/future-value", response_model=CalculatorResult)
async def api_future_value(
    data: FutureValueInput,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate future value with compound interest"""
    result = calculate_future_value(data)
    await save_calculation(db, current_user, "future_value", data.model_dump(), result.model_dump())
    return result


@router.post("/loan-emi", response_model=CalculatorResult)
async def api_loan_emi(
    data: LoanEMIInput,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate loan EMI (Equated Monthly Installment)"""
    result = calculate_loan_emi(data)
    await save_calculation(db, current_user, "loan_emi", data.model_dump(), result.model_dump())
    return result


@router.post("/savings-plan", response_model=CalculatorResult)
async def api_savings_plan(
    data: SavingsPlanInput,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate savings plan growth"""
    result = calculate_savings_plan(data)
    await save_calculation(db, current_user, "savings_plan", data.model_dump(), result.model_dump())
    return result


@router.post("/mortgage", response_model=CalculatorResult)
async def api_mortgage(
    data: MortgageInput,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate mortgage payments"""
    result = calculate_mortgage(data)
    await save_calculation(db, current_user, "mortgage", data.model_dump(), result.model_dump())
    return result


@router.post("/investment-return", response_model=CalculatorResult)
async def api_investment_return(
    data: InvestmentReturnInput,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate investment returns"""
    result = calculate_investment_return(data)
    await save_calculation(db, current_user, "investment_return", data.model_dump(), result.model_dump())
    return result
