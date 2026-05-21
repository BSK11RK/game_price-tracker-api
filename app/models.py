from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from datetime import datetime

from app.db import Base


# ゲームテーブル
class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    
    
# 価格履歴テーブル
class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    
    
# 監視対象ゲーム
class WatchGame(Base):
    __tablename__ = "watch_games"
    
    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(Integer, unique=True, nullable=False)
    enabled = Column(Boolean, default=True)