import os
import yfinance as yf
from fredapi import Fred
import requests

def run_agent():
    print("Checking risk levels...")
    # 1. Fetch Data
    fred = Fred(api_key=os.getenv('FRED_API_KEY'))
    hy_spread = fred.get_series_latest_release('BAMLH0A0HYM2').iloc[-1]
    
    gold = yf.Ticker('GC=F').history(period='1d')['Close'].iloc[-1]
    vix = yf.Ticker('^VIX').history(period='1d')['Close'].iloc[-1]

    # 2. Determine Risk Status
    status_icon = "🟢"  # Default: Low Risk
    alert_msg = "All clear."

    if vix > 35 or hy_spread > 7:
        status_icon = "🚨🚨🚨"
        alert_msg = "SYSTEMIC RISK ALERT: CRITICAL"
    elif vix > 25 or hy_spread > 5:
        status_icon = "⚠️"
        alert_msg = "ELEVATED RISK: EXTREME CAUTION"

    # 3. Format Message
    report = (
        f"{status_icon} {alert_msg}\n\n"
        f"📊 DATA SUMMARY:\n"
        f"• VIX (Fear): {vix:.2f}\n"
        f"• HY Spread: {hy_spread}%\n"
        f"• Gold: ${gold:.2f}"
    )
    
    # 4. Telegram Send
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    requests.post(url, json={"chat_id": chat_id, "text": report})
    print(f"Sent status: {alert_msg}")

if __name__ == "__main__":
    run_agent()
