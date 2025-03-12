
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, func, and_

from app.db.session import get_db
from app.models.report import Report, ReportStatus
from app.models.regulatory_requirement import RegulatoryRequirement
from app.models.compliance_result import ComplianceResult
from app.schemas.compliance_result import (
    ComplianceResultCreate,
    ComplianceResultUpdate,
    ComplianceResultResponse,
    ComplianceSummaryResponse,
    RequirementResultResponse
)
from app.services.compliance_checker import check_compliance_for_report

router = APIRouter()

@router.post("/check/{report_id}", status_code=status.HTTP_202_ACCEPTED)
async def trigger_compliance_check(
    report_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Trigger a compliance check for a specific report.
    
    - **report_id**: ID of the report to check
    """
    result = await db.execute(select(Report).filter(Report.id == report_id))
    report = result.scalars().first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with ID {report_id} not found."
        )
    
    if report.status != ReportStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Report with ID {report_id} is not ready for compliance check (status: {report.status})."
        )
    
    # Update report status to processing
    await db.execute(
        update(Report)
        .where(Report.id == report_id)
        .values(status=ReportStatus.PROCESSING)
    )
    await db.commit()
    
    # Trigger background compliance check
    background_tasks.add_task(
        check_compliance_for_report,
        report_id
    )
    
    return {"message": f"Compliance check for report ID {report_id} has been triggered."}

@router.get("/report/{report_id}", response_model=ComplianceSummaryResponse)
async def get_compliance_summary(
    report_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get compliance check summary for a specific report.
    
    - **report_id**: ID of the report to get summary for
    """
    # Check if report exists
    report_result = await db.execute(select(Report).filter(Report.id == report_id))
    report = report_result.scalars().first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with ID {report_id} not found."
        )
    
    # Get all active requirements
    req_result = await db.execute(
        select(RegulatoryRequirement).filter(RegulatoryRequirement.active == True)
    )
    requirements = req_result.scalars().all()
    
    # Get compliance results for this report
    result_query = select(ComplianceResult).filter(ComplianceResult.report_id == report_id)
    result_result = await db.execute(result_query)
    results = result_result.scalars().all()
    
    # Calculate summary statistics
    total_requirements = len(requirements)
    compliant_count = sum(1 for r in results if r.is_compliant is True)
    non_compliant_count = sum(1 for r in results if r.is_compliant is False)
    pending_count = total_requirements - (compliant_count + non_compliant_count)
    
    overall_compliance_percentage = (compliant_count / total_requirements * 100) if total_requirements > 0 else 0
    
    # Create detailed results
    detailed_results = []
    
    # Create a lookup dict for the results
    results_by_req_id = {r.requirement_id: r for r in results}
    
    for req in requirements:
        result = results_by_req_id.get(req.id)
        detailed_results.append(
            RequirementResultResponse(
                id=req.id,
                name=req.name,
                description=req.description,
                category=req.category,
                is_compliant=result.is_compliant if result else None,
                confidence_score=result.confidence_score if result else None,
                extracted_evidence=result.extracted_evidence if result else None
            )
        )
    
    return ComplianceSummaryResponse(
        report_id=report_id,
        total_requirements=total_requirements,
        compliant_count=compliant_count,
        non_compliant_count=non_compliant_count,
        pending_count=pending_count,
        overall_compliance_percentage=overall_compliance_percentage,
        results=detailed_results
    )

@router.post("/result", response_model=ComplianceResultResponse, status_code=status.HTTP_201_CREATED)
async def create_compliance_result(
    result: ComplianceResultCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new compliance result.
    
    - **result**: Compliance result data
    """
    # Check if report exists
    report_result = await db.execute(select(Report).filter(Report.id == result.report_id))
    report = report_result.scalars().first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with ID {result.report_id} not found."
        )
    
    # Check if requirement exists
    req_result = await db.execute(select(RegulatoryRequirement).filter(RegulatoryRequirement.id == result.requirement_id))
    requirement = req_result.scalars().first()
    
    if not requirement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Requirement with ID {result.requirement_id} not found."
        )
    
    # Check if result already exists
    existing_result = await db.execute(
        select(ComplianceResult).filter(
            and_(
                ComplianceResult.report_id == result.report_id,
                ComplianceResult.requirement_id == result.requirement_id
            )
        )
    )
    
    if existing_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A compliance result for report ID {result.report_id} and requirement ID {result.requirement_id} already exists."
        )
    
    # Create new compliance result
    new_result = ComplianceResult(**result.dict())
    db.add(new_result)
    await db.commit()
    await db.refresh(new_result)
    
    return new_result

@router.patch("/result/{result_id}", response_model=ComplianceResultResponse)
async def update_compliance_result(
    result_id: int,
    result_update: ComplianceResultUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a specific compliance result.
    
    - **result_id**: ID of the compliance result to update
    - **result_update**: Data to update
    """
    result = await db.execute(select(ComplianceResult).filter(ComplianceResult.id == result_id))
    compliance_result = result.scalars().first()
    
    if not compliance_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Compliance result with ID {result_id} not found."
        )
    
    update_data = result_update.dict(exclude_unset=True)
    
    if update_data:
        await db.execute(
            update(ComplianceResult)
            .where(ComplianceResult.id == result_id)
            .values(**update_data)
        )
        await db.commit()
        
        # Refresh result data
        result = await db.execute(select(ComplianceResult).filter(ComplianceResult.id == result_id))
        compliance_result = result.scalars().first()
    
    return compliance_result
