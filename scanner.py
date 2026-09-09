import os
import requests
import yfinance as yf
import pandas as pd

WEBHOOK_URL = os.environ["MAKE_WEBHOOK_URL"]

symbols = {
    "BTC": "BTC-USD",
    "NIFTY": "^NSEI",
}

signals = []

for name, ticker in symbols.items():
    data = yf.download(ticker, period="6mo", interval="1d", auto_adjust=True, progress=False)

    if data.empty:
        continue

    close = data["Close"].squeeze()

    sma20 = close.rolling(20).mean()
    sma50 = close.rolling(50).mean()

    current = float(close.iloc[-1])
    ma20 = float(sma20.iloc[-1])
    ma50 = float(sma50.iloc[-1])

    # Conservative paper-trading condition:
    # price above both moving averages and 20-day average above 50-day average
    if current > ma20 and ma20 > ma50:
        signals.append({
            "asset": name,
            "price": round(current, 2),
            "signal": "WATCH",
            "reason": "Price above 20-day MA and 20-day MA above 50-day MA"
        })

if signals:
    message = {
        "type": "MARKET_SIGNAL",
        "signals": signals
    }

    response = requests.post(WEBHOOK_URL, json=message, timeout=20)
    response.raise_for_status()

    print("Alert sent:", message)
else:
    print("No qualifying setup today.")
