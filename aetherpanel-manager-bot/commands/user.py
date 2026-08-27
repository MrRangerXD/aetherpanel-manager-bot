# AetherPanel Manager Bot
# Made by ZenseiBabe

import math
from datetime import datetime
from api.users import get_users, get_user
from utils.errors import format_api_error
from utils.embeds import get_error_embed
from utils.watermark import apply_watermark
from views.pagination import PaginatedViewDict
from views.admin_views import AdminDashboardViewDict

async def generate_users_payload(page: int = 0) -> dict:
    """
    Fetches registered developer user accounts and pages through them.
    """
    res = await get_users()
    if isinstance(res, dict) and res.get("error"):
        return {"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}

    users = res.get("data", []) if isinstance(res, dict) else res
    if not isinstance(users, list):
        users = []

    if not users:
        embed = {
            "title": "👥 AetherPanel Registered Accounts",
            "description": "### 📂 Active Profiles\nNo accounts currently registered on this AetherPanel instance.",
            "color": 3447003,
            "timestamp": datetime.utcnow().isoformat()
        }
        return {"embed": apply_watermark(embed)}

    # Page size: 5 profiles
    page_size = 5
    total_pages = max(1, math.ceil(len(users) / page_size))
    page = max(0, min(page, total_pages - 1))

    start_idx = page * page_size
    end_idx = start_idx + page_size
    paged_users = users[start_idx:end_idx]

    desc = "### 📂 Active Developer Profiles\nSelect a user below to adjust credit ledgers, view server topologies, or toggle suspensions.\n\n"
    for u in paged_users:
        u_id = u.get("id", "N/A")
        username = u.get("username", "Unnamed User")
        email = u.get("email", "N/A")
        credits = u.get("credits", 0.0)
        status = u.get("status", "active").lower()

        status_emoji = "🟢" if status == "active" else "🔴"
        desc += f"**{status_emoji} {username}** (`{u_id}`)\n└ Email: `{email}` | Ledger Balance: `{credits} CR` | Status: `{status.upper()}`\n\n"

    embed = {
        "title": f"👥 Developer Profiles (Total: {len(users)})",
        "description": desc,
        "color": 3447003,
        "timestamp": datetime.utcnow().isoformat()
    }

    return {
        "embed": apply_watermark(embed),
        "components": PaginatedViewDict.get_components(page, total_pages, "users")
    }

async def generate_user_details_payload(user_id: str) -> dict:
    """
    Displays comprehensive financial ledger details and controls for a user profile.
    """
    res = await get_user(user_id)
    if isinstance(res, dict) and res.get("error"):
        return {"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}

    u = res.get("data", res) if isinstance(res, dict) and "data" in res else res
    if not isinstance(u, dict) or not u:
        return {"embed": get_error_embed("Access Refused", f"Failed to parse user profile payload for ID `{user_id}`.")}

    username = u.get("username", "Developer Profile")
    email = u.get("email", "N/A")
    credits = u.get("credits", 0.0)
    status = u.get("status", "active").lower()
    created_at = u.get("created_at") or u.get("created", "N/A")
    role = u.get("role", "User").upper()

    status_emoji = "🟢" if status == "active" else "🔴"

    desc = (
        f"## {status_emoji} Identity Node Card: {username}\n\n"
        f"**📋 Profile Specifications:**\n"
        f"└ **User ID:** `{user_id}`\n"
        f"└ **Primary Email:** `{email}`\n"
        f"└ **Authorized RBAC Class:** `{role}`\n"
        f"└ **Registration Stamp:** `{created_at}`\n\n"
        f"**💳 Financial Ledger Ledger:**\n"
        f"└ **Available Balance:** `{credits} Credits`\n"
        f"└ **Ledger Status:** `{status.upper()}`\n"
    )

    embed = {
        "title": f"👤 Profile Node Profile: {username}",
        "description": desc,
        "color": 3066993 if status == "active" else 15158332,
        "timestamp": datetime.utcnow().isoformat()
    }

    return {
        "embed": apply_watermark(embed),
        "components": AdminDashboardViewDict.get_user_controls(user_id, is_suspended=(status == "suspended"))
    }
