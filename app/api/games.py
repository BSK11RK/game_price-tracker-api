from fastapi import APIRouter, HTTPException, Query

from app.db import SessionLocal
from app.models import Game, PriceHistory


# Router
router = APIRouter(prefix="/games", tags=["ゲーム"])


# ゲーム一覧 + 検索
@router.get("")
def get_games(title: str = Query(None)):
    session = SessionLocal()
    
    query = session.query(Game)
    
    # 検索
    if title:
        query = query.filter(Game.title.like(f"%{title}%"))
        
    games = query.all()
    
    result = []
    
    for game in games:
        result.append({
            "id": game.id,
            "title": game.title,
            "price": game.price,
            "created_at": game.created_at
        })
        
    session.close()
    
    return result


# 1件取得
@router.get("/{game_id}")
def get_game(game_id: int):
    session = SessionLocal()
    
    game = session.query(Game).filter(Game.id == game_id).first()
    
    session.close()
    
    if game is None:
        raise HTTPException(status_code=404, detail="ゲームが見つかりません")
    
    return {
        "id": game.id,
        "title": game.title,
        "price": game.price,
        "created_at": game.created_at
    }
    
    
# ゲーム別価格履歴
@router.get("/{game_id}/history")
def get_game_histiry(game_id: int):
    session = SessionLocal()
    
    # ゲーム存在確認
    game = session.query(Game).filter(Game.id == game_id).first()
    
    if game is None:
        session.close()
        
        raise HTTPException(status_code=404, detail="ゲームが見つかりません")
    
    # 履歴取得
    histories = session.query(PriceHistory).filter(PriceHistory.game_id == game_id).all()
    
    result = []
    
    for history in histories:
        result.append({
            "id": history.id,
            "price": history.price,
            "created_at": history.created_at
        })
        
    session.close()
    
    return {
        "game": {
            "id": game.id,
            "title": game.title
        },
        "history": result
    }