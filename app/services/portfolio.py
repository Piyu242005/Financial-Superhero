import random
from datetime import date
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.portfolio import PortfolioHolding, StockWatchlist
from app.schemas import (
    PortfolioHoldingCreate, 
    PortfolioHoldingUpdate, 
    PortfolioHoldingResponse,
    WatchlistItemCreate,
    WatchlistItemResponse,
    PortfolioSummary
)


# Mock stock prices - In production, integrate with real stock API (Alpha Vantage, Yahoo Finance, etc.)
MOCK_STOCK_DATA = {
    "RELIANCE": {"price": 2875.50, "name": "Reliance Industries Ltd"},
    "TCS": {"price": 4125.80, "name": "Tata Consultancy Services Ltd"},
    "INFY": {"price": 1685.25, "name": "Infosys Ltd"},
    "HDFCBANK": {"price": 1720.40, "name": "HDFC Bank Ltd"},
    "ICICIBANK": {"price": 1245.60, "name": "ICICI Bank Ltd"},
    "HINDUNILVR": {"price": 2450.30, "name": "Hindustan Unilever Ltd"},
    "ITC": {"price": 465.80, "name": "ITC Ltd"},
    "SBIN": {"price": 785.25, "name": "State Bank of India"},
    "BHARTIARTL": {"price": 1580.90, "name": "Bharti Airtel Ltd"},
    "KOTAKBANK": {"price": 1890.45, "name": "Kotak Mahindra Bank Ltd"},
    "LT": {"price": 3650.20, "name": "Larsen & Toubro Ltd"},
    "ASIANPAINT": {"price": 2890.75, "name": "Asian Paints Ltd"},
    "MARUTI": {"price": 12450.60, "name": "Maruti Suzuki India Ltd"},
    "WIPRO": {"price": 485.30, "name": "Wipro Ltd"},
    "TATAMOTORS": {"price": 985.40, "name": "Tata Motors Ltd"},
    "TATASTEEL": {"price": 145.85, "name": "Tata Steel Ltd"},
    "ADANIENT": {"price": 2850.60, "name": "Adani Enterprises Ltd"},
    "BAJFINANCE": {"price": 7250.80, "name": "Bajaj Finance Ltd"},
    "HCLTECH": {"price": 1685.45, "name": "HCL Technologies Ltd"},
    "SUNPHARMA": {"price": 1725.30, "name": "Sun Pharmaceutical Industries Ltd"},
}


def get_current_price(symbol: str) -> float:
    """Get current stock price with slight random variation to simulate real-time updates"""
    if symbol.upper() in MOCK_STOCK_DATA:
        base_price = MOCK_STOCK_DATA[symbol.upper()]["price"]
        # Add small random variation (±2%) to simulate price movement
        variation = random.uniform(-0.02, 0.02)
        return round(base_price * (1 + variation), 2)
    # For unknown symbols, generate a random price
    return round(random.uniform(100, 5000), 2)


def get_stock_suggestions() -> list[dict]:
    """Get list of popular stocks for autocomplete"""
    return [
        {"symbol": symbol, "name": data["name"], "price": data["price"]}
        for symbol, data in MOCK_STOCK_DATA.items()
    ]


async def create_holding(
    db: AsyncSession, 
    user_id: int, 
    holding_data: PortfolioHoldingCreate
) -> PortfolioHolding:
    """Create a new portfolio holding"""
    holding = PortfolioHolding(
        user_id=user_id,
        symbol=holding_data.symbol.upper(),
        company_name=holding_data.company_name,
        quantity=holding_data.quantity,
        buy_price=holding_data.buy_price,
        buy_date=date.fromisoformat(holding_data.buy_date),
        notes=holding_data.notes
    )
    db.add(holding)
    await db.commit()
    await db.refresh(holding)
    return holding


async def get_user_holdings(db: AsyncSession, user_id: int) -> list[PortfolioHoldingResponse]:
    """Get all holdings for a user with current prices and calculations"""
    result = await db.execute(
        select(PortfolioHolding).where(PortfolioHolding.user_id == user_id)
    )
    holdings = result.scalars().all()
    
    response = []
    for h in holdings:
        current_price = get_current_price(h.symbol)
        current_value = current_price * h.quantity
        invested_value = h.buy_price * h.quantity
        gain_loss = current_value - invested_value
        gain_loss_percent = (gain_loss / invested_value * 100) if invested_value > 0 else 0
        
        response.append(PortfolioHoldingResponse(
            id=h.id,
            symbol=h.symbol,
            company_name=h.company_name,
            quantity=h.quantity,
            buy_price=h.buy_price,
            buy_date=h.buy_date.isoformat(),
            notes=h.notes,
            current_price=round(current_price, 2),
            current_value=round(current_value, 2),
            invested_value=round(invested_value, 2),
            gain_loss=round(gain_loss, 2),
            gain_loss_percent=round(gain_loss_percent, 2)
        ))
    
    return response


