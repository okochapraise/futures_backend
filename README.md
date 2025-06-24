# 🧠 AI-Powered Crypto Signal Backend (FastAPI)

This backend is a FastAPI-based application that analyzes cryptocurrency trading pairs (e.g., `BTCUSDT`, `ETHUSDT`) and generates intelligent buy/sell signals using:

- 📊 **Technical Indicators** – RSI, MACD, crossovers  
- 📰 **News Sentiment Analysis** – Real-time sentiment from crypto headlines  
- 💌 **Email Alerts** – Automatically sends high-confidence trade signals to a configured email  
- 💾 **Database Logging** – Stores only strong signals (confidence ≥ 70%) for historical review  
- 🔬 **Backtesting Engine** – Simulates past trades using the rule-based strategy for performance analysis  
- 🔐 **Secure Setup** – API keys, email credentials, and environment variables kept safe in `.env` (excluded from version control)

## 🔗 Endpoints
- `/predict?pair=ETHUSDT` → Get AI signal for a pair  
- `/predict/history?page=1` → View logged signals (paginated)  
- `/backtest?pair=ETHUSDT&limit=200` → Run backtest on historical data  

## 🛠 Tech Stack
- **FastAPI**  
- **HTTPX**  
- **Pandas + TA**  
- **SQLite**  
- **Render (deployment)**  
