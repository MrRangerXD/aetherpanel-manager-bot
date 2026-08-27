# AetherPanel Manager Bot
# Made by ZenseiBabe

try:
    import discord
    from discord.ui import View, Button
    DISCORD_UI_AVAILABLE = True
except ImportError:
    DISCORD_UI_AVAILABLE = False

class PaginatedViewDict:
    """Helper to return standardized paginated component structures as lists of dictionaries."""
    @staticmethod
    def get_components(current_page: int, total_pages: int, prefix: str, target_id: str = "") -> list:
        buttons = []
        suffix = f"_{target_id}" if target_id else ""
        
        # Previous Button
        buttons.append({
            "label": "◀ Previous",
            "custom_id": f"btn_{prefix}_prev_page_{current_page}{suffix}",
            "style": "secondary",
            "disabled": current_page <= 0
        })
        
        # Indicator Badge (Disabled style button)
        buttons.append({
            "label": f"Page {current_page + 1} of {max(1, total_pages)}",
            "custom_id": f"btn_{prefix}_page_indicator",
            "style": "secondary",
            "disabled": True
        })
        
        # Next Button
        buttons.append({
            "label": "Next ▶",
            "custom_id": f"btn_{prefix}_next_page_{current_page}{suffix}",
            "style": "secondary",
            "disabled": current_page >= total_pages - 1
        })

        # Refresh Button
        buttons.append({
            "label": "🔃 Refresh",
            "custom_id": f"btn_{prefix}_refresh{suffix}",
            "style": "primary",
            "disabled": False
        })

        return [{"type": "row", "buttons": buttons}]

if DISCORD_UI_AVAILABLE:
    class DiscordPaginatedView(View):
        """Active discord.py View for managing server or node list navigation."""
        def __init__(self, current_page: int, total_pages: int, prefix: str, target_id: str = "", timeout: int = 180):
            super().__init__(timeout=timeout)
            suffix = f"_{target_id}" if target_id else ""
            
            self.add_item(Button(
                label="◀ Previous",
                custom_id=f"btn_{prefix}_prev_page_{current_page}{suffix}",
                style=discord.ButtonStyle.secondary,
                disabled=current_page <= 0
            ))
            
            self.add_item(Button(
                label=f"Page {current_page + 1} of {max(1, total_pages)}",
                custom_id=f"btn_{prefix}_page_indicator",
                style=discord.ButtonStyle.secondary,
                disabled=True
            ))
            
            self.add_item(Button(
                label="Next ▶",
                custom_id=f"btn_{prefix}_next_page_{current_page}{suffix}",
                style=discord.ButtonStyle.secondary,
                disabled=current_page >= total_pages - 1
            ))

            self.add_item(Button(
                label="🔃 Refresh",
                custom_id=f"btn_{prefix}_refresh{suffix}",
                style=discord.ButtonStyle.primary
            ))
