# AetherPanel Manager Bot
# Made by ZenseiBabe

from api.client import api_client

async def get_backups(server_id: str) -> dict:
    """Retrieves list of active backups for a specific server."""
    return await api_client._request("GET", f"/servers/{server_id}/backups")

async def create_backup(server_id: str, name: str = None) -> dict:
    """Creates a new snapshot backup for the specified server."""
    return await api_client._request("POST", f"/servers/{server_id}/backups", {"name": name or ""})

async def restore_backup(server_id: str, backup_id: str) -> dict:
    """Restores the server status to a specified backup snapshot."""
    return await api_client._request("POST", f"/servers/{server_id}/backups/{backup_id}/restore")

async def delete_backup(server_id: str, backup_id: str) -> dict:
    """Permanently deletes a backup snapshot from the node store."""
    return await api_client._request("DELETE", f"/servers/{server_id}/backups/{backup_id}")
