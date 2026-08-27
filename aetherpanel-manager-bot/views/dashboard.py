# AetherPanel Manager Bot
# Made by ZenseiBabe

try:
    import discord
    from discord.ui import View, Button
    DISCORD_UI_AVAILABLE = True
except ImportError:
    DISCORD_UI_AVAILABLE = False

class DashboardViewDict:
    @staticmethod
    def get_components() -> list:
        return [
            {
                "type": "row",
                "buttons": [
                    {"label": "🖥️ Servers", "custom_id": "btn_nav_servers", "style": "primary"},
                    {"label": "🌐 Nodes", "custom_id": "btn_nav_nodes", "style": "primary"},
                    {"label": "👤 Users", "custom_id": "btn_nav_users", "style": "primary"}
                ]
            },
            {
                "type": "row",
                "buttons": [
                    {"label": "📊 System Status", "custom_id": "btn_nav_system", "style": "secondary"},
                    {"label": "🚀 Deploy New", "custom_id": "btn_nav_deploy", "style": "success"},
                    {"label": "🔃 Refresh Dashboard", "custom_id": "btn_nav_refresh_dashboard", "style": "secondary"}
                ]
            }
        ]

if DISCORD_UI_AVAILABLE:
    class DiscordDashboardView(View):
        def __init__(self, timeout: int = 180):
            super().__init__(timeout=timeout)
            
            # Row 1
            self.add_item(Button(label="🖥️ Servers", custom_id="btn_nav_servers", style=discord.ButtonStyle.primary, row=0))
            self.add_item(Button(label="🌐 Nodes", custom_id="btn_nav_nodes", style=discord.ButtonStyle.primary, row=0))
            self.add_item(Button(label="👤 Users", custom_id="btn_nav_users", style=discord.ButtonStyle.primary, row=0))
            
            # Row 2
            self.add_item(Button(label="📊 System Status", custom_id="btn_nav_system", style=discord.ButtonStyle.secondary, row=1))
            self.add_item(Button(label="🚀 Deploy New", custom_id="btn_nav_deploy", style=discord.ButtonStyle.success, row=1))
            self.add_item(Button(label="🔃 Refresh Dashboard", custom_id="btn_nav_refresh_dashboard", style=discord.ButtonStyle.secondary, row=1))
