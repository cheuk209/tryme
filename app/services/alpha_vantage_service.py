import httpx
from app.models.commodity_data import Commodity, Interval, CommodityData
from app.core.config import settings, logging

logger = logging.getLogger(__name__)

class AlphaVantageService:
    def __init__(self):
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = settings.ALPHA_VANTAGE_API_KEY

    async def get_commodity_data(self, function: str, interval: Interval) -> Commodity:
        logger.info(f"Fetching commodity data for function: {function}, interval: {interval}")
        params = {
            "function": function,
            "interval": interval.value,
            "apikey": self.api_key
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            return Commodity(
                name = data["name"],
                interval = interval,
                unit = data["unit"],
                data = [CommodityData(**item) for item in data["data"]]
            )
            