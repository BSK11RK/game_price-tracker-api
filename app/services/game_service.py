from app.db import SessionLocal
from app.models import Game, PriceHistory


# DB保存
def save_game_data(title: str, price: int):
    session = SessionLocal()
    
    # 既存確認
    existing_game = session.query(Game).filter(Game.title == title).first()
    
    # 新規
    if existing_game is None:
        new_game = Game(title=title, price=price)
        
        session.add(new_game)
        
        session.commit()
        session.refresh(new_game)
        
        # 履歴追加
        history = PriceHistory(game_id=new_game.id, price=price)
        
        session.add(history)
        session.commit()
        
        print()
        print("新規保存しました")
        
    # 価格変更
    else:
        if existing_game.price != price:
            old_price = existing_game.price
            
            existing_game.price = price
            
            session.commit()
            
            # 履歴追加]
            history = PriceHistory(game_id=existing_game.id, price=price)
            
            session.add(history)
            session.commit()
            
            print()
            print("価格更新しました")
            
            print(f"{old_price} → {price}")
            
        else:
            print()
            print("価格変化なし")
            
    session.close()