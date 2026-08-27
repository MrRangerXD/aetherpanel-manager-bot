# AetherPanel Manager Bot
# Made by ZenseiBabe

from api.client import api_client

async def get_system_status() -> dict:
    """Performs a diagnostic check against the panel's main health route."""
    return await api_client._request("GET", "/health")
