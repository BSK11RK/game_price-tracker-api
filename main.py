from apscheduler.schedulers.blocking import BlockingScheduler

from app.services.scraper_service import scrape_steam_game
from app.services.game_service import save_game_data


# 監視ゲーム一覧
GAME_IDS = [
    1245620,  # ELDEN RING
    1091500,  # Cyberpunk 2077
    1623730   # Palworld
]


# スクレイピング実行
def run_scraping():
    print()
    print("=================================")
    print("複数ゲーム監視開始")
    print("=================================")
    
    # 全ゲーム巡回
    for app_id in GAME_IDS:
        try:
            game_data = scrape_steam_game(app_id)
            
            save_game_data(
                title=game_data["title"],
                price=game_data["price"]
            )
            
        except Exception as e:
            
            print()
            print("エラー発生")
    
            print(e)
            
    print()
    print("監視終了")
    
    
# Scheduler
scheduler = BlockingScheduler()


# 定期実行設定
scheduler.add_job(run_scraping, "interval", minutes=1)


# 開始
print()
print("=================================")
print("Steam価格監視 開始")
print("1分ごとに監視します")
print("=================================")


# 初回即実行
run_scraping()


# 定期実行開始
scheduler.start()