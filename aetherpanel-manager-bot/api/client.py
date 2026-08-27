# AetherPanel Manager Bot
# Made by ZenseiBabe

import asyncio
import aiohttp
from config.config import AETHERPANEL_URL, AETHERPANEL_API_KEY, REQUEST_TIMEOUT
from utils.logger import get_logger

logger = get_logger("AetherAPI")

class AetherAPIClient:
    """
    Centralized HTTP Client for interaction with the AetherPanel REST API.
    Provides robust URL formatting, authorization masking, and comprehensive error containment.
    """
    def __init__(self, base_url: str = AETHERPANEL_URL, api_key: str = AETHERPANEL_API_KEY, timeout: int = REQUEST_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def _request(self, method: str, path: str, json_data: dict = None) -> dict:
        url = f"{self.base_url}{path}"
        headers = self._get_headers()

        # Security mask for logging
        masked_headers = headers.copy()
        if "Authorization" in masked_headers:
            masked_headers["Authorization"] = "Bearer [REDACTED]"

        logger.info(f"API Send: {method} {path}")

        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.request(method, url, headers=headers, json=json_data) as response:
                    status = response.status
                    
                    if status in (204, 201) and response.content_length == 0:
                        return {"success": True, "status": status}

                    try:
                        resp_json = await response.json()
                    except Exception:
                        text = await response.text()
                        resp_json = {"text": text}

                    if 200 <= status < 300:
                        if isinstance(resp_json, list):
                            return {"data": resp_json, "status": status}
                        if "status" not in resp_json:
                            resp_json["status"] = status
                        return resp_json

                    # Error handling logs
                    logger.error(f"API Error Response: {method} {path} | Status: {status} | Error: {resp_json}")
                    return {
                        "error": True,
                        "status": status,
                        "message": resp_json.get("message", resp_json.get("error", "Unknown API error")),
                        "details": resp_json
                    }

        except asyncio.TimeoutError:
            logger.error(f"API Request Timeout: {method} {path}")
            return {
                "error": True,
                "status": 408,
                "message": "Connection to AetherPanel timed out.",
                "details": f"The requested operation exceeded the limit of {REQUEST_TIMEOUT} seconds."
            }
        except aiohttp.ClientConnectorError as e:
            logger.error(f"API Connection Failure: {method} {path} | Error: {e}")
            return {
                "error": True,
                "status": 503,
                "message": "AetherPanel REST Endpoint Unreachable.",
                "details": str(e)
            }
        except Exception as e:
            logger.error(f"Unexpected API exception: {method} {path} | Error: {e}")
            return {
                "error": True,
                "status": 500,
                "message": f"Unexpected integration error: {str(e)}",
                "details": str(e)
            }
