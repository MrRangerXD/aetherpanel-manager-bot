# AetherPanel Manager Bot
# Made by ZenseiBabe

try:
    import discord
    from discord.ui import View, Button
    DISCORD_UI_AVAILABLE = True
except ImportError:
    DISCORD_UI_AVAILABLE = False

class ServerControlsViewDict:
    @staticmethod
    def get_components(server_id: str) -> list:
        return [
            {
                "type": "row",
                "buttons": [
                    {"label": "▶️ Start", "custom_id": f"btn_server_start_{server_id}", "style": "success"},
                    {"label": "⏹️ Stop", "custom_id": f"btn_server_stop_{server_id}", "style": "danger"},
                    {"label": "🔄 Restart", "custom_id": f"btn_server_restart_{server_id}", "style": "primary"},
                    {"label": "💀 Kill", "custom_id": f"btn_server_kill_{server_id}", "style": "danger"}
                ]
            },
            {
                "type": "row",
                "buttons": [
                    {"label": "📜 Console", "custom_id": f"btn_server_console_{server_id}", "style": "secondary"},
                    {"label": "💾 Backups", "custom_id": f"btn_server_backups_{server_id}", "style": "secondary"},
                    {"label": "📁 SFTP Info", "custom_id": f"btn_server_sftp_{server_id}", "style": "secondary"},
                    {"label": "⚡ Playit Info", "custom_id": f"btn_server_playit_{server_id}", "style": "secondary"}
                ]
            },
            {
                "type": "row",
                "buttons": [
                    {"label": "🗑️ Delete Server", "custom_id": f"btn_server_delete_prompt_{server_id}", "style": "danger"},
                    {"label": "◀️ Back to List", "custom_id": "btn_nav_servers", "style": "secondary"},
                    {"label": "🔃 Refresh Info", "custom_id": f"btn_server_details_{server_id}", "style": "primary"}
                ]
            }
        ]

    @staticmethod
    def get_console_components(server_id: str) -> list:
        return [
            {
                "type": "row",
                "buttons": [
                    {"label": "💻 Send Command", "custom_id": f"btn_server_cmd_modal_{server_id}", "style": "primary"},
                    {"label": "🔃 Refresh Output", "custom_id": f"btn_server_console_{server_id}", "style": "secondary"},
                    {"label": "◀️ Back to Server", "custom_id": f"btn_server_details_{server_id}", "style": "secondary"}
                ]
            }
        ]

    @staticmethod
    def get_backup_components(server_id: str) -> list:
        return [
            {
                "type": "row",
                "buttons": [
                    {"label": "➕ Create Backup", "custom_id": f"btn_backup_create_modal_{server_id}", "style": "success"},
                    {"label": "🔃 Refresh Backups", "custom_id": f"btn_server_backups_{server_id}", "style": "secondary"},
                    {"label": "◀️ Back to Server", "custom_id": f"btn_server_details_{server_id}", "style": "secondary"}
                ]
            }
        ]

    @staticmethod
    def get_confirmation_components(action_name: str, server_id: str) -> list:
        return [
            {
                "type": "row",
                "buttons": [
                    {"label": "Confirm Action", "custom_id": f"btn_server_confirm_{action_name}_{server_id}", "style": "danger"},
                    {"label": "Cancel", "custom_id": f"btn_server_details_{server_id}", "style": "secondary"}
                ]
            }
        ]

if DISCORD_UI_AVAILABLE:
    class DiscordServerControlsView(View):
        def __init__(self, server_id: str, timeout: int = 180):
            super().__init__(timeout=timeout)
            
            # Row 0: State controls
            self.add_item(Button(label="▶️ Start", custom_id=f"btn_server_start_{server_id}", style=discord.ButtonStyle.success, row=0))
            self.add_item(Button(label="⏹️ Stop", custom_id=f"btn_server_stop_{server_id}", style=discord.ButtonStyle.danger, row=0))
            self.add_item(Button(label="🔄 Restart", custom_id=f"btn_server_restart_{server_id}", style=discord.ButtonStyle.primary, row=0))
            self.add_item(Button(label="💀 Kill", custom_id=f"btn_server_kill_{server_id}", style=discord.ButtonStyle.danger, row=0))
            
            # Row 1: Operations
            self.add_item(Button(label="📜 Console", custom_id=f"btn_server_console_{server_id}", style=discord.ButtonStyle.secondary, row=1))
            self.add_item(Button(label="💾 Backups", custom_id=f"btn_server_backups_{server_id}", style=discord.ButtonStyle.secondary, row=1))
            self.add_item(Button(label="📁 SFTP Info", custom_id=f"btn_server_sftp_{server_id}", style=discord.ButtonStyle.secondary, row=1))
            self.add_item(Button(label="⚡ Playit Info", custom_id=f"btn_server_playit_{server_id}", style=discord.ButtonStyle.secondary, row=1))
            
            # Row 2: Danger zones
            self.add_item(Button(label="🗑️ Delete Server", custom_id=f"btn_server_delete_prompt_{server_id}", style=discord.ButtonStyle.danger, row=2))
            self.add_item(Button(label="◀️ Back to List", custom_id="btn_nav_servers", style=discord.ButtonStyle.secondary, row=2))
            self.add_item(Button(label="🔃 Refresh Info", custom_id=f"btn_server_details_{server_id}", style=discord.ButtonStyle.primary, row=2))
