# AetherPanel Manager Bot
# Made by ZenseiBabe

from config.config import BOT_OWNER_ID, COMMAND_GUILD_ID

class PermissionLevel:
    UNAUTHORIZED = 0
    USER = 1
    MANAGER = 2
    ADMIN = 3

def get_user_permission(user) -> int:
    """
    Checks the permission tier of a Discord User based on Discord Roles,
    Owner settings, or Administrator permissions.
    """
    # 1. Bot Owner bypass
    if BOT_OWNER_ID and str(user.id) == BOT_OWNER_ID:
        return PermissionLevel.ADMIN

    # 2. Check for guild-level permissions (Administrator/Guild Owner)
    try:
        if getattr(user, "guild_permissions", None) and user.guild_permissions.administrator:
            return PermissionLevel.ADMIN
    except Exception:
        pass

    # 3. Check roles if on a Guild member object
    roles_attr = getattr(user, "roles", None)
    if roles_attr:
        for role in roles_attr:
            role_name = role.name.lower()
            role_id = str(role.id)
            if role_name in ("aether admin", "aetheradmin") or role_id == os.getenv("ADMIN_ROLE_ID", ""):
                return PermissionLevel.ADMIN
            if role_name in ("aether manager", "aethermanager") or role_id == os.getenv("MANAGER_ROLE_ID", ""):
                return PermissionLevel.MANAGER

    # Default fallback to regular user permissions
    return PermissionLevel.USER
