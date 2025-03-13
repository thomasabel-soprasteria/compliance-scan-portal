
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from loguru import logger

from app.core.config import settings
from app.models.regulatory_requirement import RegulatoryRequirement
from app.models.report import Report
from app.models.compliance_result import ComplianceResult

# MongoDB client instance
client = None

async def get_db():
    """Get MongoDB database instance."""
    return client[settings.DB_NAME]

async def connect_to_mongo():
    """Connect to MongoDB."""
    global client
    try:
        logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL.split('@')[-1]}")
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        await init_beanie(
            database=client[settings.DB_NAME],
            document_models=[
                RegulatoryRequirement,
                Report,
                ComplianceResult
            ]
        )
        logger.info("Successfully connected to MongoDB")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close MongoDB connection."""
    global client
    if client:
        client.close()
        logger.info("MongoDB connection closed")

async def create_indexes():
    """Create necessary indexes."""
    try:
        # Create indexes as needed
        await RegulatoryRequirement.create_indexes()
        await Report.create_indexes()
        await ComplianceResult.create_indexes()
        logger.info("MongoDB indexes created or already exist")
    except Exception as e:
        logger.error(f"Error creating MongoDB indexes: {e}")
        raise
