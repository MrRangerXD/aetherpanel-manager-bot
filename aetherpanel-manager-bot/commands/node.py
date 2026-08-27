# AetherPanel Manager Bot
# Made by ZenseiBabe

import math
from datetime import datetime
from api.nodes import get_nodes, get_node
from utils.errors import format_api_error
from utils.embeds import get_error_embed
from utils.watermark import apply_watermark
from views.pagination import PaginatedViewDict
from views.node_views import NodeControlsViewDict

async def generate_nodes_payload(page: int = 0) -> dict:
    """
    Fetches cluster nodes from AetherPanel and formats a paginated Discord payload.
    """
    res = await get_nodes()
    if isinstance(res, dict) and res.get("error"):
        return {"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}

    nodes = res.get("data", []) if isinstance(res, dict) else res
    if not isinstance(nodes, list):
        nodes = []

    if not nodes:
        embed = {
            "title": "🌐 AetherPanel Cluster Nodes",
            "description": "### 📡 Active Nodes Telemetry\nNo physical cluster nodes exist on this AetherPanel account yet.",
            "color": 10181046,
            "timestamp": datetime.utcnow().isoformat()
        }
        return {"embed": apply_watermark(embed)}

    # Page size: 5 nodes
    page_size = 5
    total_pages = max(1, math.ceil(len(nodes) / page_size))
    page = max(0, min(page, total_pages - 1))

    start_idx = page * page_size
    end_idx = start_idx + page_size
    paged_nodes = nodes[start_idx:end_idx]

    desc = "### 📡 Active Cluster Nodes Telemetry\nSelect a node to inspect system specifications and active container counts.\n\n"
    for n in paged_nodes:
        n_id = n.get("id", "N/A")
        name = n.get("name", "Unnamed Node")
        host = n.get("host", "127.0.0.1")
        status = n.get("status", "unknown").lower()
        active_containers = n.get("servers_count", 0)

        status_emoji = "🟢" if status in ("online", "active") else "🔴"
        desc += f"**{status_emoji} {name}** (`{n_id}`)\n└ Endpoint: `{host}` | Containers: `{active_containers}` | State: `{status.upper()}`\n\n"

    embed = {
        "title": f"🌐 Cluster Nodes (Total: {len(nodes)})",
        "description": desc,
        "color": 10181046,
        "timestamp": datetime.utcnow().isoformat()
    }

    return {
        "embed": apply_watermark(embed),
        "components": PaginatedViewDict.get_components(page, total_pages, "nodes")
    }

async def generate_node_details_payload(node_id: str) -> dict:
    """
    Fetches comprehensive diagnostic analytics for a specific physical cluster node.
    """
    res = await get_node(node_id)
    if isinstance(res, dict) and res.get("error"):
        return {"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}

    n = res.get("data", res) if isinstance(res, dict) and "data" in res else res
    if not isinstance(n, dict) or not n:
        return {"embed": get_error_embed("Telemetry Refused", f"Failed to parse node payload for ID `{node_id}`.")}

    name = n.get("name", "Physical Node")
    status = n.get("status", "offline").lower()
    host = n.get("host", "127.0.0.1")
    port = n.get("port", "8080")
    cpu = n.get("cpu", "0")
    if cpu != "N/A" and isinstance(cpu, (int, float)):
        cpu = f"{cpu}%"
    ram = n.get("ram", "N/A")
    disk = n.get("disk", "N/A")
    servers_count = n.get("servers_count", 0)
    maintenance = n.get("maintenance", False)
    agent_version = n.get("agent_version", "1.4.2")

    status_emoji = "🟢" if status in ("online", "active") else "🔴"
    if maintenance:
        status_emoji = "🟡"
        status = "maintenance"

    desc = (
        f"## {status_emoji} Node Terminal: {name}\n\n"
        f"**📋 Node Profile:**\n"
        f"└ **Node ID:** `{node_id}`\n"
        f"└ **Daemon Host:** `{host}:{port}`\n"
        f"└ **Agent Version:** `v{agent_version}`\n\n"
        f"**📊 Hardware Overheads:**\n"
        f"└ **Node CPU:** `{cpu}`\n"
        f"└ **Memory Allocated:** `{ram}`\n"
        f"└ **Disk Space:** `{disk}`\n"
        f"└ **Active Servers:** `{servers_count}`\n"
        f"└ **Operational State:** `{status.upper()}`\n"
    )

    embed = {
        "title": f"🌐 Node Diagnostics: {name}",
        "description": desc,
        "color": 3066993 if status in ("online", "active") else 15105570 if status == "maintenance" else 15158332,
        "timestamp": datetime.utcnow().isoformat()
    }

    return {
        "embed": apply_watermark(embed),
        "components": NodeControlsViewDict.get_components(node_id, is_maintenance=maintenance)
    }
