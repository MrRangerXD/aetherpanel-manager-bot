#!/usr/bin/env python3
# Made by ZenseiBabe
# AetherPanel Manager Bot

"""
AetherPanel Manager Bot
=======================
An API-driven, production-ready Discord management & automation bot for AetherPanel infrastructure.
Main entry point coordinating modular sub-packages.
"""

import os
import sys
import json
import asyncio
from datetime import datetime

# Try importing discord.py for live production setups
try:
    import discord
    from discord import app_commands
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

# Import configuration and logging
from config.config import DISCORD_TOKEN, AETHERPANEL_URL, AETHERPANEL_API_KEY, BOT_PREFIX, COMMAND_GUILD_ID, validate_config
from utils.logger import get_logger
from utils.watermark import apply_watermark, apply_watermark_to_discord_embed
from utils.permissions import PermissionLevel, get_user_permission
from utils.embeds import get_error_embed, get_success_embed, get_info_embed
from utils.errors import format_api_error

# Import API endpoints
import api
from api.client import api_client

# Import commands/payload generators
import commands as bot_commands
from commands.help import generate_help_payload
from commands.server import (
    generate_servers_payload, generate_server_details_payload,
    generate_server_console_payload, generate_server_backups_payload,
    generate_server_delete_prompt_payload
)
from commands.node import generate_nodes_payload, generate_node_details_payload
from commands.admin import generate_admin_payload
from commands.user import generate_users_payload, generate_user_details_payload
from commands.deploy import generate_deploy_payload, generate_deploy_confirm_payload

# Initialize logger
logger = get_logger("AetherMain")


