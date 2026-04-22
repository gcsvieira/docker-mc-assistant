import asyncio
import datetime
import logging
from ui import strings
from ops import docker

logger = logging.getLogger('mc_assistant')

# Configuration from environment
import os
DISCORD_NOTIFY_CHANNEL_ID_STR = os.environ.get("DISCORD_NOTIFY_CHANNEL_ID", "")
AUTOSTOP_TIMEOUT_ENV_KEY = os.environ.get("AUTOSTOP_TIMEOUT_ENV_KEY", "AUTOSTOP_TIMEOUT_EST")

async def autostop_watcher_loop(client):
    """
    Persistent background task: checks the MC container logs periodically and sends a Discord
    notification whenever AUTO_STOP shuts the server down.
    """
    # We only care about autostops that happen AFTER the bot starts
    last_check_time = datetime.datetime.now(datetime.timezone.utc)

    while True:
        # Check for the autostop signal in the recent logs
        triggered, has_players = await asyncio.to_thread(docker.check_for_autostop, since=last_check_time)
        
        # Update last_check_time slightly before the current check to avoid missing lines 
        last_check_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(seconds=1)
        
        if triggered:
            await _send_autostop_notification(client, has_players)
            # After a trigger, wait a bit longer to avoid multiple notifications for the same event
            await asyncio.sleep(60)
        
        # Poll every 10 seconds
        await asyncio.sleep(10)


async def _send_autostop_notification(client, has_players: bool):
    """Sends the autostop message to the configured Discord channel."""
    channel_id_str = DISCORD_NOTIFY_CHANNEL_ID_STR
    if not channel_id_str:
        logger.warning("[Autostop] DISCORD_NOTIFY_CHANNEL_ID is not set. Cannot send notification.")
        return

    try:
        channel_id = int(channel_id_str)
    except ValueError:
        logger.error(f"[Autostop] DISCORD_NOTIFY_CHANNEL_ID is not a valid integer: {channel_id_str!r}")
        return

    channel = client.get_channel(channel_id)
    if channel is None:
        logger.error(f"[Autostop] Could not find channel with ID {channel_id}. Is the bot in that server?")
        return

    env_key = AUTOSTOP_TIMEOUT_ENV_KEY if has_players else "AUTOSTOP_TIMEOUT_INIT"
    default_sek = "15" if has_players else "10"
    seconds = await asyncio.to_thread(docker.get_container_env_var, env_key, default_sek)
    await channel.send(strings.MSG_AUTOSTOP_NOTIFICATION(int(seconds) // 60, has_players))


async def background_wait_for_ready(interaction, action: str = "start", since: datetime.datetime = None):
    """Wait for the server to be ready in the background and notify the user."""
    ready = await asyncio.to_thread(docker.wait_for_server_ready, since=since)
    if ready:
        if action == "restart":
            await interaction.followup.send(strings.MSG_RESTART_READY)
        else:
            await interaction.followup.send(strings.MSG_SERVER_READY)
