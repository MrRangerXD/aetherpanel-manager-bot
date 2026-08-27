# AetherPanel Manager Bot
# Made by ZenseiBabe

try:
    import discord
    from discord.ui import View, Button
    DISCORD_UI_AVAILABLE = True
except ImportError:
    DISCORD_UI_AVAILABLE = False

class NodeControlsViewDict:
    @staticmethod
    def get_components(node_id: str, is_maintenance: bool = False) -> list:
        maint_label = "🔧 Exit Maintenance" if is_maintenance else "🔧 Enter Maintenance"
        maint_style = "success" if is_maintenance else "danger"
        maint_action = "exitmaint" if is_maintenance else "entermaint"

        return [
            {
                "type": "row",
                "buttons": [
                    {"label": "📁 View Servers", "custom_id": f"btn_node_servers_{node_id}", "style": "primary"},
                    {"label": maint_label, "custom_id": f"btn_node_maint_{maint_action}_{node_id}", "style": maint_style},
                    {"label": "🔃 Refresh Telemetry", "custom_id": f"btn_node_details_{node_id}", "style": "primary"}
                ]
            },
            {
                "type": "row",
                "buttons": [
                    {"label": "◀️ Back to Nodes", "custom_id": "btn_nav_nodes", "style": "secondary"}
                ]
            }
        ]

if DISCORD_UI_AVAILABLE:
    class DiscordNodeControlsView(View):
        def __init__(self, node_id: str, is_maintenance: bool = False, timeout: int = 180):
            super().__init__(timeout=timeout)
            maint_label = "🔧 Exit Maintenance" if is_maintenance else "🔧 Enter Maintenance"
            maint_style = discord.ButtonStyle.success if is_maintenance else discord.ButtonStyle.danger
            maint_action = "exitmaint" if is_maintenance else "entermaint"

            self.add_item(Button(label="📁 View Servers", custom_id=f"btn_node_servers_{node_id}", style=discord.ButtonStyle.primary, row=0))
            self.add_item(Button(label=maint_label, custom_id=f"btn_node_maint_{maint_action}_{node_id}", style=maint_style, row=0))
            self.add_item(Button(label="🔃 Refresh Telemetry", custom_id=f"btn_node_details_{node_id}", style=discord.ButtonStyle.primary, row=0))
            self.add_item(Button(label="◀️ Back to Nodes", custom_id="btn_nav_nodes", style=discord.ButtonStyle.secondary, row=1))
