import asyncpg
from dotenv import load_dotenv
import os
from typing import AsyncGenerator

# Load database url from .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL").strip()

async def connect_db() -> asyncpg.Connection:
    """Establish a connection to the database.

    Returns:
        asyncpg.Connection: The database connection.
    """
    return await asyncpg.connect(DATABASE_URL)

async def get_db() -> AsyncGenerator[asyncpg.Connection, None]:
    """Yield a database connection and ensure it is closed properly.

    Yields:
        asyncpg.Connection: The database connection.
    """
    db = await connect_db()
    try:
        yield db
    finally:
        await db.close()