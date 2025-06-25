from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from dotenv import load_dotenv

from app.backtest.strategy import backtest_strategy
from app.routers import predict, backtest
from app.utils.db import init_db

# Load environment variables
load_dotenv()

# Initialize DB
init_db()

# Create FastAPI app
app = FastAPI(title="AI Futures Backend")

# Optional: Prevent trailing slash redirect issues
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Include routers
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])
app.include_router(backtest.router, prefix="/backtest", tags=["Backtest"])

# Root route
@app.get("/")
def read_root():
    return {"message": "AI Trading Assistant Backend is Running"}


# @router.get("/backtest")
async def run_backtest(pair: str = "ETHUSDT"):
    results = await backtest_strategy(pair)
    return results