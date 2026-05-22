from app.db import SessionLocal
from app.models import Game, PriceHistory, WatchGame
from app.services.scraper_service import get_game_title


# ゲーム保存
def save_game_data(title, price):
    session = SessionLocal()
    
    # 既存確認
    existing_game = session.query(Game).filter(Game.title == title).first()
    
    # 新規
    if existing_game is None:
        new_game = Game(title=title, price=price)
        
        session.add(new_game)
        session.commit()
        session.refresh(new_game)
        
        print()
        print("新規ゲーム保存")
        print(title)
        
        # 履歴追加
        history = PriceHistory(game_id=new_game.id, price=price)
        
        session.add(history)
        session.commit()
        
    # 価格変更
    else:
        if existing_game.price != price:
            old_price = existing_game.price
            
            existing_game.price = price
            
            session.commit()
            
            print()
            print("価格更新")
            print(title)
            print(f"{old_price} → {price}")
            
            # 履歴追加]
            history = PriceHistory(game_id=existing_game.id, price=price)
            
            session.add(history)
            session.commit()
            
        else:
            print()
            print("価格変更なし")
            print(title)
            
    session.close()
    
    
# WatchGame一覧
def get_watch_games():
    session = SessionLocal()
    
    games = session.query(WatchGame).all()
    
    session.close()
    
    return games


# WatchGame追加
def create_watch_game(app_id):
    session = SessionLocal()
    
    existing = session.query(WatchGame).filter(WatchGame.app_id == app_id).first()
    
    if existing:
        session.close()
        
        return None
    
    # タイトル取得
    title = get_game_title(app_id)
    
    game = WatchGame(app_id=app_id, title=title)
    
    session.add(game)
    session.commit()
    session.refresh(game)
    session.close()
    
    return game


# WatchGame削除
def delete_watch_game(game_id):
    session = SessionLocal()
    
    game = session.query(WatchGame).filter(WatchGame.id == game_id).first()
    
    if game is None:
        session.close()
        
        return False
    
    session.delete(game)
    session.commit()
    session.close()
    
    return True