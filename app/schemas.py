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


# Portfolio Schemas
class PortfolioHoldingCreate(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20, description="Stock symbol")
    company_name: str = Field(..., min_length=1, max_length=255, description="Company name")
    quantity: float = Field(..., gt=0, description="Number of shares")
    buy_price: float = Field(..., gt=0, description="Purchase price per share")
    buy_date: str = Field(..., description="Purchase date (YYYY-MM-DD)")
    notes: Optional[str] = Field(None, max_length=500)


class PortfolioHoldingUpdate(BaseModel):
    symbol: Optional[str] = Field(None, max_length=20)
    company_name: Optional[str] = Field(None, max_length=255)
    quantity: Optional[float] = Field(None, gt=0)
    buy_price: Optional[float] = Field(None, gt=0)
    buy_date: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=500)


class PortfolioHoldingResponse(BaseModel):
    id: int
    symbol: str
    company_name: str
    quantity: float
    buy_price: float
    buy_date: str
    notes: Optional[str]
    current_price: float = 0.0
    current_value: float = 0.0
    invested_value: float = 0.0
    gain_loss: float = 0.0
    gain_loss_percent: float = 0.0

    class Config:
        from_attributes = True


class WatchlistItemCreate(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20)
    company_name: str = Field(..., min_length=1, max_length=255)
    target_price: Optional[float] = Field(None, gt=0)
    notes: Optional[str] = Field(None, max_length=500)


class WatchlistItemResponse(BaseModel):
    id: int
    symbol: str
    company_name: str
    target_price: Optional[float]
    current_price: float = 0.0
    notes: Optional[str]

    class Config:
        from_attributes = True


class PortfolioSummary(BaseModel):
    total_invested: float
    current_value: float
    total_gain_loss: float
    total_gain_loss_percent: float
    holdings_count: int
    top_performer: Optional[str] = None
    worst_performer: Optional[str] = None
