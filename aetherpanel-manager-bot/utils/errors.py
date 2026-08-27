# AetherPanel Manager Bot
# Made by ZenseiBabe

def format_api_error(status: int, message: str, details: str = None) -> dict:
    """
    Standard error parser and formatter returning high quality Embed descriptor.
    """
    error_title = "❌ API Request Failed"
    color = 15158332  # Red Hex

    if status == 401:
        error_title = "🔐 Authentication Failure"
        desc = (
            "AetherPanel rejected the configured API key.\n"
            "Verify your `AETHERPANEL_API_KEY` exists and has proper permissions."
        )
    elif status == 403:
        error_title = "⛔ Action Forbidden"
        desc = (
            "The configured credentials do not have permission for this endpoint.\n"
            f"Error details: `{message}`"
        )
    elif status == 404:
        error_title = "🔍 Resource Not Found"
        desc = (
            "The requested node, server, or user could not be found.\n"
            f"Details: `{message}`"
        )
    elif status == 429:
        error_title = "⏳ Rate Limited"
        desc = (
            "You are making requests too quickly. Rate limit has been exceeded.\n"
            "Please back off and try again later."
        )
    elif status == 408:
        error_title = "🔌 Connection Timeout"
        desc = (
            "The AetherPanel REST server did not respond in time.\n"
            "Check if the server is healthy and online."
        )
    elif status == 503:
        error_title = "📡 Panel Unreachable"
        desc = (
            "Could not connect to the panel. It appears to be offline.\n"
            "Verify if your `AETHERPANEL_URL` is pointing to the correct address."
        )
    else:
        desc = f"**Status:** `{status}`\n**Response Message:** `{message}`"
        if details:
            desc += f"\n**Details:** `{details}`"

    return {
        "title": error_title,
        "description": desc,
        "color": color
    }
