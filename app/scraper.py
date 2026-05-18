from playwright.sync_api import sync_playwright
from app.db import SessionLocal, engine
from app.models import Base, Game


# テーブル作成
Base.metadata.create_all(bind=engine)


# SteamDB URL
URL = "https://steamdb.info/app/1245620/"


# スクレイピング関数
def scrape_steam_game():
    print("SteamDBへアクセス中...")
    
    with sync_playwright() as p:
        # ブラウザ起動
        browser = p.chromium.launch(headless=False, slow_mo=1000) 
        
        # Context作成
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/136.0.0.0 "
                "Safari/537.36"
            ),
            locale="ja-JP"
        ) 
    
        # ページ作成
        page = browser.new_page()
        
        # SteamDBアクセス
        page.goto(URL, wait_until="domcontentloaded")
        
        # Cloudflare待機
        print()
        print("Cloudflare確認を待っています...")
        print("ブラウザ側で秒数待ってください")
        
        # 読み込み待機
        page.wait_for_timeout(5000)
        
        # タイトル取得
        title = page.title()
        
        print()
        print("ページタイトル:")
        print(title)
        
        # Cloudflare判定
        if "Checking your browser" in title:
            print()
            print("Cloudflare突破失敗")
            
            browser.close()
            return
        
        # ゲームタイトル取得
        game_title = page.locator("h1").first.text_content()
        
        print()
        print("ゲームタイトル:")
        print(game_title)
        
        # 現在価格取得
        price_element = page.locator(".table-prices td").nth(2)
        
        price_text = price_element.text_content()
        
        print()
        print("価格:")
        print(price_text)
        
        # 数値変換
        cleaned_price = (
            price_text
            .replace("$", "")
            .replace("¥", "")
            .replace(",", "")
            .strip()
        )
        
        price = float(cleaned_price)
        
        # DBセッション
        session = SessionLocal()
        
        # 既存ゲーム確認
        existing_game = session.query(Game).filter(Game.title == game_title).first()
        
        # 新規ゲーム
        if existing_game is None:
            print()
            print("新規ゲーム -> INSERT")
            
            new_game = Game(title=game_title, price=price)
        
            session.add(new_game)
        
        # 既存ゲーム
        else:
            # 価格変化チェック
            if existing_game.price != price:
                print()
                print("価格変動あり -> UPDATE")
                
                print(f"{existing_game.price} -> {price}")
                
                existing_game.price = price
                
            else:
                print()
                print("価格変動なし")
        
        # 保存
        session.commit()
        
        session.close()
        
        print()
        print("SQLite保存完了")
        
        # ブラウザ終了
        browser.close()