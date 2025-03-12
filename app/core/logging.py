
import sys
import os
from loguru import logger
from app.core.config import settings

def configure_logging():
    """Configure logging for the application."""
    # Remove default logger
    logger.remove()
    
    # Configure logger
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    
    # Add console logger
    logger.add(
        sys.stderr, 
        format=log_format, 
        level=settings.LOG_LEVEL,
        colorize=True
    )
    
    # Add file logger
    os.makedirs("logs", exist_ok=True)
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="7 days",
        format=log_format,
        level=settings.LOG_LEVEL,
        backtrace=True,
        diagnose=True
    )
    
    logger.info("Logging configured with level: {}", settings.LOG_LEVEL)
