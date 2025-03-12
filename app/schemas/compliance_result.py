
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ComplianceResultBase(BaseModel):
    """Base schema for compliance result data."""
    report_id: int
    requirement_id: int
    is_compliant: Optional[bool] = None
    confidence_score: Optional[float] = None
    extracted_evidence: Optional[str] = None

class ComplianceResultCreate(ComplianceResultBase):
    """Schema for creating a new compliance result."""
    pass

class ComplianceResultUpdate(BaseModel):
    """Schema for updating an existing compliance result."""
    is_compliant: Optional[bool] = None
    confidence_score: Optional[float] = None
    extracted_evidence: Optional[str] = None

class ComplianceResultResponse(ComplianceResultBase):
    """Schema for compliance result response data."""
    id: int
    analysis_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RequirementResultResponse(BaseModel):
    """Schema for combined requirement and result response."""
    id: int
    name: str
    description: str
    category: Optional[str]
    is_compliant: Optional[bool]
    confidence_score: Optional[float]
    extracted_evidence: Optional[str]

    class Config:
        orm_mode = True

class ComplianceSummaryResponse(BaseModel):
    """Schema for compliance summary response."""
    report_id: int
    total_requirements: int
    compliant_count: int
    non_compliant_count: int
    pending_count: int
    overall_compliance_percentage: float
    results: List[RequirementResultResponse]

    class Config:
        orm_mode = True
