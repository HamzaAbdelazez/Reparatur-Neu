import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.status import HTTP_200_OK

from api.config.core import configure_logging
from api.config.db import init_db_tables
from api.routers.users import router as users_router
from api.routers.uploaded_pdfs import router as uploaded_pdfs_router

# Set up logging configuration
configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan event to run startup and shutdown code.

    Initializes database tables when the app starts.
    """
    try:
        logger.info("Initializing database tables")
        await init_db_tables()
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize DB tables: {e}")
        raise
    yield  # Continue running the app


app = FastAPI(title="Reparatur API", lifespan=lifespan)

app.include_router(users_router)

app.include_router(uploaded_pdfs_router)


@app.get(
    path="/",
    operation_id="getHealth",
    status_code=HTTP_200_OK,
)
async def health():
    """
    Simple health check endpoint.

    Returns:
        A message confirming the API is running.
    """
    return {"message": "Reparatur API is up and running!"}


if __name__ == "__main__":
    # Start the server with live reload for development
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
