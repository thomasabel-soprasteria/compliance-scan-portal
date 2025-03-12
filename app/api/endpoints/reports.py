
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, BackgroundTasks
from fastapi.responses import FileResponse
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
import os
import shutil
from datetime import datetime
from loguru import logger

from app.db.session import get_db
from app.models.report import Report, ReportStatus
from app.schemas.report import ReportCreate, ReportUpdate, ReportResponse, ReportDetail
from app.services.pdf_processor import process_pdf_report
from app.core.config import settings

router = APIRouter()

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def upload_report(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    company_name: Optional[str] = Form(None),
    fiscal_year: Optional[int] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload a new annual report PDF file.
    
    - **file**: PDF file to upload
    - **company_name**: Name of the company (optional)
    - **fiscal_year**: Fiscal year of the report (optional)
    """
    # Validate file extension
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted."
        )
    
    # Validate file size
    file_size = 0
    content = await file.read()
    file_size = len(content)
    await file.seek(0)
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds the maximum allowed size of {settings.MAX_UPLOAD_SIZE / (1024 * 1024)}MB."
        )
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(settings.TEMP_UPLOAD_DIR, filename)
    
    # Save file to disk
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not save the file."
        )
    
    # Create database record
    new_report = Report(
        file_name=file.filename,
        file_path=file_path,
        file_size=file_size,
        status=ReportStatus.PENDING,
        company_name=company_name,
        fiscal_year=fiscal_year
    )
    
    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)
    
    # Process PDF in background
    background_tasks.add_task(
        process_pdf_report,
        new_report.id,
        file_path
    )
    
    return new_report

@router.get("/", response_model=List[ReportResponse])
async def list_reports(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ReportStatus] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    List all uploaded reports with optional filtering and pagination.
    
    - **skip**: Number of reports to skip (for pagination)
    - **limit**: Maximum number of reports to return
    - **status**: Filter reports by status
    """
    query = select(Report).offset(skip).limit(limit).order_by(Report.upload_date.desc())
    
    if status:
        query = query.filter(Report.status == status)
    
    result = await db.execute(query)
    reports = result.scalars().all()
    
    return reports

@router.get("/{report_id}", response_model=ReportDetail)
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed information about a specific report.
    
    - **report_id**: ID of the report to retrieve
    """
    result = await db.execute(select(Report).filter(Report.id == report_id))
    report = result.scalars().first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with ID {report_id} not found."
        )
    
    return report

@router.get("/{report_id}/download")
async def download_report(
    report_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Download the original PDF file for a specific report.
    
    - **report_id**: ID of the report to download
    """
    result = await db.execute(select(Report).filter(Report.id == report_id))
    report = result.scalars().first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with ID {report_id} not found."
        )
    
    if not os.path.exists(report.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The file for this report is not available."
        )
    
    return FileResponse(
        path=report.file_path,
        filename=report.file_name,
        media_type="application/pdf"
    )

@router.patch("/{report_id}", response_model=ReportResponse)
async def update_report(
    report_id: int,
    report_update: ReportUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update information about a specific report.
    
    - **report_id**: ID of the report to update
    - **report_update**: Data to update
    """
    result = await db.execute(select(Report).filter(Report.id == report_id))
    report = result.scalars().first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with ID {report_id} not found."
        )
    
    update_data = report_update.dict(exclude_unset=True)
    
    if update_data:
        await db.execute(
            update(Report)
            .where(Report.id == report_id)
            .values(**update_data)
        )
        await db.commit()
        
        # Refresh report data
        result = await db.execute(select(Report).filter(Report.id == report_id))
        report = result.scalars().first()
    
    return report

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    report_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a specific report and its associated file.
    
    - **report_id**: ID of the report to delete
    """
    result = await db.execute(select(Report).filter(Report.id == report_id))
    report = result.scalars().first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with ID {report_id} not found."
        )
    
    # Delete file if it exists
    if os.path.exists(report.file_path):
        try:
            os.remove(report.file_path)
        except Exception as e:
            logger.error(f"Error deleting file {report.file_path}: {e}")
            # Continue with deletion even if file removal fails
    
    # Delete database record
    await db.delete(report)
    await db.commit()
    
    return None
