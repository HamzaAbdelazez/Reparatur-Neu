import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.database import table_models
from api.config.core import settings

logger = logging.getLogger(__name__)

# Create asynchronous SQLAlchemy engine using the database URL from settings
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Create a session factory bound to the async engine, with sessions that do not expire objects on commit
AsyncSessionFactory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    """
    Async generator function that provides a database session.

    Yields:
        AsyncSession: An asynchronous SQLAlchemy database session.

    Usage:
        Use this as a dependency in async frameworks (e.g., FastAPI) to provide a DB session.
    """
    async with AsyncSessionFactory() as db:
        yield db


async def init_db_tables():
    """
    Initialize database tables
    """
    async with engine.connect() as conn:
        logger.info(f"Connecting to DB: {settings.DATABASE_URL}")
        for table in table_models.Base.metadata.tables:
            logger.info(f"Found table model: {table}")

        logger.info("Creating all tables")
        await conn.run_sync(table_models.Base.metadata.create_all)
