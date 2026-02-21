import os
import yfinance as yf
from fredapi import Fred
import requests

def run_agent():
    print("Fetching data...")
    # 1. FRED Data
    fred = Fred(api_key=os.getenv('FRED_API_KEY'))
    hy_spread = fred.get_series_latest_release('BAMLH0A0HYM2').iloc[-1]
    
    # 2. Yahoo Finance Data
    gold = yf.Ticker('GC=F').history(period='1d')['Close'].iloc[-1]
    vix = yf.Ticker('^VIX').history(period='1d')['Close'].iloc[-1]

    # 3. Format Message
    report = (f"📈 MARKET REPORT\n"
              f"Spread: {hy_spread}%\n"
              f"Gold: ${gold:.2f}\n"
              f"VIX: {vix:.2f}")
    
    # 4. Telegram Send
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    response = requests.post(url, json={"chat_id": chat_id, "text": report})
    print(f"Status: {response.status_code}")

if __name__ == "__main__":
    run_agent()
