from fastapi import APIRouter  # type: ignore[import-not-found]

router =  APIRouter(prefix="/api", tags=["Audit"])

@router.get("/health")
def health():
    return {
        "status": "healthy"
    }