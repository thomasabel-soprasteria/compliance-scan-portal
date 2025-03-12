
from fastapi import APIRouter
from app.api.endpoints import reports, requirements, compliance

router = APIRouter()

# Include endpoints from different modules
router.include_router(reports.router, prefix="/reports", tags=["reports"])
router.include_router(requirements.router, prefix="/requirements", tags=["requirements"])
router.include_router(compliance.router, prefix="/compliance", tags=["compliance"])
