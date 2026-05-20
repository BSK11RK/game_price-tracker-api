from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime

from app.db import Base


# gamesテーブル
class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    
    
# price_historyテーブル
class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now)