# AetherPanel Manager Bot
# Made by ZenseiBabe

from api.client import api_client

async def get_admin_dashboard() -> dict:
    """Retrieves overall cluster statistics and server summaries."""
    return await api_client._request("GET", "/admin/dashboard")
