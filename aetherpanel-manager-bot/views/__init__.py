# AetherPanel Manager Bot
# Made by ZenseiBabe

from views.pagination import PaginatedViewDict
from views.dashboard import DashboardViewDict
from views.server_views import ServerControlsViewDict
from views.node_views import NodeControlsViewDict
from views.admin_views import AdminDashboardViewDict
from views.help_views import HelpViewDict

# Conditional Discord.py wrappers
try:
    from views.pagination import DiscordPaginatedView
    from views.dashboard import DiscordDashboardView
    from views.server_views import DiscordServerControlsView
    from views.node_views import DiscordNodeControlsView
    from views.admin_views import DiscordAdminDashboardView
    from views.help_views import DiscordHelpView
except ImportError:
    pass
