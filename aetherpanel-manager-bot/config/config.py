# AetherPanel Manager Bot
# Made by ZenseiBabe

import os
from dotenv import load_dotenv

# Load configuration variables from .env
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
AETHERPANEL_URL = os.getenv("AETHERPANEL_URL", "http://localhost:3000/api/aether").rstrip("/")
AETHERPANEL_API_KEY = os.getenv("AETHERPANEL_API_KEY", "")
BOT_OWNER_ID = os.getenv("BOT_OWNER_ID", "")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
COMMAND_GUILD_ID = os.getenv("COMMAND_GUILD_ID", "")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

def validate_config() -> list[str]:
    """
    Validates that all essential configurations are present.
    Returns a list of missing configuration names.
    """
    missing = []
    if not DISCORD_TOKEN or DISCORD_TOKEN == "your_discord_token_here":
        missing.append("DISCORD_TOKEN")
    if not AETHERPANEL_URL:
        missing.append("AETHERPANEL_URL")
    if not AETHERPANEL_API_KEY:
        missing.append("AETHERPANEL_API_KEY")
    return missing
