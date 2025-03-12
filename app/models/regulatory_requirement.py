
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from app.db.session import Base
from datetime import datetime

class RegulatoryRequirement(Base):
    """Database model for regulatory requirements."""
    __tablename__ = "regulatory_requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100))
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<RegulatoryRequirement(id={self.id}, name='{self.name}', active={self.active})>"
