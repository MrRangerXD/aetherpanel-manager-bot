# AetherPanel Manager Bot
# Made by ZenseiBabe

try:
    import discord
    from discord.ui import View, Button
    DISCORD_UI_AVAILABLE = True
except ImportError:
    DISCORD_UI_AVAILABLE = False

class AdminDashboardViewDict:
    @staticmethod
    def get_components() -> list:
        return [
            {
                "type": "row",
                "buttons": [
                    {"label": "👥 All Users", "custom_id": "btn_nav_users", "style": "primary"},
                    {"label": "🖥️ All Servers", "custom_id": "btn_nav_servers", "style": "primary"},
                    {"label": "🌐 All Nodes", "custom_id": "btn_nav_nodes", "style": "primary"}
                ]
            },
            {
                "type": "row",
                "buttons": [
                    {"label": "📊 Core Metrics", "custom_id": "btn_nav_system", "style": "secondary"},
                    {"label": "🔃 Refresh metrics", "custom_id": "btn_admin_refresh_dashboard", "style": "primary"}
                ]
            }
        ]

    @staticmethod
    def get_user_controls(user_id: str, is_suspended: bool = False) -> list:
        status_label = "✅ Unsuspend Account" if is_suspended else "🚫 Suspend Account"
        status_style = "success" if is_suspended else "danger"
        status_action = "unsuspend" if is_suspended else "suspend"

        return [
            {
                "type": "row",
                "buttons": [
                    {"label": "💳 Adjust Credits", "custom_id": f"btn_user_credits_modal_{user_id}", "style": "primary"},
                    {"label": "📁 User's Servers", "custom_id": f"btn_user_servers_{user_id}", "style": "primary"},
                    {"label": status_label, "custom_id": f"btn_user_status_{status_action}_{user_id}", "style": status_style}
                ]
            },
            {
                "type": "row",
                "buttons": [
                    {"label": "◀️ Back to Users", "custom_id": "btn_nav_users", "style": "secondary"},
                    {"label": "🔃 Refresh Profile", "custom_id": f"btn_user_details_{user_id}", "style": "primary"}
                ]
            }
        ]

if DISCORD_UI_AVAILABLE:
    class DiscordAdminDashboardView(View):
        def __init__(self, timeout: int = 180):
            super().__init__(timeout=timeout)
            self.add_item(Button(label="👥 All Users", custom_id="btn_nav_users", style=discord.ButtonStyle.primary, row=0))
            self.add_item(Button(label="🖥️ All Servers", custom_id="btn_nav_servers", style=discord.ButtonStyle.primary, row=0))
            self.add_item(Button(label="🌐 All Nodes", custom_id="btn_nav_nodes", style=discord.ButtonStyle.primary, row=0))
            self.add_item(Button(label="📊 Core Metrics", custom_id="btn_nav_system", style=discord.ButtonStyle.secondary, row=1))
            self.add_item(Button(label="🔃 Refresh Metrics", custom_id="btn_admin_refresh_dashboard", style=discord.ButtonStyle.primary, row=1))
