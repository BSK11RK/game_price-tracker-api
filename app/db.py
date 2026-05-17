import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# dataフォルダ自動作成
os.makedirs("data", exist_ok=True)


# SQLite DBパス
DATABASE_URL = "sqlite:///data/steam_prices.db"


# Engine作成
engine = create_engine(DATABASE_URL, echo=False)


# Session作成
SessionLocal = sessionmaker(bind=engine)


# Base作成
Base = declarative_base()