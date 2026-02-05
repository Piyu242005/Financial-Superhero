from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Date
from sqlalchemy.sql import func
from app.database import Base


class PortfolioHolding(Base):
    """User's investment holdings"""
    __tablename__ = "portfolio_holdings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    symbol = Column(String(20), nullable=False)  # Stock symbol (e.g., RELIANCE, TCS)
    company_name = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)
    buy_price = Column(Float, nullable=False)  # Price per share at purchase
    buy_date = Column(Date, nullable=False)
    notes = Column(String(500))  # Optional notes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class StockWatchlist(Base):
    """User's watchlist of stocks to monitor"""
    __tablename__ = "stock_watchlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    symbol = Column(String(20), nullable=False)
    company_name = Column(String(255), nullable=False)
    target_price = Column(Float)  # Price alert target
    notes = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
