
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from loguru import logger
from sqlalchemy.ext.declarative import declarative_base

# Create SQLAlchemy engine
# Convert standard PostgreSQL URL to async version
db_url = str(settings.DATABASE_URL)
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(
    db_url,
    echo=settings.DEBUG,
    future=True,
)

# Create session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create declarative base
Base = declarative_base()

async def get_db() -> AsyncSession:
    """Dependency for getting async DB session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_db_and_tables():
    """Create database tables if they don't exist."""
    async with engine.begin() as conn:
        try:
            # Only create tables that don't exist
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created or already exist")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise
