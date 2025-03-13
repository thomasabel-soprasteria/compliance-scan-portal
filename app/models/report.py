
from datetime import datetime
from enum import Enum
from beanie import Document, Indexed
from pydantic import Field
from typing import Optional

class ReportStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Report(Document):
    """MongoDB document for uploaded reports."""
    file_name: Indexed(str)
    file_path: str
    file_size: int
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    status: ReportStatus = ReportStatus.PENDING
    company_name: Optional[str] = None
    fiscal_year: Optional[int] = None
    processed_text: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "reports"
        
    def __repr__(self):
        return f"<Report(id={self.id}, file_name='{self.file_name}', status='{self.status}')>"
        
    async def save_with_timestamp(self):
        """Save with updated timestamp."""
        self.updated_at = datetime.utcnow()
        return await self.save()
