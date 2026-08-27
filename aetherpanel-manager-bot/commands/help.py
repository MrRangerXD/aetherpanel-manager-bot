# AetherPanel Manager Bot
# Made by ZenseiBabe

from datetime import datetime
from utils.watermark import apply_watermark
from views.help_views import HelpViewDict

def generate_help_payload(category: str = "main") -> dict:
    """
    Generates branded help system embed and buttons according to selected category.
    """
    category = category.lower()
    color = 3447003 # Blue
    title = "📖 AetherPanel Bot Manual"
    desc = ""

    if category == "main":
        desc = (
            "## Welcome to AetherPanel Manager Bot\n"
            "This interactive bot lets you control, monitor, and scale virtual servers, nodes, "
            "and billing credits on AetherPanel directly from Discord.\n\n"
            "### 🗂️ Manual Index\n"
            "Select one of the help sections using the controls below to read specialized manuals:\n"
            "* 🖥️ **Servers Help** — Manage virtual server power states, backups, and console endpoints.\n"
            "* 🌐 **Nodes Help** — Track active node resources and administrative overrides.\n"
            "* 💾 **Backups Help** — Handle backups lists, restorations, and snapshot creations.\n"
            "* 👤 **Users Help** — Inspect profile balances, map accounts, and review profiles.\n"
            "* 🚀 **Deploy Help** — Provision and scale cluster nodes instantly.\n"
            "* 🛡️ **Admin Help** — Manage suspensions, adjust finances, and review logs.\n"
            "* 📊 **System Help** — Read platform diagnostics and latencies."
        )
    elif category == "servers":
        title = "🖥️ Server Management Manual"
        desc = (
            "### Virtual Server Controls\n"
            "Standard commands let you control your server resources. Normal users can only manage servers they own.\n\n"
            "**Available Operations:**\n"
            "└ `/server list` — Page through active virtual machines.\n"
            "└ `/server info <id>` — View telemetry, specs, ownership, and current state.\n"
            "└ `/server start <id>` — Boot the physical server container.\n"
            "└ `/server stop <id>` — Initiate a safe graceful shutdown sequence.\n"
            "└ `/server restart <id>` — Perform a power reboot.\n"
            "└ `/server kill <id>` — Instantly terminate execution (may corrupt files).\n"
            "└ `/server console <id>` — Tail console log streams and send backend CLI entries.\n"
            "└ `/server command <id> <cmd>` — Send a CLI command directly inside the machine.\n"
            "└ `/server delete <id>` — Destroy the server instance completely (destructive)."
        )
    elif category == "nodes":
        title = "🌐 Node Management Manual"
        color = 10181046 # Purple
        desc = (
            "### Node Infrastructure Telemetry\n"
            "Admin-only capabilities to supervise cluster node hardware states, daemon heartbeats, and capacities.\n\n"
            "**Commands Map:**\n"
            "└ `/node list` — Browse all active cluster nodes.\n"
            "└ `/node info <id>` — Analyze real CPU/RAM overheads, port allocations, and versions.\n"
            "└ `/node status <id>` — Check ping latencies and agent health indicators.\n"
            "└ `/node maintenance <id> <true/false>` — Toggle maintenance mode to lock allocations.\n"
            "└ `/node servers <id>` — See virtual machines assigned to this node."
        )
    elif category == "backups":
        title = "💾 Backup Management Manual"
        desc = (
            "### Snapshot Backups Engine\n"
            "Easily preserve state records, database files, and maps safely inside offsite node vaults.\n\n"
            "**Operation Directives:**\n"
            "└ `/backup list <id>` — Retrieve list of backup snapshots on the server.\n"
            "└ `/backup create <id> [name]` — Provision a state snapshot.\n"
            "└ `/backup restore <id> <backup_id>` — Overwrite live disk with snapshot states.\n"
            "└ `/backup delete <id> <backup_id>` — Clean up disk usage by destroying old snapshots."
        )
    elif category == "users":
        title = "👤 User Management Manual"
        desc = (
            "### User Account Operations\n"
            "Track active developer profiles, map identifiers, and review transaction histories.\n\n"
            "**Directives:**\n"
            "└ `/user info <id>` — Show registered usernames, emails, roles, and credit ledgers.\n"
            "└ `/user servers <id>` — View all virtual machine nodes assigned to a user."
        )
    elif category == "deploy":
        title = "🚀 Server Provisioning Manual"
        color = 3066993 # Green
        desc = (
            "### Deployments & Scaling\n"
            "Authorized users can provision cloud instances through the REST API.\n\n"
            "**How to Deploy:**\n"
            "└ `/deploy` — Starts an interactive modal flow inside Discord.\n"
            "└ `/free` — Deploy a server instantly under the free credit allocation tier (if supported)."
        )
    elif category == "admin":
        title = "🛡️ Administration Overseer Guide"
        color = 15158332 # Red
        desc = (
            "### Operator Console Overrides\n"
            "Financial adjustment and suspension switches reserved strictly for system supervisors.\n\n"
            "**Overwatch Directives:**\n"
            "└ `/admin dashboard` — Full analytics overview of system assets, networks, and ratios.\n"
            "└ `/user suspend <id>` — Block user credentials from booting or logging into machines.\n"
            "└ `/user unsuspend <id>` — Lift suspend overrides.\n"
            "└ `/user credits <id> <add/deduct/set> <amount>` — Adjust ledger balances."
        )
    elif category == "system":
        title = "📊 Panel Diagnostic Controls"
        desc = (
            "### Diagnostic Health and Integrity\n"
            "Confirm that the bot can connect to the panel.\n\n"
            "**Diagnostics Map:**\n"
            "└ `/status` — View ping latencies, core gateway response rates, and system uptime."
        )

    embed = {
        "title": title,
        "description": desc,
        "color": color,
        "timestamp": datetime.utcnow().isoformat()
    }

    return {
        "embed": apply_watermark(embed),
        "components": HelpViewDict.get_components()
    }
