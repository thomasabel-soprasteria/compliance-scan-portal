
from datetime import datetime
from beanie import Document, Indexed
from pydantic import Field
from typing import Optional

class RegulatoryRequirement(Document):
    """MongoDB document for regulatory requirements."""
    name: Indexed(str)
    description: str
    category: Optional[str] = None
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "regulatory_requirements"
        
    def __repr__(self):
        return f"<RegulatoryRequirement(id={self.id}, name='{self.name}', active={self.active})>"
        
    async def save_with_timestamp(self):
        """Save with updated timestamp."""
        self.updated_at = datetime.utcnow()
        return await self.save()
