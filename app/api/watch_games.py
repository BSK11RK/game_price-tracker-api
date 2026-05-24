from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.game_service import get_watch_games, create_watch_game, delete_watch_game, update_watch_game_enabled


router = APIRouter(prefix="/watch-games", tags=["監視ゲーム"])


# リクエスト
class WatchGameCreate(BaseModel):
    app_id: int
    
class WatchGameUpdate(BaseModel):
    enabled: bool
    
    
# 一覧取得
@router.get("/")
def get_all_watch_games():
    return get_watch_games()


# 追加
@router.post("/")
def create_game(data: WatchGameCreate):
    game = create_watch_game(data.app_id)
    
    if game is None:
        raise HTTPException(status_code=400, detail="既に登録されています")
    
    return game


# ON/OFF切替
@router.patch("/{game_id}")
def update_game(game_id: int, data: WatchGameUpdate):
    game = update_watch_game_enabled(game_id, data.enabled)
    
    if game is None:
        raise HTTPException(status_code=404, detail="ゲームが見つかりません")
    
    return game


# 削除
@router.delete("/{game_id}")
def delete_game(game_id: int):
    success = delete_watch_game(game_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="ゲームが見つかりません")
    
    return {"message": "削除しました"}