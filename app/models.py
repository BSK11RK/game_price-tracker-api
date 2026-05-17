from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db import Base


# gamesテーブル
class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now)