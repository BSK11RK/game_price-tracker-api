import threading, uvicorn
from fastapi import FastAPI
from apscheduler.schedulers.blocking import BlockingScheduler

from app.db import Base, engine, SessionLocal
from app.models import PriceHistory, WatchGame
from app.services.scraper_service import scrape_steam_game
from app.services.game_service import save_game_data
from app.api.games import router as games_router
from app.api.history import router as history_router
from app.api.watch_games import router as watch_games_router


# FastAPI
app = FastAPI(title="Steam Price Tracker API")

app.include_router(games_router)
app.include_router(history_router)
app.include_router(watch_games_router)


# テーブル作成
Base.metadata.create_all(bind=engine)


# 初期監視ゲーム登録
def seed_watch_games():
    session = SessionLocal()
    
    existing = session.query(WatchGame).count()
    
    if existing == 0:
        default_games = [
            1245620,  # ELDEN RING
            1091500,  # Cyberpunk 2077
            1623730   # Palworld
        ]
        
        print()
        print("初期監視ゲーム登録開始")
        
        for app_id in default_games:
            try:
                game_data = scrape_steam_game(app_id)
                
                game = WatchGame(
                    app_id=app_id, 
                    title=game_data["title"],
                    current_price=game_data["price"],
                    lowest_price=game_data["price"],
                    enabled=True
                )
                
                session.add(game)
                session.commit()
                
                # 初期履歴保存
                history = PriceHistory(watch_game_id=game.id, price=game_data["price"])
                
                session.add(history)
                session.commit()
                
                print()
                print("登録完了")
                print(game_data["title"])

            except Exception as e:
                print()
                print("初期登録エラー")
                
                print(e)
                
    session.close()
        

# スクレイピング実行
def run_scraping():
    session = SessionLocal()
    
    watch_games = session.query(WatchGame).filter(WatchGame.enabled == True).all()
    
    print()
    print("=================================")
    print("監視開始")
    print("=================================")
    
    # 全ゲーム巡回
    for watch_game in watch_games:
        try:
            game_data = scrape_steam_game(watch_game.app_id)
            
            save_game_data(
                app_id=game_data["app_id"],
                title=game_data["title"],
                price=game_data["price"]
            )
            
        except Exception as e:
            
            print()
            print("監視エラー")
    
            print(e)
        
    session.close()
            
    print()
    print("監視終了")
    
    
# Scheduler
scheduler = BlockingScheduler()


# 定期実行設定
scheduler.add_job(run_scraping, "interval", minutes=30)


# FastAPI起動
def start_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)


# 開始
print()
print("=================================")
print("Steam価格監視BOT 起動")
print("=================================")


# 初期データ
seed_watch_games()


# 初回即実行
run_scraping()


# API起動
api_thread = threading.Thread(target=start_api)

api_thread.start()


# 定期実行開始
scheduler.start()