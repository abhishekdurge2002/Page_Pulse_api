from pydantic import BaseModel, HttpUrl  
from typing import Optional, Dict
from datetime import datetime

class AuditRequest(BaseModel):
    url: HttpUrl


class AuditResponse(BaseModel):
    success: bool
    request_id: str
    timestamp: datetime
    url: str
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None
    title: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    error: Optional[str] = None
    cached: bool = False