from fastapi import FastAPI, HTTPException, Query
from app.db import SessionLocal
from app.models import Game, PriceHistory


# FastAPI作成
app = FastAPI(
    title="Steam Price Tracker API",
    description="Steamゲーム価格監視API",
    version="1.0.0"
)


# ゲーム一覧取得 + 検索
@app.get("/games")
def get_games(title: str = Query(None)):
    session = SessionLocal()
    
    query = session.query(Game)
    
    # 検索条件がある場合
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
@app.get("/games/{game_id}")
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


# 価格履歴取得
@app.get("/history")
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