
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RegulatoryRequirementBase(BaseModel):
    """Base schema for regulatory requirement data."""
    name: str
    description: str
    category: Optional[str] = None
    active: bool = True

class RegulatoryRequirementCreate(RegulatoryRequirementBase):
    """Schema for creating a new regulatory requirement."""
    pass

class RegulatoryRequirementUpdate(BaseModel):
    """Schema for updating an existing regulatory requirement."""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    active: Optional[bool] = None

class RegulatoryRequirementResponse(RegulatoryRequirementBase):
    """Schema for regulatory requirement response data."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
