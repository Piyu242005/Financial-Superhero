from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import ChatMessage, ChatResponse
from app.services.rag import rag_service
from app.services.auth import get_current_user
from app.models.user import User, ChatHistory

router = APIRouter(prefix="/chat", tags=["AI Chat"])


@router.post("/ask", response_model=ChatResponse)
async def ask_question(
    message: ChatMessage,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ask a financial question to the AI assistant"""
    result = await rag_service.get_answer(message.message, message.session_id)
    
    # Save to history if user is logged in
    if current_user:
        chat_history = ChatHistory(
            user_id=current_user.id,
            session_id=result["session_id"],
            question=message.message,
            answer=result["answer"]
        )
        db.add(chat_history)
        await db.commit()
    
    return ChatResponse(**result)


@router.get("/history")
async def get_chat_history(
    session_id: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get chat history for current user"""
    if not current_user:
        return {"history": []}
    
    from sqlalchemy import select
    
    query = select(ChatHistory).where(ChatHistory.user_id == current_user.id)
    if session_id:
        query = query.where(ChatHistory.session_id == session_id)
    query = query.order_by(ChatHistory.created_at.desc()).limit(50)
    
    result = await db.execute(query)
    history = result.scalars().all()
    
    return {
        "history": [
            {
                "id": h.id,
                "question": h.question,
                "answer": h.answer,
                "session_id": h.session_id,
                "created_at": h.created_at.isoformat()
            }
            for h in history
        ]
    }
