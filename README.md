# Steam Price Tracker API

Steamゲームの価格を定期監視する FastAPI ベースの価格監視システムです。

Steam公式APIからゲーム価格を取得し、SQLiteへ保存します。

価格履歴管理や監視ON/OFF機能も実装しています。

---

# 使用技術

- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite
- APScheduler
- Docker
- Steam Store API

---

# 主な機能

## ゲーム監視

- 複数ゲーム監視
- 定期価格取得
- 最安値保存
- 価格履歴保存

## API

- 一覧取得
- 1件取得
- タイトル検索
- 監視ON/OFF
- 削除

## 自動化

- APSchedulerによる定期実行

---

# API一覧

| Method | URL | 内容 |
|---|---|---|
| GET | /watch-games/ | 一覧取得 |
| GET | /watch-games/{id} | 1件取得 |
| GET | /watch-games/search/?keyword=xxx | タイトル検索 |
| POST | /watch-games/ | 監視追加 |
| PATCH | /watch-games/{id} | ON/OFF切替 |
| DELETE | /watch-games/{id} | 削除 |
| GET | /history/ | 価格履歴一覧 |

---

# DB構成

## watch_games

監視対象ゲーム。

- app_id
- title
- current_price
- lowest_price
- enabled

## price_history

価格履歴。

- watch_game_id
- price
- created_at

---

# 工夫した点

- Gameテーブルを廃止し、watch_games中心へ設計変更
- Service層分離
- Schedulerによる自動監視
- 価格変更時のみ履歴保存
- Steam公式APIを利用し安定化

---

# 起動方法

## ローカル

```bash
pip install -r requirements.txt
python main.py
```

---

# Docker起動

```bash
docker compose up
```

---

# Swagger UI

```text
http://localhost:8000/docs
```