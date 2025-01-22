from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from app.http_client import HTTPClient
from app.venue_service import VenueService


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


# Run with:
# python -m pytest tests/test_venue_service.py -v
