from fastapi import APIRouter, HTTPException, Query
from app.db import SessionLocal
from app.models import Game


# Router
router = APIRouter(prefix="/games", tags=["Games"])


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