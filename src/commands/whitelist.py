import discord
import asyncio
from discord import app_commands
from commands.server import server_group
from ui import strings, utils
from ops import docker, rcon

whitelist_group = app_commands.Group(
    name=strings.CMD_WHITELIST_GROUP_NAME, 
    parent=server_group, 
    description=strings.CMD_WHITELIST_GROUP_DESC
)

async def _whitelist_action(interaction: discord.Interaction, action: str, player: str = None):
    if not utils.has_server_admin_role(interaction):
        await interaction.response.send_message(strings.TMPL_PERMISSION_DENIED, ephemeral=True)
        return
        
    await interaction.response.defer(ephemeral=False)
    
    if not await asyncio.to_thread(docker.is_container_running):
        verb = "check the list" if action == "list" else f"{action} to the whitelist" if action == "add" else "remove from the whitelist"
        await interaction.followup.send(f"Operation failed: {verb} is not possible because the server is stopped.")
        return
        
    cmd = f"whitelist {action}" if not player else f"whitelist {action} {player}"
    success, output = await asyncio.to_thread(docker.run_mc_command, cmd)
    
    if not success:
        await interaction.followup.send(strings.MSG_RCON_UNREACHABLE)
        return

    if "Unknown command" in output or "Error" in output:
        await interaction.followup.send(strings.TITLE_WHITELIST_ERROR, f"{output}", "fail")
        return
        
    if action == "list":
        parsed_wl = rcon.parse_whitelist(output)
        sentence = rcon.build_whitelist_sentence(parsed_wl)
        await interaction.followup.send(sentence)
    else:
        sentence = rcon.format_whitelist_action(action, player, output)
        await interaction.followup.send(sentence)

@whitelist_group.command(name=strings.CMD_WHITELIST_ADD_NAME, description=strings.CMD_WHITELIST_ADD_DESC)
@app_commands.describe(player=strings.CMD_WHITELIST_PLAYER_ARG_DESC)
@app_commands.checks.cooldown(1, 5)
async def whitelist_add(interaction: discord.Interaction, player: str):
    await _whitelist_action(interaction, "add", player)

@whitelist_group.command(name=strings.CMD_WHITELIST_REMOVE_NAME, description=strings.CMD_WHITELIST_REMOVE_DESC)
@app_commands.describe(player=strings.CMD_WHITELIST_PLAYER_ARG_DESC)
@app_commands.checks.cooldown(1, 5)
async def whitelist_remove(interaction: discord.Interaction, player: str):
    await _whitelist_action(interaction, "remove", player)

@whitelist_group.command(name=strings.CMD_WHITELIST_LIST_NAME, description=strings.CMD_WHITELIST_LIST_DESC)
@app_commands.checks.cooldown(1, 10)
async def whitelist_list(interaction: discord.Interaction):
    await _whitelist_action(interaction, "list")
