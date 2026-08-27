# AetherPanel Manager Bot
# Made by ZenseiBabe

from api.client import api_client

async def get_nodes() -> dict:
    """Retrieves list of active virtual nodes from the API."""
    return await api_client._request("GET", "/nodes")

async def get_node(node_id: str) -> dict:
    """Retrieves specific details of a single node."""
    return await api_client._request("GET", f"/nodes/{node_id}")

async def set_node_maintenance(node_id: str, maintenance: bool) -> dict:
    """Puts a node into or out of maintenance mode."""
    return await api_client._request("POST", f"/nodes/{node_id}", {"maintenance": maintenance})
