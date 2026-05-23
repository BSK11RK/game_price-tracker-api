from fastapi import APIRouter
from app.services.game_service import get_watch_games


# Router
router = APIRouter(prefix="/games", tags=["ゲーム"])


# 一覧取得
@router.get("/")
def get_games():
    games = get_watch_games()
    
    return games