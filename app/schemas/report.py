
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class ReportStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ReportBase(BaseModel):
    """Base schema for report data."""
    company_name: Optional[str] = None
    fiscal_year: Optional[int] = None

class ReportCreate(ReportBase):
    """Schema for creating a new report."""
    # No additional fields needed - file is handled separately

class ReportUpdate(ReportBase):
    """Schema for updating an existing report."""
    company_name: Optional[str] = None
    fiscal_year: Optional[int] = None
    status: Optional[ReportStatus] = None

class ReportResponse(ReportBase):
    """Schema for report response data."""
    id: int
    file_name: str
    file_size: int
    upload_date: datetime
    status: ReportStatus
    company_name: Optional[str] = None
    fiscal_year: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ReportDetail(ReportResponse):
    """Detailed report schema including processing details."""
    processed_text: Optional[str] = None

    class Config:
        orm_mode = True
