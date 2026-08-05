import time
from datetime import datetime, timezone

import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException

from app.core.config import settings
from app.services.cache_service import cache
from app.utils.logger import logger


class AuditService:

    @staticmethod
    async def audit(url: str, request_id: str):

        # Check cache first
        if url in cache:
            cached_result = cache[url].copy()

            # Update request-specific fields
            cached_result["cached"] = True
            cached_result["request_id"] = request_id
            cached_result["timestamp"] = datetime.now(timezone.utc)

            logger.info(
                "cache_hit",
                request_id=request_id,
                url=url
            )

            return cached_result

        start = time.perf_counter()

        try:
            logger.info(
                "audit_started",
                request_id=request_id,
                url=url
            )

            async with httpx.AsyncClient(
                timeout=settings.REQUEST_TIMEOUT,
                follow_redirects=True
            ) as client:

                response = await client.get(url)

            elapsed = round((time.perf_counter() - start) * 1000, 2)

            title = None

            if "text/html" in response.headers.get("content-type", ""):
                soup = BeautifulSoup(response.text, "html.parser")

                if soup.title and soup.title.string:
                    title = soup.title.string.strip()

            result = {
                "success": True,
                "request_id": request_id,
                "timestamp": datetime.now(timezone.utc),
                "url": str(response.url),
                "status_code": response.status_code,
                "response_time_ms": elapsed,
                "title": title,
                "headers": dict(response.headers),
                "error": None,
                "cached": False
            }

            # Store in cache
            cache[url] = result

            logger.info(
                "audit_completed",
                request_id=request_id,
                url=url,
                status=response.status_code,
                response_time_ms=elapsed
            )

            return result

        except httpx.TimeoutException:

            logger.error(
                "request_timeout",
                request_id=request_id,
                url=url
            )

            raise HTTPException(
                status_code=504,
                detail={
                    "success": False,
                    "request_id": request_id,
                    "timestamp": datetime.now(timezone.utc),
                    "url": url,
                    "error": "Request timed out"
                }
            )

        except httpx.RequestError as e:

            logger.error(
                "request_failed",
                request_id=request_id,
                url=url,
                error=str(e)
            )

            raise HTTPException(
                status_code=502,
                detail={
                    "success": False,
                    "request_id": request_id,
                    "timestamp": datetime.now(timezone.utc),
                    "url": url,
                    "error": str(e)
                }
            )

        except Exception as e:

            logger.exception(
                "unexpected_error",
                request_id=request_id,
                url=url,
                error=str(e)
            )

            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "request_id": request_id,
                    "timestamp": datetime.now(timezone.utc),
                    "url": url,
                    "error": "Internal Server Error"
                }
            )