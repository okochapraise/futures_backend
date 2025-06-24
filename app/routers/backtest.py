from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.backtest.strategy import backtest_strategy
import traceback

router = APIRouter()

@router.get("/backtest")
async def run_backtest(
    pair: str = Query("", description="Trading pair like BTCUSDT"),
    limit: int = Query(100, ge=50, le=1000, description="Number of candles to fetch (50–1000)")
):
    try:
        results = await backtest_strategy(pair, limit=limit)
        return results
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "trace": traceback.format_exc()
        })
