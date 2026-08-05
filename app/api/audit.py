from fastapi import APIRouter, Request
from app.core.limiter import limiter 

from app.models.schemas import AuditRequest, AuditResponse
from app.services.audit_service import AuditService

router =  APIRouter(prefix="/api", tags=["Audit"])

@router.get("/health")
def health():
    return {
        "status": "healthy"
    }


@router.post("/audit", response_model=AuditResponse)
async def audit(request: Request, body: AuditRequest):
    return await AuditService.audit(
        str(body.url),
        request.state.request_id)