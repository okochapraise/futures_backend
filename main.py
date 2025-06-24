from fastapi import FastAPI
from app.routers import predict
from dotenv import load_dotenv
load_dotenv()
from app.utils.db import init_db
from fastapi import APIRouter
from app.routers import backtest  
from app.backtest.strategy import backtest_strategy

init_db()

router = APIRouter()

app = FastAPI(title="AI Futures Backend")

app.include_router(predict.router, prefix="/predict", tags=["Prediction"])
app.include_router(backtest.router, prefix="/backtest", tags=["Backtest"]) 

@app.get("/")
def read_root():
    return {"message": "AI Trading Assistant Backend is Running"}

@router.get("/backtest")
async def run_backtest(pair: str = "ETHUSDT"):
    results = await backtest_strategy(pair)
    return results