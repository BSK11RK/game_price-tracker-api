from fastapi import FastAPI

from app.api.games import router as games_router
from app.api.history import router as history_router


# FastAPI
app = FastAPI(

    title="Steam Price Tracker API",

    description="Steamゲーム価格監視API",

    version="2.0.0"
)


# Router登録
app.include_router(games_router)

app.include_router(history_router)