import httpx
from app.config import settings

# TODO Do not raise


async def fetch_prices():
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.RUINSCAPE_ITEM_PRICES_URL)
        response.raise_for_status()  # raises if status != 2xx
        data = response.json()
        return data
