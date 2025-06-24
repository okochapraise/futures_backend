import pandas as pd
from app.services.binance import fetch_ohlcv
from app.services.news import fetch_crypto_news  # optional, mock this if needed
from ta.momentum import RSIIndicator
from ta.trend import MACD

async def backtest_strategy(pair: str = "BTCUSDT", limit: int = 100):
    df = await fetch_ohlcv(pair, limit=limit)
    if df is None or df.empty:
        return {"error": f"No data available for {pair}"}

    trades = []
    position = None
    entry_price = 0
    pnl = 0

    for i in range(50, len(df)):  # skip warm-up period
        current = df.iloc[i]
        rsi = current["rsi"]
        macd = current["macd"]
        macd_signal = current["macd_signal"]
        close_price = current["close"]
        timestamp = current["timestamp"]

        action = "Hold"
        if rsi < 30 and macd > macd_signal:
            action = "Buy"
        elif rsi > 70 and macd < macd_signal:
            action = "Sell"
        elif macd > macd_signal:
            action = "Buy"
        elif macd < macd_signal:
            action = "Sell"

        # execute trades
        if action == "Buy" and position is None:
            position = {
                "entry": close_price,
                "entry_time": timestamp
            }
        elif action == "Sell" and position is not None:
            profit = close_price - position["entry"]
            trades.append({
                "entry_time": position["entry_time"],
                "exit_time": timestamp,
                "entry": position["entry"],
                "exit": close_price,
                "profit": round(profit, 2)
            })
            pnl += profit
            position = None  # close position

    # summary
    wins = len([t for t in trades if t["profit"] > 0])
    losses = len(trades) - wins
    total_trades = len(trades)

    return {
        "pair": pair,
        "total_trades": total_trades,
        "win_rate": round(wins / total_trades * 100, 2) if total_trades > 0 else 0,
        "total_profit": round(pnl, 2),
        "trades": trades[-5:],  
        "data_points": len(df),
        "sample_result": df.tail(5).to_dict(orient="records")    
        }
