# AetherPanel Manager Bot
# Made by ZenseiBabe

from datetime import datetime
from api.servers import get_servers
from utils.watermark import apply_watermark

def generate_deploy_payload(node_id: str = None, server_type: str = None) -> dict:
    """
    Constructs the step-by-step interactive configuration prompt for deploying new virtual machines.
    """
    desc = (
        "## 🚀 Cloud Provisioning Engine\n"
        "Configure and deploy new virtual machine nodes instantly on AetherPanel nodes.\n\n"
        "**⚙️ Current Selection:**\n"
        f"└ Target Hardware Node: `{node_id or 'NOT_SELECTED'}`\n"
        f"└ Virtual Class Class: `{server_type or 'NOT_SELECTED'}`\n\n"
        "**🛠️ Step 1: Select Server Class & Hardware**\n"
        "Use the selection dropdowns or actions below to proceed with configuration."
    )

    embed = {
        "title": "🚀 Cluster Deployment Center",
        "description": desc,
        "color": 3066993, # Green
        "timestamp": datetime.utcnow().isoformat()
    }

    # Setup select dropdown options
    components = [
        {
            "type": "row",
            "select_menu": {
                "custom_id": "select_deploy_node",
                "placeholder": "Choose target compute Node...",
                "options": [
                    {"label": "Node-01 (APAC Standard)", "value": "node_01", "description": "High performance compute in SG region."},
                    {"label": "Node-02 (EU Standard)", "value": "node_02", "description": "High IOPS storage SSD nodes."}
                ]
            }
        },
        {
            "type": "row",
            "select_menu": {
                "custom_id": "select_deploy_type",
                "placeholder": "Choose server software type...",
                "options": [
                    {"label": "Minecraft Server (Paper/Purpur)", "value": "minecraft", "description": "Low memory latency game servers."},
                    {"label": "Discord Python/Node Bot", "value": "bot", "description": "Pre-configured systemd runtime environments."},
                    {"label": "Direct Database (PostgreSQL/Redis)", "value": "database", "description": "Highly available master cluster."}
                ]
            }
        },
        {
            "type": "row",
            "buttons": [
                {"label": "Configure Specs (Modal)", "custom_id": f"btn_deploy_config_modal_{node_id or 'node_01'}_{server_type or 'minecraft'}", "style": "success"},
                {"label": "Cancel Deployment", "custom_id": "btn_nav_servers", "style": "secondary"}
            ]
        }
    ]

    return {
        "embed": apply_watermark(embed),
        "components": components
    }

def generate_deploy_confirm_payload(name: str, node: str, srv_type: str, ram: str, cpu: str, disk: str) -> dict:
    """
    Shows a confirmation card summarizing specs before calling the API.
    """
    desc = (
        "## 🛠️ Confirm Virtual Node Specifications\n"
        "Please review your provisioning parameters carefully before launching.\n\n"
        f"**📋 Node Parameters:**\n"
        f"└ **Server Name:** `{name}`\n"
        f"└ **Hardware Target:** `{node.upper()}`\n"
        f"└ **Software Category:** `{srv_type.upper()}`\n"
        f"└ **Memory Allocated:** `{ram}`\n"
        f"└ **Compute Overheads:** `{cpu} Core`\n"
        f"└ **Storage Capacity:** `{disk}`\n\n"
        f"*Confirming triggers server provisioning via the REST API endpoint immediately.*"
    )

    embed = {
        "title": "🚀 Finalize Node Creation",
        "description": desc,
        "color": 3066993,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Build unique parameters for button execution
    param_str = f"{name}_{node}_{srv_type}_{ram}_{cpu}_{disk}".replace(" ", "%20")
    components = [
        {
            "type": "row",
            "buttons": [
                {"label": "Deploy Server", "custom_id": f"btn_deploy_execute_{param_str}", "style": "success"},
                {"label": "Cancel", "custom_id": "btn_nav_servers", "style": "secondary"}
            ]
        }
    ]

    return {
        "embed": apply_watermark(embed),
        "components": components
    }
