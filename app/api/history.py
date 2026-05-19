from fastapi import APIRouter
from app.db import SessionLocal
from app.models import PriceHistory


# Router
router = APIRouter(prefix="/history", tags=["History"])


# 価格履歴一覧
@router.get("")
def get_price_history():
    session = SessionLocal()
    
    histories = session.query(PriceHistory).all()
    
    result = []
    
    for history in histories:
        result.append({
            "id": history.id,
            "game_id": history.game_id,
            "price": history.price,
            "created_at": history.created_at
        })
        
        session.close()
        
        return result