# AetherPanel Manager Bot
# Made by ZenseiBabe

import math
from datetime import datetime
from api.servers import get_servers, get_server, get_server_console
from api.backups import get_backups
from utils.embeds import get_error_embed
from utils.errors import format_api_error
from utils.watermark import apply_watermark
from views.pagination import PaginatedViewDict
from views.server_views import ServerControlsViewDict

async def generate_servers_payload(page: int = 0) -> dict:
    """
    Retrieves real-time virtual servers from AetherPanel and formats a paginated Discord payload.
    """
    res = await get_servers()
    if isinstance(res, dict) and res.get("error"):
        return {"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}

    # Extract server list
    servers = res.get("data", []) if isinstance(res, dict) else res
    if not isinstance(servers, list):
        servers = []

    if not servers:
        embed = {
            "title": "🖥️ AetherPanel Virtual Servers",
            "description": "### 📁 Active Compute Nodes\nNo virtual machine deployments exist on this AetherPanel account yet.",
            "color": 3447003,
            "timestamp": datetime.utcnow().isoformat()
        }
        return {"embed": apply_watermark(embed)}

    # Page size: 5 servers
    page_size = 5
    total_pages = max(1, math.ceil(len(servers) / page_size))
    page = max(0, min(page, total_pages - 1))

    start_idx = page * page_size
    end_idx = start_idx + page_size
    paged_servers = servers[start_idx:end_idx]

    desc = "### 📁 Active Compute Nodes\nSelect a server to view detailed diagnostics and trigger state shifts.\n\n"
    for s in paged_servers:
        srv_id = s.get("id", "N/A")
        name = s.get("name", "Unnamed Node")
        node = s.get("node", "Node-01")
        srv_type = s.get("type", "Docker Container")
        status = s.get("status", "unknown").lower()
        ram = s.get("ram", "N/A")

        status_emoji = "🟢" if status == "running" else "🔴" if status in ("offline", "stopped") else "🟡"
        desc += f"**{status_emoji} {name}** (`{srv_id}`)\n└ Node: `{node}` | Resource: `{ram}` | Class: `{srv_type.upper()}` | State: `{status.upper()}`\n\n"

    embed = {
        "title": f"🖥️ AetherPanel Servers (Total: {len(servers)})",
        "description": desc,
        "color": 3447003,
        "timestamp": datetime.utcnow().isoformat()
    }

    return {
        "embed": apply_watermark(embed),
        "components": PaginatedViewDict.get_components(page, total_pages, "servers")
    }

async def generate_server_details_payload(server_id: str) -> dict:
    """
    Retrieves a single server's telemetry metrics and configurations.
    """
    res = await get_server(server_id)
    if isinstance(res, dict) and res.get("error"):
        return {"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}

    s = res.get("data", res) if isinstance(res, dict) and "data" in res else res
    if not isinstance(s, dict) or not s:
        return {"embed": get_error_embed("Telemetry Refused", f"Failed to parse server metadata for ID `{server_id}`.")}

    name = s.get("name", "Virtual Container")
    status = s.get("status", "offline").lower()
    owner = s.get("owner", "System Admin")
    node = s.get("node", "Default-Node")
    srv_type = s.get("type", "Docker")
    ip = s.get("ip", "127.0.0.1")
    port = s.get("port", "25565")

    # Resource metrics mapping
    cpu = s.get("cpu", "N/A")
    if cpu != "N/A" and isinstance(cpu, (int, float)):
        cpu = f"{cpu}%"
    ram = s.get("ram", "N/A")
    disk = s.get("disk", "N/A")
    uptime = s.get("uptime", "N/A")

    status_emoji = "🟢" if status == "running" else "🔴" if status in ("offline", "stopped") else "🟡"

    desc = (
        f"## {status_emoji} {name} Status Metrics\n\n"
        f"**📋 Identity Profile:**\n"
        f"└ **Server ID:** `{server_id}`\n"
        f"└ **Identity Class:** `{srv_type.upper()}`\n"
        f"└ **Owner Email:** `{owner}`\n"
        f"└ **Target Allocation:** `{ip}:{port}`\n\n"
        f"**⚡ Telemetry Overheads:**\n"
        f"└ **CPU Compute:** `{cpu}`\n"
        f"└ **RAM Allocation:** `{ram}`\n"
        f"└ **Storage Threshold:** `{disk}`\n"
        f"└ **Process State:** `{status.upper()}`\n"
        f"└ **Uptime:** `{uptime}`\n"
        f"└ **Cluster Host:** `{node}`\n"
    )

    embed = {
        "title": f"🖥️ Terminal Control: {name}",
        "description": desc,
        "color": 3066993 if status == "running" else 15158332 if status in ("offline", "stopped") else 15105570,
        "timestamp": datetime.utcnow().isoformat()
    }

    return {
        "embed": apply_watermark(embed),
        "components": ServerControlsViewDict.get_components(server_id)
    }

async def generate_server_console_payload(server_id: str) -> dict:
    """
    Fetches real console history lines for the designated server.
    """
    res = await get_server_console(server_id)
    if isinstance(res, dict) and res.get("error"):
        return {"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}

    # Extract logs list
    logs = res.get("data", []) if isinstance(res, dict) else res
    if "logs" in res:
        logs = res["logs"]

    if isinstance(logs, list):
        log_str = "\n".join(logs)
    elif isinstance(logs, str):
        log_str = logs
    else:
        log_str = "No console diagnostics returned from AetherPanel API."

    # Discord message limits handling (max 2000 chars total, so truncate logs)
    if len(log_str) > 1200:
        log_str = "..." + log_str[-1200:]

    desc = (
        f"### 📜 Interactive Console: `{server_id}`\n"
        f"To send input keys into the active machine container process, click the **Send Command** button below.\n"
        f"```bash\n"
        f"{log_str or 'Waiting for logs...'}\n"
        f"```"
    )

    embed = {
        "title": "🖥️ Process Output Stream",
        "description": desc,
        "color": 3447003,
        "timestamp": datetime.utcnow().isoformat()
    }

    return {
        "embed": apply_watermark(embed),
        "components": ServerControlsViewDict.get_console_components(server_id)
    }

async def generate_server_backups_payload(server_id: str) -> dict:
    """
    Fetches active backups for the server.
    """
    res = await get_backups(server_id)
    if isinstance(res, dict) and res.get("error"):
        return {"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}

    backups = res.get("data", []) if isinstance(res, dict) else res
    if not isinstance(backups, list):
        backups = []

    desc = f"## 💾 Active Backups for `{server_id}`\n"
    if not backups:
        desc += "\n*No snapshot backups exist for this instance. Create one below to secure your files.*"
    else:
        desc += "\n"
        for idx, b in enumerate(backups, start=1):
            b_id = b.get("id", "N/A")
            name = b.get("name") or f"backup_snapshot_{idx}"
            size = b.get("size", "N/A")
            created = b.get("created_at") or b.get("created", "N/A")
            desc += f"**{idx}. {name}** (`{b_id}`)\n└ Size: `{size}` | Created: `{created}`\n\n"

    embed = {
        "title": "💾 Snapshot Backup Manager",
        "description": desc,
        "color": 10181046, # Purple
        "timestamp": datetime.utcnow().isoformat()
    }

    return {
        "embed": apply_watermark(embed),
        "components": ServerControlsViewDict.get_backup_components(server_id)
    }

def generate_server_delete_prompt_payload(server_id: str) -> dict:
    """
    Presents a scary delete confirmation block.
    """
    desc = (
        f"### ⚠️ CRITICAL DESTRUCTIVE OVERRIDE WARNING\n"
        f"Are you absolutely certain you want to destroy the server node `{server_id}`?\n\n"
        f"**This action will permanently delete:**\n"
        f"└ Docker containers and runtime processes.\n"
        f"└ All files on disk (configuration, binaries, mods, data).\n"
        f"└ Associated database records and snapshot vaults.\n\n"
        f"*This operation cannot be undone. Confirming sends a physical deletion request to the node daemon.*"
    )

    embed = {
        "title": f"💣 Nuclear Option Confirmation: {server_id}",
        "description": desc,
        "color": 15158332, # Red
        "timestamp": datetime.utcnow().isoformat()
    }

    return {
        "embed": apply_watermark(embed),
        "components": ServerControlsViewDict.get_confirmation_components("delete", server_id)
    }
