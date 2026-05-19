from app.services.scraper_service import scrape_steam_game
from app.services.game_service import save_game_data


# 実行
if __name__ == "__main__":
    game_data = scrape_steam_game()
    
    save_game_data(
        title=game_data["title"],
        price=game_data["price"]
    )