async def get_holding_by_id(db: AsyncSession, holding_id: int, user_id: int) -> PortfolioHolding | None:
    """Get a specific holding by ID"""
    result = await db.execute(
        select(PortfolioHolding).where(
            PortfolioHolding.id == holding_id,
            PortfolioHolding.user_id == user_id
        )
    )
    return result.scalar_one_or_none()


async def update_holding(
    db: AsyncSession, 
    holding: PortfolioHolding, 
    update_data: PortfolioHoldingUpdate
) -> PortfolioHolding:
    """Update an existing holding"""
    update_dict = update_data.model_dump(exclude_unset=True)
    
    if 'buy_date' in update_dict and update_dict['buy_date']:
        update_dict['buy_date'] = date.fromisoformat(update_dict['buy_date'])
    if 'symbol' in update_dict and update_dict['symbol']:
        update_dict['symbol'] = update_dict['symbol'].upper()
    
    for key, value in update_dict.items():
        if value is not None:
            setattr(holding, key, value)
    
    await db.commit()
    await db.refresh(holding)
    return holding


async def delete_holding(db: AsyncSession, holding_id: int, user_id: int) -> bool:
    """Delete a holding"""
    result = await db.execute(
        delete(PortfolioHolding).where(
            PortfolioHolding.id == holding_id,
            PortfolioHolding.user_id == user_id
        )
    )
    await db.commit()
    return result.rowcount > 0


async def get_portfolio_summary(db: AsyncSession, user_id: int) -> PortfolioSummary:
    """Calculate portfolio summary statistics"""
    holdings = await get_user_holdings(db, user_id)
    
    if not holdings:
        return PortfolioSummary(
            total_invested=0,
            current_value=0,
            total_gain_loss=0,
            total_gain_loss_percent=0,
            holdings_count=0
        )
    
    total_invested = sum(h.invested_value for h in holdings)
    current_value = sum(h.current_value for h in holdings)
    total_gain_loss = current_value - total_invested
    total_gain_loss_percent = (total_gain_loss / total_invested * 100) if total_invested > 0 else 0
    
    # Find top and worst performers
    sorted_by_gain = sorted(holdings, key=lambda x: x.gain_loss_percent, reverse=True)
    top_performer = sorted_by_gain[0].symbol if sorted_by_gain else None
    worst_performer = sorted_by_gain[-1].symbol if sorted_by_gain else None
    
    return PortfolioSummary(
        total_invested=round(total_invested, 2),
        current_value=round(current_value, 2),
        total_gain_loss=round(total_gain_loss, 2),
        total_gain_loss_percent=round(total_gain_loss_percent, 2),
        holdings_count=len(holdings),
        top_performer=top_performer,
        worst_performer=worst_performer
    )


# Watchlist operations
async def add_to_watchlist(
    db: AsyncSession, 
    user_id: int, 
    item_data: WatchlistItemCreate
) -> StockWatchlist:
    """Add a stock to user's watchlist"""
    item = StockWatchlist(
        user_id=user_id,
        symbol=item_data.symbol.upper(),
        company_name=item_data.company_name,
        target_price=item_data.target_price,
        notes=item_data.notes
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def get_user_watchlist(db: AsyncSession, user_id: int) -> list[WatchlistItemResponse]:
    """Get user's watchlist with current prices"""
    result = await db.execute(
        select(StockWatchlist).where(StockWatchlist.user_id == user_id)
    )
    items = result.scalars().all()
    
    return [
        WatchlistItemResponse(
            id=item.id,
            symbol=item.symbol,
            company_name=item.company_name,
            target_price=item.target_price,
            current_price=get_current_price(item.symbol),
            notes=item.notes
        )
        for item in items
    ]


async def remove_from_watchlist(db: AsyncSession, item_id: int, user_id: int) -> bool:
    """Remove a stock from watchlist"""
    result = await db.execute(
        delete(StockWatchlist).where(
            StockWatchlist.id == item_id,
            StockWatchlist.user_id == user_id
        )
    )
    await db.commit()
    return result.rowcount > 0
