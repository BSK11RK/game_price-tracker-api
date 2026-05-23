from fastapi import APIRouter

from app.db import SessionLocal
from app.models import PriceHistory, WatchGame


# Router
router = APIRouter(prefix="/history", tags=["価格履歴"])


# 全履歴取得
@router.get("/")
def get_history():
    session = SessionLocal()
    
    histories = session.query(PriceHistory).all()
    
    result = []
    
    for history in histories:
        game = session.query(WatchGame).filter(WatchGame.id == history.watch_game_id).first()
        
        result.append({
            "id": history.id,
            "game_title": game.title,
            "price": history.price,
            "created_at": history.created_at
        })
        
    session.close()
    
    return result