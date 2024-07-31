import httpx
from app.models.commodity_data import Commodity, Interval

class AlphaVantageService:
    def __init__(self):
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = "ZUTMJQV502645BUD"

    async def get_commodity_data(self, function: str, interval: Interval) -> Commodity:
        params = {
            "function": function,
            "interval": interval.value,
            "apikey": self.api_key
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()