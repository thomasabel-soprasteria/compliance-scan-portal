
from sqlalchemy import Column, Integer, Boolean, Float, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime

class ComplianceResult(Base):
    """Database model for compliance check results."""
    __tablename__ = "compliance_results"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id", ondelete="CASCADE"), nullable=False)
    requirement_id = Column(Integer, ForeignKey("regulatory_requirements.id", ondelete="CASCADE"), nullable=False)
    is_compliant = Column(Boolean)
    confidence_score = Column(Float)
    extracted_evidence = Column(Text)
    analysis_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Unique constraint to ensure one result per report-requirement pair
    __table_args__ = (UniqueConstraint('report_id', 'requirement_id', name='uix_report_requirement'),)
    
    def __repr__(self):
        return f"<ComplianceResult(id={self.id}, report_id={self.report_id}, requirement_id={self.requirement_id}, is_compliant={self.is_compliant})>"
