from apscheduler.schedulers.blocking import BlockingScheduler

from app.services.scraper_service import scrape_steam_game
from app.services.game_service import save_game_data


# スクレイピング実行
def run_scraping():
    print()
    print("=================================")
    print("スクレイピング開始")
    print("=================================")
    
    game_data = scrape_steam_game()
    
    save_game_data(
        title=game_data["title"],
        price=game_data["price"]
    )
    
    print()
    print("スクレイピング終了")
    
    
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