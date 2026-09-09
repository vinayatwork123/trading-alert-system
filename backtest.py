import yfinance as yf

STARTING_CAPITAL = 1000.0

symbols = {
    "BTC": "BTC-USD",
    "NIFTY": "^NSEI"
}

for name, ticker in symbols.items():

    data = yf.download(
        ticker,
        period="5y",
        interval="1d",
        auto_adjust=True,
        progress=False
    )

    if data.empty:
        print(f"{name}: No data available")
        continue

    close = data["Close"].squeeze()

    ma20 = close.rolling(20).mean()
    ma50 = close.rolling(50).mean()

    cash = STARTING_CAPITAL
    units = 0.0
    completed_trades = 0

    for i in range(50, len(data)):

        price = float(close.iloc[i])

        bullish = (
            price > float(ma20.iloc[i])
            and float(ma20.iloc[i]) > float(ma50.iloc[i])
        )

        bearish = (
            price < float(ma20.iloc[i])
            or float(ma20.iloc[i]) < float(ma50.iloc[i])
        )

        if units == 0 and bullish:
            units = cash / price
            cash = 0

        elif units > 0 and bearish:
            cash = units * price
            units = 0
            completed_trades += 1

    if units > 0:
        final_value = units * float(close.iloc[-1])
    else:
        final_value = cash

    profit = final_value - STARTING_CAPITAL
    return_pct = profit / STARTING_CAPITAL * 100

    print()
    print("==============================")
    print(name)
    print("==============================")
    print(f"Starting capital: ${STARTING_CAPITAL:.2f}")
    print(f"Final value:      ${final_value:.2f}")
    print(f"Profit/Loss:      ${profit:.2f}")
    print(f"Return:           {return_pct:.2f}%")
    print(f"Completed trades: {completed_trades}")
