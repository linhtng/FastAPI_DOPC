from typing import Any, Dict

import httpx
from fastapi import HTTPException


# TODO: Add unit tests for this class, return json response as expected: test case json response
class HTTPClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout

    async def get(self, endpoint: str) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}{endpoint}")
                # Check specific status code
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"External API returned {response.status_code}: {response.text}",
                    )
                return response.json()
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Request timeout")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")


# TODO: Need unit tests for these exception
# except httpx.TimeoutException:
#     raise HTTPException(status_code=504, detail="Request timeout")
# except httpx.HTTPStatusError as e:
#     raise HTTPException(status_code=e.response.status_code, detail=str(e))
# except Exception as e:
#     raise HTTPException(status_code=500, detail=f"External API error: {str(e)}")
