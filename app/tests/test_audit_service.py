import pytest
from unittest.mock import AsyncMock, patch

from app.services.audit_service import AuditService
from app.services.cache_service import cache

@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_success(mock_get):

    response = AsyncMock()

    response.status_code = 200

    response.url = "https://example.com"

    response.headers = {
        "content-type": "text/html"
    }

    response.text = """
    <html>
        <title>Example</title>
    </html>
    """

    mock_get.return_value = response

    result = await AuditService.audit(
        "https://example.com",
        "test-id"
    )

    assert result["success"] is True

    assert result["status_code"] == 200

    assert result["title"] == "Example"


import httpx

@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_timeout(mock_get):

    mock_get.side_effect = httpx.TimeoutException(
        "Timeout"
    )

    try:

        await AuditService.audit(
            "https://example.com",
            "test-id"
        )

    except Exception as e:

        assert e.status_code == 504


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_request_error(mock_get):

    mock_get.side_effect = httpx.RequestError(
        "Connection failed"
    )

    try:

        await AuditService.audit(
            "https://example.com",
            "test-id"
        )

    except Exception as e:

        assert e.status_code == 502


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_cache(mock_get):

    cache.clear()

    response = AsyncMock()

    response.status_code = 200

    response.url = "https://example.com"

    response.headers = {
        "content-type": "text/html"
    }

    response.text = "<title>Example</title>"

    mock_get.return_value = response

    result1 = await AuditService.audit(
        "https://example.com",
        "1"
    )

    result2 = await AuditService.audit(
        "https://example.com",
        "2"
    )

    assert result1["cached"] is False

    assert result2["cached"] is True