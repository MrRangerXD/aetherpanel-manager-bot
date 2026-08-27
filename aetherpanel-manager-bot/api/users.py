# AetherPanel Manager Bot
# Made by ZenseiBabe

from api.client import api_client

async def get_users() -> dict:
    """Retrieves all users from AetherPanel."""
    return await api_client._request("GET", "/users")

async def get_user(user_id: str) -> dict:
    """Retrieves details of a single user."""
    return await api_client._request("GET", f"/users/{user_id}")

async def adjust_user_credits(user_id: str, action: str, amount: float) -> dict:
    """Adds, deducts, or sets credit balance for a user's ledger."""
    return await api_client._request("POST", f"/users/{user_id}/credits", {"action": action, "amount": amount})

async def set_user_status(user_id: str, status: str) -> dict:
    """Suspends or unsuspends a user account."""
    return await api_client._request("POST", f"/users/{user_id}/status", {"status": status})
