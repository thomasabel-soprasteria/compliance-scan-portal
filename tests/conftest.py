
import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.db.session import Base, get_db
from app.core.config import settings

# Create a test database URL (in-memory SQLite for tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create a test engine
engine = create_async_engine(TEST_DATABASE_URL, echo=True)

# Create a session factory
TestingSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest.fixture
async def db_session():
    # Create all tables in the test database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create a session
    async with TestingSessionLocal() as session:
        yield session
    
    # Drop all tables after tests complete
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client(db_session):
    # Override the get_db dependency to use the test database
    async def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Use AsyncClient for testing
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    # Remove the override
    app.dependency_overrides.clear()
