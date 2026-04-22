import os
from dotenv import load_dotenv

load_dotenv(override=True)
DISCORD_ADMIN_ROLE = os.environ.get("DISCORD_ADMIN_ROLE", "Server Admin")

# ==========================================
# Commands
# ==========================================
CMD_SERVER_GROUP_NAME = "server"
CMD_SERVER_GROUP_DESC = "Minecraft Server Management"

# /server start
CMD_START_NAME = "start"
CMD_START_DESC = "Starts the specified Minecraft server."

# /server stop
CMD_STOP_NAME = "stop"
CMD_STOP_DESC = "Stops the Minecraft server after checking for active players."

# /server restart
CMD_RESTART_NAME = "restart"
CMD_RESTART_DESC = "Restarts the Minecraft server after checking for active players."

# /server status
CMD_STATUS_NAME = "status"
CMD_STATUS_DESC = "Displays the current status and uptime of the Minecraft server."

# /server manage
CMD_MANAGE_NAME = "manage"
CMD_MANAGE_DESC = f"Targets a specific container for management. Requires \"{DISCORD_ADMIN_ROLE}\" role."
CMD_MANAGE_ARG_DESC = "The exact name of the Docker container to target."

# /getting-started
CMD_GETTING_STARTED_NAME = "getting-started"
CMD_GETTING_STARTED_DESC = f"Information on how to configure the assistant and the {DISCORD_ADMIN_ROLE} role."

# ==========================================
# Embed Titles
# ==========================================
TITLE_FORCE_OVERRIDE = "Force Override"
TITLE_FORCE_EXECUTED = "Force Override Executed"
TITLE_OVERRIDE_CANCEL = "Override Cancelled"
TITLE_SERVER_DOWN = "Server Status"
TITLE_VERIFICATION_FAILED = "Verification Failed"
TITLE_EXECUTING_ACTION = "Executing {}"
TITLE_ACTION_FAILED = "{} Failed"
TITLE_PLAYERS_DETECTED = "Players Detected"
TITLE_ADMIN_OVERRIDE = "Administrator Override Protocol"
TITLE_WAIT = "Wait"
TITLE_SERVER_ALREADY_UP = "Server Status"
TITLE_SERVER_STARTED = "Server Started"
TITLE_STARTUP_ERROR = "Startup Error"
TITLE_SERVER_STATUS_CARD = "Minecraft Server Status"
TITLE_PERMISSION_DENIED = "Permission Denied"
TITLE_TARGET_UPDATED = "Target Updated"
TITLE_CONFIG_ERROR = "Configuration Error"
TITLE_GETTING_STARTED_CARD = "Getting Started"

# ==========================================
# Responses
# ==========================================
# Buttons & Ephemeral Responses
BTN_DO_IT = "Confirm"
BTN_NEVERMIND = "Cancel"
MSG_GOT_IT = "Request received."

# Status Panel Fields
FIELD_STATUS = "Status"
FIELD_UPTIME = "Uptime"
FIELD_PLAYERS_ONLINE = "Players Online"

# Fixed Message Descriptions
MSG_MISSING_TOKEN = "Missing valid DISCORD_TOKEN in .env. Initialization aborted."
MSG_VERIFICATION_FAILED = "Player verification failed (RCON unreachable). Operation aborted for safety."
MSG_PLAYERS_DETECTED = "Active players detected on the server. Proceeding may disrupt their session."
MSG_ADMIN_OVERRIDE_PROMPT = "*Administrator privileges detected. Do you wish to override safety checks and proceed?*"
MSG_SERVER_STARTED = "The Minecraft server has been started."
MSG_SERVER_STATUS_DESC = "Current state of the server:"
MSG_CONFIG_ERROR = "An error occurred while updating the configuration. Please check the system logs."

# Dynamic Response Templates
TMPL_FORCE_EXECUTED = "Server forcefully {action_past_tense} by an Administrator."
TMPL_SERVER_DOWN = "The server is already in the {state} state."
TMPL_EXECUTING_ACTION = "No players detected. Proceeding to {action_name} the server."
TMPL_RESTART_NOTIFICATION = "A notification will be sent once the operation is complete."
TMPL_ACTION_FAILED = "Failed to {action_name} the server: {msg}"
TMPL_COOLDOWN_WAIT = "Action on cooldown. Please wait before attempting again."
TMPL_SERVER_ALREADY_UP = "The server is already running. {player_sentence}"
TMPL_STARTUP_ERROR = "Server startup failed. System error: {message}"
TMPL_PERMISSION_DENIED = f"Permission denied. The \"{DISCORD_ADMIN_ROLE}\" role is required for this command."
TMPL_TARGET_UPDATED = "Target container name updated to: {container_name}"
TMPL_CONTAINER_NOT_ALLOWED = "The specified container is not in the approved list. Please contact the system administrator."
MSG_CANNOT_CHANGE_WHILE_RUNNING = "The current server is still running. Please stop it before switching targets."

TMPL_START_SUCCESS = "Server startup initiated. A notification will be sent when loading is complete."
TMPL_RESTART_SUCCESS = "Server restart initiated. A notification will be sent when loading is complete."
MSG_SERVER_READY = "The Minecraft server is now ready."
MSG_RESTART_READY = "Server restart completed successfully."
MSG_AUTOSTOP_NOTIFICATION = lambda minutes, has_players: (
    f"No players detected for {minutes} minute{'s' if minutes != 1 else ''}. Stopping the server."
    if has_players
    else f"No players joined within {minutes} minute{'s' if minutes != 1 else ''}. Stopping the server."
)

MSG_GETTING_STARTED_BODY = (
    "**Welcome to the Minecraft Server Assistant!**\n\n"
    "To get started, ensure your Minecraft container is running on this host.\n"
    "By default, the assistant looks for a container named \\`mc_server\\`.\n"
    f"If the container has a different name, a {DISCORD_ADMIN_ROLE} can use \\`/server manage <name>\\` to update the target.\n\n"
    "**Access Control**: Destructive commands (stop, restart, manage) are restricted. "
    f"A Discord role named exactly **\\`{DISCORD_ADMIN_ROLE}\\`** must be present in the server "
    "and assigned to users to permit these actions."
)


# ==========================================
# Whitelist System
# ==========================================
CMD_WHITELIST_GROUP_NAME = "whitelist"
CMD_WHITELIST_GROUP_DESC = "Manage the server player whitelist."

CMD_WHITELIST_ADD_NAME = "add"
CMD_WHITELIST_ADD_DESC = f"Add a player to the whitelist. Requires {DISCORD_ADMIN_ROLE} role."

CMD_WHITELIST_REMOVE_NAME = "remove"
CMD_WHITELIST_REMOVE_DESC = f"Remove a player from the whitelist. Requires {DISCORD_ADMIN_ROLE} role."

CMD_WHITELIST_LIST_NAME = "list"
CMD_WHITELIST_LIST_DESC = f"List all whitelisted players. Requires {DISCORD_ADMIN_ROLE} role."
CMD_WHITELIST_PLAYER_ARG_DESC = "Minecraft username of the player."

TITLE_WHITELIST_SUCCESS = "Whitelist Updated"
TITLE_WHITELIST_ERROR = "Whitelist Error"
TITLE_WHITELIST_LIST = "Server Whitelist"
TITLE_RCON_UNREACHABLE = "RCON Unreachable"

MSG_RCON_UNREACHABLE = "The server is running, but the RCON interface is unreachable."

TMPL_WHITELIST_ACTION = "Executed whitelist {action} for player {player}.\n**Result:**\n{result}"

