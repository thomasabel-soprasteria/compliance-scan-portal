
from datetime import datetime
from beanie import Document, Indexed, Link
from pydantic import Field
from typing import Optional

from app.models.report import Report
from app.models.regulatory_requirement import RegulatoryRequirement

class ComplianceResult(Document):
    """MongoDB document for compliance check results."""
    report: Link[Report]
    requirement: Link[RegulatoryRequirement]
    is_compliant: Optional[bool] = None
    confidence_score: Optional[float] = None
    extracted_evidence: Optional[str] = None
    analysis_date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "compliance_results"
        indexes = [
            # Compound index to ensure one result per report-requirement pair
            [
                ("report.id", 1),
                ("requirement.id", 1),
            ],
        ]
        
    def __repr__(self):
        return f"<ComplianceResult(id={self.id}, report_id={self.report.id}, requirement_id={self.requirement.id}, is_compliant={self.is_compliant})>"
        
    async def save_with_timestamp(self):
        """Save with updated timestamp."""
        self.updated_at = datetime.utcnow()
        return await self.save()
