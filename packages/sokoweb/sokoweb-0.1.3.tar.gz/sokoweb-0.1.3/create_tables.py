# create_tables.py

import asyncio
from sokoweb.database import engine, Base
from sokoweb.db_models import User, Product, NodeCredit

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())