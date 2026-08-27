# AetherPanel Manager Bot
# Made by ZenseiBabe

from utils.watermark import WATERMARK_TEXT, apply_watermark, apply_watermark_to_discord_embed
from utils.logger import get_logger
from utils.errors import format_api_error
from utils.embeds import get_error_embed, get_success_embed, get_info_embed
from utils.permissions import PermissionLevel, get_user_permission
