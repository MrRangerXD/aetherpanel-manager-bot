# AetherPanel Manager Bot
# Made by ZenseiBabe

from datetime import datetime
from api.admin import get_admin_dashboard
from utils.errors import format_api_error
from utils.watermark import apply_watermark
from views.admin_views import AdminDashboardViewDict

async def generate_admin_payload() -> dict:
    """
    Fetches system-wide administrative statistics from AetherPanel and formats a dashboard.
    """
    res = await get_admin_dashboard()
    if isinstance(res, dict) and res.get("error"):
        return {"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}

    stats = res.get("data", res) if isinstance(res, dict) and "data" in res else res
    if not isinstance(stats, dict):
        stats = {}

    total_users = stats.get("total_users", 0)
    active_users = stats.get("active_users", total_users)
    total_servers = stats.get("total_servers", 0)
    running_servers = stats.get("running_servers", 0)
    total_nodes = stats.get("total_nodes", 0)
    active_nodes = stats.get("active_nodes", total_nodes)
    global_cpu = stats.get("global_cpu", "N/A")
    global_ram = stats.get("global_ram", "N/A")

    desc = (
        "## 🛡️ Operator Dashboard Overview\n"
        "System wide capacity overview, resources, and developer allocations.\n\n"
        "**👥 Developer Accounts Profile:**\n"
        f"└ Total Users: `{total_users}` | Active: `{active_users}`\n\n"
        "**🖥️ Active Compute Instances:**\n"
        f"└ Total Servers: `{total_servers}` | Online: `{running_servers}`\n\n"
        "**🌐 Physical Hardware Nodes:**\n"
        f"└ Total Nodes: `{total_nodes}` | Active: `{active_nodes}`\n\n"
        "**⚡ Global Hardware Utilization Ratio:**\n"
        f"└ Cluster Core CPU Usage: `{global_cpu}`\n"
        f"└ Cluster Allocated memory: `{global_ram}`\n"
    )

    embed = {
        "title": "🛡️ AetherPanel Operator Center",
        "description": desc,
        "color": 15158332, # Red Hex
        "timestamp": datetime.utcnow().isoformat()
    }

    return {
        "embed": apply_watermark(embed),
        "components": AdminDashboardViewDict.get_components()
    }
