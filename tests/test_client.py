from fastapi import HTTPException
import httpx
import pytest
from unittest.mock import AsyncMock, patch
from app.utils.http_client import HTTPClient
from app.services.venue_service import VenueService


@pytest.fixture
def client():
    return HTTPClient(base_url="http://test.com")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status_code,expected_status,error_message",
    [
        (404, 404, "Not Found"),
        (500, 500, "Server Error"),
        (403, 403, "Forbidden"),
    ],
)
async def test_http_errors(client, status_code, expected_status, error_message):
    mock_response = AsyncMock()
    mock_response.status_code = status_code
    mock_response.text = error_message

    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_instance

        with pytest.raises(HTTPException) as exc:
            await client.get("/test")
        assert exc.value.status_code == expected_status


@pytest.mark.asyncio
async def test_timeout_error(client):
    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.get.side_effect = httpx.TimeoutException("Timeout")
        mock_client.return_value.__aenter__.return_value = mock_instance

        with pytest.raises(HTTPException) as exc:
            await client.get("/test")
        assert exc.value.status_code == 504
        assert "timeout" in exc.value.detail.lower()


@pytest.mark.asyncio
async def test_venue_service_http_errors():
    # Setup mock HTTP client
    mock_client = AsyncMock(spec=HTTPClient)

    # Test cases
    test_cases = [
        (404, "Venue not found"),
        (500, "Internal server error"),
        (503, "Service unavailable"),
    ]

    for status_code, error_message in test_cases:
        # Mock client to raise HTTPException
        mock_client.get.side_effect = HTTPException(
            status_code=status_code, detail=error_message
        )

        # Create service with mocked client
        service = VenueService()
        service.client = mock_client

        # Test static endpoint
        with pytest.raises(HTTPException) as exc_info:
            await service.get_venue_static("test-venue")
        assert exc_info.value.status_code == status_code

        # Test dynamic endpoint
        with pytest.raises(HTTPException) as exc_info:
            await service.get_venue_dynamic("test-venue")
        assert exc_info.value.status_code == status_code
