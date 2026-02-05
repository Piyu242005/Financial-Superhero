from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.auth import get_current_user_required
from app.services import portfolio as portfolio_service
from app.models.user import User
from app.schemas import (
    PortfolioHoldingCreate,
    PortfolioHoldingUpdate,
    PortfolioHoldingResponse,
    WatchlistItemCreate,
    WatchlistItemResponse,
    PortfolioSummary
)

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/", response_model=list[PortfolioHoldingResponse])
async def get_portfolio(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """Get all portfolio holdings for the current user"""
    return await portfolio_service.get_user_holdings(db, current_user.id)


@router.post("/", response_model=PortfolioHoldingResponse, status_code=status.HTTP_201_CREATED)
async def add_holding(
    holding: PortfolioHoldingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """Add a new holding to portfolio"""
    new_holding = await portfolio_service.create_holding(db, current_user.id, holding)
    
    # Get the response with current price calculations
    current_price = portfolio_service.get_current_price(new_holding.symbol)
    current_value = current_price * new_holding.quantity
    invested_value = new_holding.buy_price * new_holding.quantity
    gain_loss = current_value - invested_value
    gain_loss_percent = (gain_loss / invested_value * 100) if invested_value > 0 else 0
    
    return PortfolioHoldingResponse(
        id=new_holding.id,
        symbol=new_holding.symbol,
        company_name=new_holding.company_name,
        quantity=new_holding.quantity,
        buy_price=new_holding.buy_price,
        buy_date=new_holding.buy_date.isoformat(),
        notes=new_holding.notes,
        current_price=round(current_price, 2),
        current_value=round(current_value, 2),
        invested_value=round(invested_value, 2),
        gain_loss=round(gain_loss, 2),
        gain_loss_percent=round(gain_loss_percent, 2)
    )


@router.put("/{holding_id}", response_model=PortfolioHoldingResponse)
async def update_holding(
    holding_id: int,
    update_data: PortfolioHoldingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """Update an existing holding"""
    holding = await portfolio_service.get_holding_by_id(db, holding_id, current_user.id)
    if not holding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Holding not found"
        )
    
    updated = await portfolio_service.update_holding(db, holding, update_data)
    
    current_price = portfolio_service.get_current_price(updated.symbol)
    current_value = current_price * updated.quantity
    invested_value = updated.buy_price * updated.quantity
    gain_loss = current_value - invested_value
    gain_loss_percent = (gain_loss / invested_value * 100) if invested_value > 0 else 0
    
    return PortfolioHoldingResponse(
        id=updated.id,
        symbol=updated.symbol,
        company_name=updated.company_name,
        quantity=updated.quantity,
        buy_price=updated.buy_price,
        buy_date=updated.buy_date.isoformat(),
        notes=updated.notes,
        current_price=round(current_price, 2),
        current_value=round(current_value, 2),
        invested_value=round(invested_value, 2),
        gain_loss=round(gain_loss, 2),
        gain_loss_percent=round(gain_loss_percent, 2)
    )


@router.delete("/{holding_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_holding(
    holding_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """Delete a holding from portfolio"""
    deleted = await portfolio_service.delete_holding(db, holding_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Holding not found"
        )
    return None


@router.get("/summary", response_model=PortfolioSummary)
async def get_portfolio_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """Get portfolio summary with total values and performance"""
    return await portfolio_service.get_portfolio_summary(db, current_user.id)


@router.get("/stocks", response_model=list[dict])
async def get_stock_suggestions():
    """Get list of popular stocks for autocomplete"""
    return portfolio_service.get_stock_suggestions()


# Watchlist endpoints
@router.get("/watchlist", response_model=list[WatchlistItemResponse])
async def get_watchlist(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """Get user's stock watchlist"""
    return await portfolio_service.get_user_watchlist(db, current_user.id)


@router.post("/watchlist", response_model=WatchlistItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_watchlist(
    item: WatchlistItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """Add a stock to watchlist"""
    new_item = await portfolio_service.add_to_watchlist(db, current_user.id, item)
    return WatchlistItemResponse(
        id=new_item.id,
        symbol=new_item.symbol,
        company_name=new_item.company_name,
        target_price=new_item.target_price,
        current_price=portfolio_service.get_current_price(new_item.symbol),
        notes=new_item.notes
    )


@router.delete("/watchlist/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_watchlist(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_required)
):
    """Remove a stock from watchlist"""
    removed = await portfolio_service.remove_from_watchlist(db, item_id, current_user.id)
    if not removed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist item not found"
        )
    return None
