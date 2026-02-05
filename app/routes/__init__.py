from app.routes.auth import router as auth_router
from app.routes.calculator import router as calculator_router
from app.routes.chat import router as chat_router
from app.routes.pages import router as pages_router
from app.routes.portfolio import router as portfolio_router

__all__ = ["auth_router", "calculator_router", "chat_router", "pages_router", "portfolio_router"]
