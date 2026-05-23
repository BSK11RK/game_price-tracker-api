import requests


# SteamDBスクレイピング
def scrape_steam_game(app_id: int):
    url = (
        "https://store.steampowered.com/api/appdetails"
        f"?appids={app_id}&cc=jp"
    )
    
    print()
    print("=================================")
    print(f"Steam APIアクセス: {app_id}")
    print("=================================")
    
    res = requests.get(url)
    
    # レスポンス確認
    if res.status_code != 200:
        raise Exception(f"API取得失敗: {res.status_code}")
    
    data = res.json()
    
    # データ存在確認
    if not data[str(app_id)]["success"]:
        raise Exception("ゲームデータ取得失敗")

    game_data = data[str(app_id)]["data"]
    
    # タイトル取得
    title = game_data["name"]
    
    print()
    print("ゲームタイトル:")
    print(title)
    
    # 価格取得
    price_data =game_data.get("price_overview")
    
    # 無料ゲーム対策
    if price_data is None:
        price = 0
        
    else:
        # final は最終価格（100倍）
        price = int(price_data["final"] / 100)
        
    print()
    print("価格:")
    print(price)
    
    return {
        "app_id": app_id,
        "title": title,
        "price": price
    }