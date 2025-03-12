
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from app.db.session import get_db
from app.models.regulatory_requirement import RegulatoryRequirement
from app.schemas.regulatory_requirement import (
    RegulatoryRequirementCreate,
    RegulatoryRequirementUpdate,
    RegulatoryRequirementResponse
)

router = APIRouter()

@router.post("/", response_model=RegulatoryRequirementResponse, status_code=status.HTTP_201_CREATED)
async def create_requirement(
    requirement: RegulatoryRequirementCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new regulatory requirement.
    
    - **requirement**: Regulatory requirement data
    """
    new_requirement = RegulatoryRequirement(**requirement.dict())
    db.add(new_requirement)
    await db.commit()
    await db.refresh(new_requirement)
    
    return new_requirement

@router.get("/", response_model=List[RegulatoryRequirementResponse])
async def list_requirements(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    List all regulatory requirements with optional filtering and pagination.
    
    - **skip**: Number of requirements to skip (for pagination)
    - **limit**: Maximum number of requirements to return
    - **active_only**: If true, return only active requirements
    - **category**: Filter requirements by category
    """
    query = select(RegulatoryRequirement).offset(skip).limit(limit)
    
    if active_only:
        query = query.filter(RegulatoryRequirement.active == True)
    
    if category:
        query = query.filter(RegulatoryRequirement.category == category)
    
    result = await db.execute(query)
    requirements = result.scalars().all()
    
    return requirements

@router.get("/{requirement_id}", response_model=RegulatoryRequirementResponse)
async def get_requirement(
    requirement_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific regulatory requirement by ID.
    
    - **requirement_id**: ID of the requirement to retrieve
    """
    result = await db.execute(
        select(RegulatoryRequirement).filter(RegulatoryRequirement.id == requirement_id)
    )
    requirement = result.scalars().first()
    
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Requirement with ID {requirement_id} not found."
        )
    
    return requirement

@router.patch("/{requirement_id}", response_model=RegulatoryRequirementResponse)
async def update_requirement(
    requirement_id: int,
    requirement_update: RegulatoryRequirementUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a specific regulatory requirement.
    
    - **requirement_id**: ID of the requirement to update
    - **requirement_update**: Data to update
    """
    result = await db.execute(
        select(RegulatoryRequirement).filter(RegulatoryRequirement.id == requirement_id)
    )
    requirement = result.scalars().first()
    
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Requirement with ID {requirement_id} not found."
        )
    
    update_data = requirement_update.dict(exclude_unset=True)
    
    if update_data:
        await db.execute(
            update(RegulatoryRequirement)
            .where(RegulatoryRequirement.id == requirement_id)
            .values(**update_data)
        )
        await db.commit()
        
        # Refresh requirement data
        result = await db.execute(
            select(RegulatoryRequirement).filter(RegulatoryRequirement.id == requirement_id)
        )
        requirement = result.scalars().first()
    
    return requirement

@router.delete("/{requirement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_requirement(
    requirement_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a specific regulatory requirement.
    
    - **requirement_id**: ID of the requirement to delete
    """
    result = await db.execute(
        select(RegulatoryRequirement).filter(RegulatoryRequirement.id == requirement_id)
    )
    requirement = result.scalars().first()
    
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Requirement with ID {requirement_id} not found."
        )
    
    await db.execute(
        delete(RegulatoryRequirement).where(RegulatoryRequirement.id == requirement_id)
    )
    await db.commit()
    
    return None
