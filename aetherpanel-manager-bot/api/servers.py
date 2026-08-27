# AetherPanel Manager Bot
# Made by ZenseiBabe

from api.client import api_client

async def get_servers() -> dict:
    """Retrieves all servers from the real AetherPanel API."""
    return await api_client._request("GET", "/servers")

async def get_server(server_id: str) -> dict:
    """Retrieves detailed information of a single server from the API."""
    return await api_client._request("GET", f"/servers/{server_id}")

async def trigger_server_lifecycle(server_id: str, action: str) -> dict:
    """Sends start, stop, restart, or kill commands to a server."""
    return await api_client._request("POST", f"/servers/{server_id}/lifecycle", {"action": action})

async def get_server_console(server_id: str) -> dict:
    """Retrieves the recent console logs for the server."""
    return await api_client._request("GET", f"/servers/{server_id}/console")

async def send_server_command(server_id: str, command: str) -> dict:
    """Sends a raw console command to the running server."""
    return await api_client._request("POST", f"/servers/{server_id}/console", {"command": command})

async def delete_server(server_id: str) -> dict:
    """Deletes a server from AetherPanel."""
    return await api_client._request("DELETE", f"/servers/{server_id}/delete")

async def create_server(payload: dict) -> dict:
    """Triggers server creation through AetherPanel."""
    return await api_client._request("POST", "/servers/create", payload)

async def create_free_server(payload: dict) -> dict:
    """Triggers server creation on the free tier endpoint."""
    return await api_client._request("POST", "/servers/free", payload)
