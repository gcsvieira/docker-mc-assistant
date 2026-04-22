import os
import logging
import discord
import asyncio
import datetime
import signal
import sys
from discord.ext import commands
from discord import app_commands

from ui import strings, logger as ui_logger
from ops import docker, tasks
from commands.server import server_group
from commands.whitelist import whitelist_group
from commands.misc import getting_started

# Initialize logging
logger = ui_logger.setup_logging()

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
if not DISCORD_TOKEN or DISCORD_TOKEN == "your_discord_bot_token_here":
    logger.error("Missing DISCORD_TOKEN in environment.")
    exit(1)

class MCServerBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Add commands to the tree
        self.tree.add_command(server_group)
        self.tree.add_command(getting_started)
        
        await self.tree.sync()
        logger.info("Bot is ready and slash commands synced.")

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} — launching autostop watcher.")
        self.autostop_task = asyncio.create_task(tasks.autostop_watcher_loop(self))

    async def close(self):
        """Override close to ensure background tasks are cancelled and docker client is closed."""
        print("[Shutdown] Initiating graceful shutdown...", flush=True)
        
        if hasattr(self, 'autostop_task'):
            print("[Shutdown] Cancelling autostop watcher task...", flush=True)
            self.autostop_task.cancel()
            try:
                await asyncio.wait_for(self.autostop_task, timeout=2.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                print("[Shutdown] Autostop task cancelled or timed out (expected).", flush=True)
        
        try:
            print("[Shutdown] Closing Docker client connection pool...", flush=True)
            docker.client.close()
            print("[Shutdown] Docker client connection pool closed.", flush=True)
        except Exception as e:
            print(f"[Shutdown] Error closing docker client: {e}", flush=True)

        print("[Shutdown] Calling super().close()...", flush=True)
        await super().close()
        print("[Shutdown] Shutdown complete.", flush=True)

client = MCServerBot()

async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(strings.TMPL_COOLDOWN_WAIT, ephemeral=True)
    else:
        logger.error(f"AppCommandError: {error}")

client.tree.on_error = on_app_command_error

if __name__ == "__main__":
    def handle_exit_signal(sig, frame):
        """Force a clean exit when receiving SIGINT or SIGTERM."""
        print(f"\n[System] Received signal {sig}. Closing connections...", flush=True)
        try:
            docker.client.close()
        except:
            pass
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit_signal)
    signal.signal(signal.SIGTERM, handle_exit_signal)

    try:
        client.run(DISCORD_TOKEN, log_handler=None)
    except Exception as e:
        logger.critical(f"Bot execution halted by unhandled exception: {e}")
    finally:
        try:
            docker.client.close()
        except:
            pass
        logger.info("Process exited.")
