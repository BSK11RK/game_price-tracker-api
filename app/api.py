from fastapi import FastAPI
from app.db import SessionLocal
from app.models import Game, PriceHistory


# FastAPI作成
app = FastAPI(
    title="Steam Price Tracker API",
    description="Steamゲーム価格監視API",
    version="1.0.0"
)


# ゲーム一覧取得
@app.get("/games")
def get_games():
    session = SessionLocal()
    games = session.query(Game).all()
    
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