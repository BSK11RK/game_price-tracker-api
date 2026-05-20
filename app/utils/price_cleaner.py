# 価格文字列を数値化
def clean_price(price_text: str):
    cleaned_price = (
        price_text
        .replace("$", "")
        .replace("¥", "")
        .replace(",", "")
        .strip()
    )
    
    return int(float(cleaned_price))