# AetherPanel Manager Bot
# Made by ZenseiBabe

from datetime import datetime
from utils.watermark import apply_watermark

def get_error_embed(title: str, description: str, status_code: int = None) -> dict:
    """
    Constructs a branded standard error embed dictionary.
    """
    desc = f"### ⚠️ Operation Aborted\n{description}"
    if status_code:
        desc += f"\n\n*Status Code: `{status_code}`*"

    embed = {
        "title": f"Error: {title}",
        "description": desc,
        "color": 15158332, # Red Hex
        "timestamp": datetime.utcnow().isoformat()
    }
    return apply_watermark(embed)

def get_success_embed(title: str, description: str) -> dict:
    """
    Constructs a branded standard success embed dictionary.
    """
    embed = {
        "title": f"Success: {title}",
        "description": f"### ✅ Task Executed Successfully\n{description}",
        "color": 3066993, # Green Hex
        "timestamp": datetime.utcnow().isoformat()
    }
    return apply_watermark(embed)

def get_info_embed(title: str, description: str) -> dict:
    """
    Constructs a branded general informational embed dictionary.
    """
    embed = {
        "title": title,
        "description": description,
        "color": 3447003, # Blue Hex
        "timestamp": datetime.utcnow().isoformat()
    }
    return apply_watermark(embed)
