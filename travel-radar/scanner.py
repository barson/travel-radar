import os
from datetime import datetime, timedelta
import random
from supabase import create_client, Client
import requests

# 1. 連線到你的雲端 Supabase 資料庫 (從 GitHub 秘密設定中讀取)
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# 模擬的熱門航點與基礎底價
DESTINATIONS = [
    {"code": "OKA", "city": "日本 · 沖繩", "base_flight": 4500, "base_hotel": 5400, "tag": "3星質感商旅 (8.6★)"},
    {"code": "PUS", "city": "韓國 · 釜山", "base_flight": 5200, "base_hotel": 4800, "tag": "超贊房東 Airbnb (4.9★)"},
    {"code": "DAD", "city": "越南 · 峴港", "base_flight": 5500, "base_hotel": 6200, "tag": "4星渡假商旅 (8.9★)"}
]

def run_scanner_and_update():
    print("🚀 開始執行機加酒自動掃描...")
    today = datetime.now()
    
    for item in DESTINATIONS:
        # 模擬即時抓取與計算價格
        flight_price = item["base_flight"] + random.randint(-400, 500)
        hotel_total = item["base_hotel"] + random.randint(-300, 400)
        total_price = flight_price + hotel_total
        avg_price = 12500 # 歷史 100 筆均線基準
        diff_pct = round(((avg_price - total_price) / avg_price) * 100, 1)
        
        future_start = today + timedelta(days=random.randint(10, 45))
        future_end = future_start + timedelta(days=3)
        dates_str = f"{future_start.strftime('%m/%d')} ~ {future_end.strftime('%m/%d')} (4天3夜)"

        # 準備要上傳到 Supabase 雲端資料庫的資料格式
        deal_data = {
            "code": item["code"],
            "city": item["city"],
            "nights": "4天3夜",
            "dates": dates_str,
            "flight": flight_price,
            "hotel": hotel_total,
            "total": total_price,
            "avg_price": avg_price,
            "diff": diff_pct,
            "tag": item["tag"],
            "updated_at": today.strftime("%Y-%m-%d %H:%M:%S")
        }

        # 寫入 Supabase (upsert: 存在就更新，不存在就新增)
        supabase.table("current_deals").upsert(deal_data).execute()
        print(f"✅ 已成功更新雲端資料庫：{item['city']} -> 總價 NT$ {total_price:,}")

if __name__ == "__main__":
    run_scanner_and_update()
