import asyncio
import logging
from typing import Dict, List

from app.items.services import get_all_ids_set
from app.prices.models import Price
from app.prices.services import bulk_update as bulk_update_prices
from app.prices.services import get_all as get_all_prices
from app.prices.utils import fetch_prices
from app.ws.connection_manager import ws_conn_manager
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

            existing_item_ids_set = await get_all_ids_set(async_db_session)

            # Compare API prices with DB prices
            new_prices = []
            updated_prices: List[Dict] = []
            for item_id, new_price_data in api_prices["data"].items():
                if item_id not in existing_item_ids_set:
                    continue  # Skip items not in the DB

                old_price = db_prices.get(item_id)

                high = new_price_data.get("high")
                high_time = new_price_data.get("highTime")
                low = new_price_data.get("low")
                low_time = new_price_data.get("lowTime")

                if not old_price:  # Price not in DB
                    new_prices.append(
                        Price(
                            item_id=item_id,
                            high=high,
                            high_time=high_time,
                            low=low,
                            low_time=low_time,
                        )
                    )
                elif old_price.high != high or old_price.low != low:
                    updated_prices.append(
                        {
                            "id": old_price.id,
                            "item_id": item_id,  # No need to update item_id
                            "low": low,
                            "low_time": low_time,
                            "high": high,
                            "high_time": high_time,
                        }  # TODO Only update changed fields
                    )

            log.info(f"Found {len(updated_prices)} items to update.")

            # Bulk add
            if new_prices:
                async_db_session.add_all(new_prices)

            # Bulk update
            if updated_prices:
                await bulk_update_prices(
                    async_db_session,
                    prices_list=[price for price in updated_prices],
                )

                # Notify WebSocket clients about the updated prices
                await ws_conn_manager.broadcast_json(updated_prices)
                print(f"Sent {len(updated_prices)} items")

            await async_db_session.commit()

            log.info("Prices updated successfully.")
        except Exception as e:
            log.error(f"Error updating prices: {e}", exc_info=True)
        finally:
            await asyncio.sleep(interval_seconds)
