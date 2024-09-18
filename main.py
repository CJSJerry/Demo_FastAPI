from fastapi import FastAPI
from contextlib import asynccontextmanager
from dependencies import connect_db
from endpoints import country, product_category, customer, product, installation
from typing import AsyncGenerator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage the lifespan of the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Indicates that the lifespan context is active.
    """
    app.state.db = await connect_db()
    try:
        yield
    finally:
        await app.state.db.close()

app = FastAPI(lifespan=lifespan)

app.include_router(country.router, prefix="/v1")
app.include_router(customer.router, prefix="/v1")
app.include_router(product_category.router, prefix="/v1")
app.include_router(product.router, prefix="/v1")
app.include_router(installation.router, prefix="/v1")