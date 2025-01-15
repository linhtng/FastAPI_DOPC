from typing import Any, Dict
import httpx
from fastapi import HTTPException


class HTTPClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout

    async def get(self, endpoint: str) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                response.raise_for_status()
                return response.json()
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Request timeout")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")
