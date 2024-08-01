from fastapi import APIRouter, Depends, HTTPException, Path, Query
from app.services.alpha_vantage_service import AlphaVantageService
from app.models.commodity_data import *
from time import sleep
from typing import Optional
from datetime import datetime

router = APIRouter()

@router.get("/commodity/{function}", response_model=Commodity)
async def get_commodity_data(
    function: str = Path(..., description="Commodity function (e.g., WTI, BRENT)"),
    interval: Interval = Query(Interval.monthly, description="Data interval (e.g. weekly, monthly, daily)"),
    start_date: Optional[str] = Query(None, description="Start date for filtering (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date for filtering (YYYY-MM-DD)"),
    alpha_vantage_service: AlphaVantageService = Depends()
):
    """
    This function retrieves commodity prices
    """
    print(f"Received request for {function} with interval {interval}")
    try:
        data = await alpha_vantage_service.get_commodity_data(function, interval) 
        
        commodity_response = Commodity(
            name = data["name"],
            interval = interval,
            unit = data["unit"],
            data = [CommodityData(**item) for item in data["data"]]
        )
        print("commodity_response is: ", commodity_response.data)
        if start_date or end_date:
            start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
            end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
            filtered_data = [
                item for item in commodity_response.data
                if (not start or datetime.strptime(item.date, "%Y-%m-%d") >= start) and
                (not end or datetime.strptime(item.date, "%Y-%m-%d") <= end)
            ]
            commodity_response.data = filtered_data
        
        return commodity_response

    except ValueError as e:
        print(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.get("/sleep")
def hello():
    """ Dummy endpoint for testing async workflows """
    print("sleeping")
    sleep(30)
    print("waking up")