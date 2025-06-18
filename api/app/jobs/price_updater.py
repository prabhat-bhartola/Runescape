import asyncio
import logging
from typing import Dict

from app.prices.models import Price
from app.prices.services import bulk_update as bulk_update_prices
from app.prices.services import get_all as get_all_prices
from app.prices.utils import fetch_prices
from sqlmodel.ext.asyncio.session import AsyncSession

log = logging.getLogger(__name__)


async def update_prices_periodically(
    async_db_session: AsyncSession, *, interval_seconds: int = 180
) -> None:
    """
    Periodically fetch and update item prices every `interval_seconds` seconds.
    """
    log.info("Starting periodic price updates...")
    while True:
        try:
            log.info("Fetching prices...")

            api_prices = await fetch_prices()
            db_prices: Dict[str, Price] = {
                price.item_id: price for price in await get_all_prices(async_db_session)
            }

            # Compare API prices with DB prices
            updated_prices = []
            for item_id, new_price_data in api_prices.items():
                old_price = db_prices.get(item_id)
                if not old_price:
                    continue  # item not in DB, or not tracked
                if (
                    old_price.high != new_price_data["high"]
                    or old_price.low != new_price_data["low"]
                ):
                    updated_prices.append(
                        (item_id, new_price_data["high"], new_price_data["low"])
                    )

            # Bulk update
            if updated_prices:
                await bulk_update_prices(
                    async_db_session,
                    prices_list=[
                        {
                            "item_id": item_id,
                            "high": high,
                            "low": low,
                        }
                        for item_id, high, low in updated_prices
                    ],
                )

            log.info("Prices updated successfully.")
        except Exception as e:
            log.error(f"Error updating prices: {e}")
        finally:
            await asyncio.sleep(interval_seconds)
