import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

print(f"💡 Running script from - {project_root}")


import asyncio
import traceback

import httpx
from app.common.services import get_or_create
from app.config import settings
from app.database.core import get_async_session
from app.models import *  # For SQLAlchemy to have reference of the models

"""
A *NOT* very optimized script to seed the database with initial items data.

Prices are automatically fetched on startup.
"""


async def fetch_items():
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.RUINSCAPE_ITEM_MAPPING_URL)
        response.raise_for_status()  # raises if status != 2xx
        data = response.json()
        return data


async def main():
    async for async_db_session in get_async_session():
        try:
            for item in await fetch_items():
                item["id"] = str(item.pop("id", None))

                await get_or_create(
                    async_db_session,
                    tablename="item",
                    search_by={"id": item["id"]},
                    create_data=item,
                )

            await async_db_session.commit()
            return 0  # Success

        except Exception as e:
            print(f"❌ Error while processing item {item['id']}: {e}")
            print(traceback.format_exc())
            return 1  # Break the loop on error


if __name__ == "__main__":
    result = asyncio.run(main())
    if result == 0:
        print("✅ Script executed successfully.")
    else:
        print("❌ Script failed with an error.")
