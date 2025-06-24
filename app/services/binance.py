import httpx
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
async def fetch_ohlcv(pair: str, interval: str = "1h", limit: int = 100):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": pair.upper(),
        "interval": interval,
        "limit": limit
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if not data:
                return None

            df = pd.DataFrame(data, columns=[
                "timestamp", "open", "high", "low", "close", "volume",
                "_", "_", "_", "_", "_", "_"
            ])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

            # Recalculate RSI and MACD
            df["rsi"] = RSIIndicator(close=df["close"], window=14).rsi()
            macd = MACD(close=df["close"])
            df["macd"] = macd.macd()
            df["macd_signal"] = macd.macd_signal()
            df["macd_diff"] = macd.macd_diff()

            return df

        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e}")
            return None
        except Exception as e:
            print(f"Error fetching OHLCV: {e}")
            return None
