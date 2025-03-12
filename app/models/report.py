
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from app.db.session import Base
import enum
from datetime import datetime

class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Report(Base):
    """Database model for uploaded reports."""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING, nullable=False)
    company_name = Column(String(255))
    fiscal_year = Column(Integer)
    processed_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Report(id={self.id}, file_name='{self.file_name}', status='{self.status}')>"
