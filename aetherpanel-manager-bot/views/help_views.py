# AetherPanel Manager Bot
# Made by ZenseiBabe

try:
    import discord
    from discord.ui import View, Button
    DISCORD_UI_AVAILABLE = True
except ImportError:
    DISCORD_UI_AVAILABLE = False

class HelpViewDict:
    @staticmethod
    def get_components() -> list:
        return [
            {
                "type": "row",
                "buttons": [
                    {"label": "🖥️ Servers Help", "custom_id": "btn_help_category_servers", "style": "primary"},
                    {"label": "🌐 Nodes Help", "custom_id": "btn_help_category_nodes", "style": "primary"},
                    {"label": "💾 Backups Help", "custom_id": "btn_help_category_backups", "style": "primary"},
                    {"label": "👤 Users Help", "custom_id": "btn_help_category_users", "style": "primary"}
                ]
            },
            {
                "type": "row",
                "buttons": [
                    {"label": "🚀 Deploy Help", "custom_id": "btn_help_category_deploy", "style": "success"},
                    {"label": "🛡️ Admin Help", "custom_id": "btn_help_category_admin", "style": "danger"},
                    {"label": "📊 System Help", "custom_id": "btn_help_category_system", "style": "secondary"},
                    {"label": "🏠 Help Main", "custom_id": "btn_help_category_main", "style": "secondary"}
                ]
            }
        ]

if DISCORD_UI_AVAILABLE:
    class DiscordHelpView(View):
        def __init__(self, timeout: int = 180):
            super().__init__(timeout=timeout)
            # Add buttons matching categories
            self.add_item(Button(label="🖥️ Servers Help", custom_id="btn_help_category_servers", style=discord.ButtonStyle.primary, row=0))
            self.add_item(Button(label="🌐 Nodes Help", custom_id="btn_help_category_nodes", style=discord.ButtonStyle.primary, row=0))
            self.add_item(Button(label="💾 Backups Help", custom_id="btn_help_category_backups", style=discord.ButtonStyle.primary, row=0))
            self.add_item(Button(label="👤 Users Help", custom_id="btn_help_category_users", style=discord.ButtonStyle.primary, row=0))
            
            self.add_item(Button(label="🚀 Deploy Help", custom_id="btn_help_category_deploy", style=discord.ButtonStyle.success, row=1))
            self.add_item(Button(label="🛡️ Admin Help", custom_id="btn_help_category_admin", style=discord.ButtonStyle.danger, row=1))
            self.add_item(Button(label="📊 System Help", custom_id="btn_help_category_system", style=discord.ButtonStyle.secondary, row=1))
            self.add_item(Button(label="🏠 Help Main", custom_id="btn_help_category_main", style=discord.ButtonStyle.secondary, row=1))
