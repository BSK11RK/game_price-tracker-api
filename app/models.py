from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func

from app.db import Base


# 監視対象ゲーム
class WatchGame(Base):
    __tablename__ = "watch_games"
    
    id = Column(Integer, primary_key=True, index=True)
    app_id = Column(Integer, unique=True, nullable=False)
    title = Column(String, nullable=False)
    current_price = Column(Integer, nullable=False)
    lowest_price = Column(Integer, nullable=False)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    
# 価格履歴
class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True, index=True)
    watch_game_id = Column(Integer, ForeignKey("watch_games.id"))
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())