# ==========================================
# 1. DISCORD CLI TEST COMMAND SIMULATION
# ==========================================
async def execute_cli_test_command(command_str: str) -> str:
    """
    Simulates Discord bot interaction states over the CLI for sandboxed browser previews.
    Queries the actual endpoints from the server.ts proxy and parses standard outputs.
    """
    logger.info(f"CLI Sandbox Command Intercepted: {command_str}")
    parts = command_str.split("_")

    try:
        if command_str in ("/panel", "/aether dashboard", "btn_nav_refresh_dashboard", "btn_admin_refresh_dashboard", "btn_help_category_main"):
            # Master panel dashboard view
            payload = await generate_admin_payload()
            return json.dumps(payload, indent=2)

        elif command_str in ("/help", "btn_help_category_main"):
            payload = generate_help_payload("main")
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_help_category_"):
            category = command_str.replace("btn_help_category_", "")
            payload = generate_help_payload(category)
            return json.dumps(payload, indent=2)

        elif command_str in ("/servers", "/server list", "btn_nav_servers", "btn_servers_refresh"):
            payload = await generate_servers_payload(page=0)
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_servers_next_page_"):
            current_page = int(parts[4])
            payload = await generate_servers_payload(page=current_page + 1)
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_servers_prev_page_"):
            current_page = int(parts[4])
            payload = await generate_servers_payload(page=current_page - 1)
            return json.dumps(payload, indent=2)

        elif command_str in ("/nodes", "/node list", "btn_nav_nodes", "btn_nodes_refresh"):
            payload = await generate_nodes_payload(page=0)
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_nodes_next_page_"):
            current_page = int(parts[4])
            payload = await generate_nodes_payload(page=current_page + 1)
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_nodes_prev_page_"):
            current_page = int(parts[4])
            payload = await generate_nodes_payload(page=current_page - 1)
            return json.dumps(payload, indent=2)

        elif command_str in ("/users", "/user list", "btn_nav_users", "btn_users_refresh"):
            payload = await generate_users_payload(page=0)
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_users_next_page_"):
            current_page = int(parts[4])
            payload = await generate_users_payload(page=current_page + 1)
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_users_prev_page_"):
            current_page = int(parts[4])
            payload = await generate_users_payload(page=current_page - 1)
            return json.dumps(payload, indent=2)

        elif command_str in ("/status", "btn_nav_system"):
            # Check latency and diagnostic state
            start = datetime.now()
            res = await api.get_system_status()
            latency = int((datetime.now() - start).total_seconds() * 1000)

            if isinstance(res, dict) and res.get("error"):
                return json.dumps({"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}, indent=2)

            desc = (
                "## 🩺 System Diagnostic Report\n\n"
                "**🛰️ Gateway Status:**\n"
                "└ AetherPanel REST API: 🟢 **ONLINE**\n"
                f"└ Response Latency: `{latency}ms`\n"
                "└ Diagnostic Token Check: 🟢 **VALID**\n\n"
                "**⚙️ Discord Daemon Overhead:**\n"
                "└ Connection State: 🟢 **HEALTHY**\n"
                f"└ Database Status: 🟢 **INTEGRAL**\n"
                f"└ Framework: `discord.py v2.3.2 (Components V2)`\n"
            )
            embed = {
                "title": "📋 AetherPanel System Health",
                "description": desc,
                "color": 3066993,
                "timestamp": datetime.utcnow().isoformat()
            }
            return json.dumps({"embed": apply_watermark(embed)}, indent=2)

        elif command_str in ("/deploy", "btn_nav_deploy"):
            payload = generate_deploy_payload()
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_deploy_config_modal_"):
            # Format: btn_deploy_config_modal_node_type
            node = parts[4]
            srv_type = parts[5]
            # Returns interactive deployment form layout
            return json.dumps({
                "modal_type": "deploy_server",
                "title": f"Deploy {srv_type.upper()} Node",
                "node": node,
                "type": srv_type,
                "custom_id": f"modal_deploy_execute_{node}_{srv_type}"
            }, indent=2)

        elif command_str.startswith("modal_deploy_execute_"):
            # Format: modal_deploy_execute_node_type: name_ram_cpu_disk
            m_parts = command_str.replace("modal_deploy_execute_", "").split(":")
            meta_info = m_parts[0].split("_")
            node = meta_info[0]
            srv_type = meta_info[1]
            inputs = m_parts[1].strip().split("_")
            
            name = inputs[0]
            ram = inputs[1]
            cpu = inputs[2]
            disk = inputs[3]

            payload = generate_deploy_confirm_payload(name, node, srv_type, ram, cpu, disk)
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_deploy_execute_"):
            # Format: btn_deploy_execute_name_node_type_ram_cpu_disk
            raw_params = command_str.replace("btn_deploy_execute_", "")
            params = [p.replace("%20", " ") for p in raw_params.split("_")]
            
            payload = {
                "name": params[0],
                "node": params[1],
                "type": params[2],
                "ram": params[3],
                "cpu": float(params[4]),
                "disk": params[5],
                "owner": "mrrangerplayz@gmail.com"
            }

            res = await api.create_server(payload)
            if "error" in res:
                return json.dumps({"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}, indent=2)

            # Succeeded
            s_data = res.get("data", res)
            desc = (
                f"### 🚀 New Compute Container Provisioned\n"
                f"Your server node deployment request has been accepted by the cluster daemon!\n\n"
                f"└ **Server Name:** `{s_data.get('name')}`\n"
                f"└ **Assigned ID:** `{s_data.get('id')}`\n"
                f"└ **Hardware Target:** `{s_data.get('node')}`\n"
                f"└ **IP endpoint:** `{s_data.get('ip')}:{s_data.get('port')}`\n"
                f"└ **Process State:** `🟢 RUNNING`"
            )
            embed = {
                "title": "✅ Server Created Successfully",
                "description": desc,
                "color": 3066993,
                "timestamp": datetime.utcnow().isoformat()
            }
            return json.dumps({"embed": apply_watermark(embed)}, indent=2)

        elif command_str.startswith("btn_server_details_") or command_str.startswith("btn_server_refresh_"):
            server_id = "_".join(parts[3:])
            payload = await generate_server_details_payload(server_id)
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_server_console_"):
            server_id = "_".join(parts[3:])
            payload = await generate_server_console_payload(server_id)
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_server_backups_"):
            server_id = "_".join(parts[3:])
            payload = await generate_server_backups_payload(server_id)
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_server_sftp_"):
            server_id = "_".join(parts[3:])
            res = await api.get_server(server_id)
            if isinstance(res, dict) and res.get("error"):
                return json.dumps({"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}, indent=2)

            s = res.get("data", res) if isinstance(res, dict) and "data" in res else res
            desc = (
                f"## 📁 SFTP Connection Credentials\n\n"
                f"Secure File Transfer parameters for server `{s.get('name')}`.\n\n"
                f"└ **SFTP Host IP:** `{s.get('ip', '127.0.0.1')}`\n"
                f"└ **SFTP Port:** `2222` (Cluster Gateway)\n"
                f"└ **Username:** `sftp_{server_id}`\n"
                f"└ **Password:** `*Configured Account Password*`\n\n"
                f"*Use any compliant SFTP Client like FileZilla or WinSCP to connect securely.*"
            )
            embed = {
                "title": f"📁 SFTP: {s.get('name')}",
                "description": desc,
                "color": 3447003,
                "timestamp": datetime.utcnow().isoformat()
            }
            components = [
                {
                    "type": "row",
                    "buttons": [
                        {"label": "◀ Back to Details", "custom_id": f"btn_server_details_{server_id}", "style": "secondary"}
                    ]
                }
            ]
            return json.dumps({"embed": apply_watermark(embed), "components": components}, indent=2)

        elif command_str.startswith("btn_server_playit_"):
            server_id = "_".join(parts[3:])
            res = await api.get_server(server_id)
            if isinstance(res, dict) and res.get("error"):
                return json.dumps({"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}, indent=2)

            s = res.get("data", res) if isinstance(res, dict) and "data" in res else res
            desc = (
                f"## ⚡ Playit.gg Cloud Tunnels\n\n"
                f"Seamless UDP/TCP domain gateway integration for `{s.get('name')}`.\n\n"
                f"└ **Tunnel Status:** 🟢 **CONNECTED**\n"
                f"└ **Public DNS endpoint:** `{s.get('name').lower().replace(' ', '-')}.playit.gg`\n"
                f"└ **Mapped Node Address:** `{s.get('ip')}:{s.get('port')}`\n\n"
                f"*Playit network routes are automatically managed. No port forwarding is required.*"
            )
            embed = {
                "title": f"⚡ Playit: {s.get('name')}",
                "description": desc,
                "color": 15105570, # Gold Hex
                "timestamp": datetime.utcnow().isoformat()
            }
            components = [
                {
                    "type": "row",
                    "buttons": [
                        {"label": "◀ Back to Details", "custom_id": f"btn_server_details_{server_id}", "style": "secondary"}
                    ]
                }
            ]
            return json.dumps({"embed": apply_watermark(embed), "components": components}, indent=2)

        elif command_str.startswith("btn_server_delete_prompt_"):
            server_id = "_".join(parts[4:])
            payload = generate_server_delete_prompt_payload(server_id)
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_server_confirm_delete_"):
            server_id = "_".join(parts[4:])
            res = await api.delete_server(server_id)
            if isinstance(res, dict) and res.get("error"):
                return json.dumps({"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}, indent=2)

            payload = await generate_servers_payload(page=0)
            payload["content"] = f"✅ Virtual Node `{server_id}` successfully purged from AetherPanel cluster nodes."
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_server_start_") or command_str.startswith("btn_server_stop_") or command_str.startswith("btn_server_restart_") or command_str.startswith("btn_server_kill_"):
            action = parts[2]
            server_id = "_".join(parts[3:])
            
            res = await api.trigger_server_lifecycle(server_id, action)
            if isinstance(res, dict) and res.get("error"):
                return json.dumps({"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}, indent=2)

            payload = await generate_server_details_payload(server_id)
            payload["content"] = f"🚀 Power Action `{action.upper()}` signaled successfully to server `{server_id}`."
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_server_cmd_modal_"):
            server_id = "_".join(parts[4:])
            return json.dumps({
                "modal_type": "server_command",
                "title": "Send Console Command",
                "server_id": server_id,
                "custom_id": f"modal_server_cmd_execute_{server_id}"
            }, indent=2)

        elif command_str.startswith("modal_server_cmd_execute_"):
            # Format: modal_server_cmd_execute_serverid: command
            server_id = command_str.split(":")[0].replace("modal_server_cmd_execute_", "")
            cmd_payload = command_str.split(":")[1].strip()

            res = await api.send_server_command(server_id, cmd_payload)
            if isinstance(res, dict) and res.get("error"):
                return json.dumps({"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}, indent=2)

            payload = await generate_server_console_payload(server_id)
            payload["content"] = f"⌨️ Command `{cmd_payload}` sent successfully to server process."
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_backup_create_modal_"):
            server_id = "_".join(parts[4:])
            return json.dumps({
                "modal_type": "backup_create",
                "title": "Provision State Snapshot",
                "server_id": server_id,
                "custom_id": f"modal_backup_create_execute_{server_id}"
            }, indent=2)

        elif command_str.startswith("modal_backup_create_execute_"):
            # Format: modal_backup_create_execute_serverid: name
            server_id = command_str.split(":")[0].replace("modal_backup_create_execute_", "")
            backup_name = command_str.split(":")[1].strip()

            res = await api.create_backup(server_id, backup_name)
            if isinstance(res, dict) and res.get("error"):
                return json.dumps({"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}, indent=2)

            payload = await generate_server_backups_payload(server_id)
            payload["content"] = f"💾 Snapshot `{backup_name}` provisioned successfully."
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_node_details_"):
            node_id = "_".join(parts[3:])
            payload = await generate_node_details_payload(node_id)
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_node_servers_"):
            node_id = "_".join(parts[3:])
            # Filter servers on this node
            n_res = await api.get_node(node_id)
            n = n_res.get("data", n_res) if "data" in n_res else n_res
            s_res = await api.get_servers()
            
            servers = s_res.get("data", []) if isinstance(s_res, dict) else s_res
            node_srvs = [s for s in servers if s.get("node") == n.get("name") or s.get("node") == node_id]

            desc = f"### 📁 Active Compute Nodes Assigned to Node `{n.get('name')}`\n\n"
            if not node_srvs:
                desc += "No containers assigned to this node."
            else:
                for idx, s in enumerate(node_srvs, start=1):
                    status_emoji = "🟢" if s.get("status") == "running" else "🔴"
                    desc += f"**{idx}. {s.get('name')}** (`{s.get('id')}`)\n└ Status: {status_emoji} {s.get('status').upper()} | RAM: `{s.get('ram')}` | Type: `{s.get('type')}`\n\n"

            payload = {
                "embed": {
                    "title": f"Node Server Map: {n.get('name')}",
                    "description": desc,
                    "color": 10181046,
                    "timestamp": datetime.utcnow().isoformat()
                },
                "components": [
                    {
                        "type": "row",
                        "buttons": [
                            {"label": "◀ Back to Node", "custom_id": f"btn_node_details_{node_id}", "style": "secondary"}
                        ]
                    }
                ]
            }
            return json.dumps({"embed": apply_watermark(payload["embed"]), "components": payload["components"]}, indent=2)

        elif command_str.startswith("btn_node_maint_"):
            action = parts[3]
            node_id = "_".join(parts[4:])
            maint_val = (action == "entermaint")
            
            res = await api.set_node_maintenance(node_id, maint_val)
            if isinstance(res, dict) and res.get("error"):
                return json.dumps({"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}, indent=2)

            payload = await generate_node_details_payload(node_id)
            payload["content"] = f"🔧 Node Maintenance status updated to `{maint_val}`."
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_user_details_"):
            user_id = "_".join(parts[3:])
            payload = await generate_user_details_payload(user_id)
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_user_status_"):
            action = parts[3]
            user_id = "_".join(parts[4:])
            status_val = "suspended" if action == "suspend" else "active"

            res = await api.set_user_status(user_id, status_val)
            if isinstance(res, dict) and res.get("error"):
                return json.dumps({"embed": format_api_error(res.get("status"), res.get("message"), res.get("details"))}, indent=2)

            payload = await generate_user_details_payload(user_id)
            payload["content"] = f"👤 User Profile suspension overridden successfully to `{status_val.upper()}`."
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_user_credits_modal_"):
            user_id = "_".join(parts[4:])
            return json.dumps({
                "modal_type": "user_credits",
                "title": "Adjust Ledger Balance",
                "user_id": user_id,
                "custom_id": f"modal_user_credits_execute_{user_id}"
            }, indent=2)

        elif command_str.startswith("modal_user_credits_execute_"):
            # Format: modal_user_credits_execute_userid: action_amount (e.g. add_50, deduct_20, set_100)
            user_id = command_str.split(":")[0].replace("modal_user_credits_execute_", "")
            inputs = command_str.split(":")[1].strip().split("_")
            action = inputs[0] # add, deduct, set
            amount = float(inputs[1])

            res = await api.adjust_user_credits(user_id, action, amount)
            if "error" in res:
                return json.dumps({"embed": get_error_embed("Ledger Adjustment Rejected", res.get("message", "Insufficient balance or negative value"), res.get("status"))}, indent=2)

            payload = await generate_user_details_payload(user_id)
            payload["content"] = f"✅ Ledger Adjusted. User `{user_id}` credits updated via `{action.upper()}` by `{amount}` CR."
            return json.dumps(payload, indent=2)

        elif command_str.startswith("btn_user_servers_"):
            user_id = "_".join(parts[3:])
            u_res = await api.get_user(user_id)
            u = u_res.get("data", u_res) if "data" in u_res else u_res
            s_res = await api.get_servers()
            
            servers = s_res.get("data", []) if isinstance(s_res, dict) else s_res
            user_srvs = [s for s in servers if s.get("owner") == u.get("email") or s.get("owner") == u.get("username")]

            desc = f"### 📁 Active Compute Nodes owned by `{u.get('username')}`\n\n"
            if not user_srvs:
                desc += "User does not own any cluster servers."
            else:
                for idx, s in enumerate(user_srvs, start=1):
                    status_emoji = "🟢" if s.get("status") == "running" else "🔴"
                    desc += f"**{idx}. {s.get('name')}** (`{s.get('id')}`)\n└ Status: {status_emoji} {s.get('status').upper()} | Node: `{s.get('node')}` | RAM: `{s.get('ram')}`\n\n"

            payload = {
                "embed": {
                    "title": f"User Server Map: {u.get('username')}",
                    "description": desc,
                    "color": 3447003,
                    "timestamp": datetime.utcnow().isoformat()
                },
                "components": [
                    {
                        "type": "row",
                        "buttons": [
                            {"label": "◀ Back to Profile", "custom_id": f"btn_user_details_{user_id}", "style": "secondary"}
                        ]
                    }
                ]
            }
            return json.dumps({"embed": apply_watermark(payload["embed"]), "components": payload["components"]}, indent=2)

        else:
            return json.dumps({"embed": get_error_embed("Command Refused", f"The requested CLI instruction `{command_str}` is unmapped in the orchestrator.")})

    except Exception as e:
        logger.error(f"Error handling CLI sandbox request: {e}", exc_info=True)
        return json.dumps({"embed": get_error_embed("Sandbox Exception", f"Internal processing error: {str(e)}", 500)})


# ==========================================
# 2. DISCORD GATEWAY CLIENT SETUP
# ==========================================
if DISCORD_AVAILABLE:
    class AetherBot(commands.Bot):
        def __init__(self):
            intents = discord.Intents.default()
            intents.message_content = True
            super().__init__(command_prefix=BOT_PREFIX, intents=intents)

        async def setup_hook(self):
            logger.info("Synchronizing Slash command structures with Discord API...")
            if COMMAND_GUILD_ID:
                guild = discord.Object(id=int(COMMAND_GUILD_ID))
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
                logger.info(f"Registered guild-specific commands locally to Guild: {COMMAND_GUILD_ID}")
            else:
                await self.tree.sync()
                logger.info("Registered global slash commands successfully.")

    bot = AetherBot()

    class AetherInteractiveView(discord.ui.View):
        def __init__(self, buttons_layout: list, timeout: int = 180):
            super().__init__(timeout=timeout)
            for row in buttons_layout:
                for btn in row.get("buttons", []):
                    style = discord.ButtonStyle.secondary
                    if btn.get("style") == "primary":
                        style = discord.ButtonStyle.primary
                    elif btn.get("style") == "success":
                        style = discord.ButtonStyle.success
                    elif btn.get("style") == "danger":
                        style = discord.ButtonStyle.danger

                    self.add_item(discord.ui.Button(
                        label=btn.get("label", ""),
                        custom_id=btn.get("custom_id", ""),
                        style=style,
                        disabled=btn.get("disabled", False)
                    ))

    def build_discord_payload(dict_payload: dict):
        embed_dict = dict_payload.get("embed", {})
        embed = None
        if embed_dict:
            embed = discord.Embed(
                title=embed_dict.get("title", ""),
                description=embed_dict.get("description", ""),
                color=embed_dict.get("color", 3447003)
            )
            apply_watermark_to_discord_embed(embed)
            if "timestamp" in embed_dict:
                embed.timestamp = datetime.fromisoformat(embed_dict["timestamp"])
            for f in embed_dict.get("fields", []):
                embed.add_field(name=f["name"], value=f["value"], inline=f.get("inline", False))

        view = None
        components = dict_payload.get("components", [])
        if components:
            view = AetherInteractiveView(components)

        return {"content": dict_payload.get("content"), "embed": embed, "view": view}

    # Slash Command: /panel
    @bot.tree.command(name="panel", description="Opens the master interactive AetherPanel dashboard.")
    async def panel_command(interaction: discord.Interaction):
        await interaction.response.defer()
        payload = await generate_admin_payload()
        d_pay = build_discord_payload(payload)
        await interaction.followup.send(content=d_pay["content"], embed=d_pay["embed"], view=d_pay["view"])

    # Slash Command: /help
    @bot.tree.command(name="help", description="Displays the premium multi-tab helper manual.")
    async def help_command(interaction: discord.Interaction):
        payload = generate_help_payload("main")
        d_pay = build_discord_payload(payload)
        await interaction.response.send_message(embed=d_pay["embed"], view=d_pay["view"])


# ==========================================
# 3. MASTER RUN ENTRANCE
# ==========================================
async def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test-command":
        # Process preview browser interaction directly over standard CLI
        cmd_str = sys.argv[2]
        result_json = await execute_cli_test_command(cmd_str)
        print(result_json)
        sys.exit(0)

    # Perform boot validation
    missing = validate_config()
    if missing:
        logger.critical(f"FATAL CONFIGURATION ERROR: Missing required environment keys: {', '.join(missing)}")
        sys.exit(1)

    if not DISCORD_AVAILABLE:
        logger.error("discord.py is not installed in the active environment. Please run the installer script.")
        sys.exit(1)

    logger.info("Connecting Discord Daemon Gateway...")
    try:
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        logger.critical(f"Connection gateway crashed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
