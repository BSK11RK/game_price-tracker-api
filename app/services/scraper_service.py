from playwright.sync_api import sync_playwright
from app.utils.price_cleaner import clean_price


# SteamDBスクレイピング
def scrape_steam_game():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        
        page = browser.new_page()
        
        print("SteamDBへアクセス中...")
        
        page.goto("https://steamdb.info/app/1245620/", wait_until="domcontentloaded")
        
        # Cloudflare待機
        page.wait_for_timeout(5000)
        
        print()
        print("ページタイトル:")
        print(page.title())
        
        # タイトル取得
        title_element = page.locator("h1")
        
        title = title_element.text_content()
        
        print()
        print("ゲームタイトル:")
        print(title)
        
        # 価格取得
        price_element = page.locator(".table-prices td").nth(2)
        
        price_text = price_element.text_content()
        
        print()
        print("価格文字列")
        print(price_text)
        
        # 数値変換
        price = clean_price(price_text)
        
        print()
        print("価格:")
        print(price)
        
        browser.close()
        
        return {
            "title": title,
            "price": price
        }