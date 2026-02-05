from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Auth Schemas
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Calculator Schemas
class FutureValueInput(BaseModel):
    principal: float = Field(..., gt=0, description="Initial investment amount")
    rate: float = Field(..., ge=0, le=100, description="Annual interest rate (%)")
    time: float = Field(..., gt=0, description="Time period in years")
    compounds_per_year: int = Field(default=12, ge=1, description="Compounding frequency")


class LoanEMIInput(BaseModel):
    principal: float = Field(..., gt=0, description="Loan amount")
    rate: float = Field(..., ge=0, le=100, description="Annual interest rate (%)")
    tenure_months: int = Field(..., gt=0, description="Loan tenure in months")


class SavingsPlanInput(BaseModel):
    initial_savings: float = Field(..., ge=0, description="Initial savings amount")
    annual_contribution: float = Field(..., ge=0, description="Yearly contribution")
    rate: float = Field(..., ge=0, le=100, description="Annual interest rate (%)")
    years: int = Field(..., gt=0, description="Investment period in years")


class MortgageInput(BaseModel):
    home_price: float = Field(..., gt=0, description="Property price")
    down_payment: float = Field(..., ge=0, description="Down payment amount")
    rate: float = Field(..., ge=0, le=100, description="Annual interest rate (%)")
    tenure_years: int = Field(..., gt=0, description="Loan tenure in years")
    property_tax_rate: float = Field(default=1.0, ge=0, description="Annual property tax (%)")
    insurance_rate: float = Field(default=0.5, ge=0, description="Annual insurance (%)")


class InvestmentReturnInput(BaseModel):
    principal: float = Field(..., gt=0, description="Initial investment")
    rate: float = Field(..., ge=0, le=100, description="Expected annual return (%)")
    years: int = Field(..., gt=0, description="Investment period in years")


class CalculatorResult(BaseModel):
    result: dict
    summary: str


# Chat Schemas
class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []
    session_id: str
