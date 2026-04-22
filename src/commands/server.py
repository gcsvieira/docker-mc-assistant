import discord
import asyncio
import datetime
from discord import app_commands
from ui import strings, embeds, utils, views
from ops import docker, rcon

from ops.tasks import background_wait_for_ready

server_group = app_commands.Group(name=strings.CMD_SERVER_GROUP_NAME, description=strings.CMD_SERVER_GROUP_DESC)

async def check_and_execute_destructive_action(interaction: discord.Interaction, action_callback, action_name: str):
    action_past = "stopped" if action_name == "stop" else "restarted"
    
    await interaction.response.defer(ephemeral=False)
    
    if not await asyncio.to_thread(docker.is_container_running):
        state = "down" if action_name == "stop" else "stopped"
        await interaction.followup.send(strings.TMPL_SERVER_DOWN.format(state=state))
        return
        
    success, output = await asyncio.to_thread(docker.run_mc_command, "list")
    if not success:
        await interaction.followup.send(strings.MSG_VERIFICATION_FAILED)
        return

    parsed = rcon.parse_player_list(output)
    player_count = parsed['current']
        
    if player_count == 0:
        message = strings.TMPL_EXECUTING_ACTION.format(action_name=action_name)

        if action_name == "restart":
            message += " " + strings.TMPL_RESTART_NOTIFICATION

        await interaction.followup.send(message)

        exec_success, msg = await asyncio.to_thread(action_callback)
        if exec_success:
            if action_name == "restart":
                asyncio.create_task(background_wait_for_ready(interaction, action="restart"))
        else:
            await interaction.followup.send(strings.TMPL_ACTION_FAILED.format(action_name=action_name, msg=msg))
        return
        
    original_message = await interaction.followup.send(strings.MSG_PLAYERS_DETECTED)
    
    if utils.has_server_admin_role(interaction):
        view = views.AdminOverrideView(action_callback, original_message, action_name, action_past)
        await interaction.followup.send(
            strings.MSG_ADMIN_OVERRIDE_PROMPT,
            view=view, 
            ephemeral=True
        )

@server_group.command(name=strings.CMD_START_NAME, description=strings.CMD_START_DESC)
async def server_start(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    if await asyncio.to_thread(docker.is_container_running):
        success, output = await asyncio.to_thread(docker.run_mc_command, "list")
        if success:
            parsed = rcon.parse_player_list(output)
            sentence = rcon.build_playing_sentence(parsed['players'])
        else:
            sentence = "but player data could not be retrieved."
        await interaction.followup.send(strings.TMPL_SERVER_ALREADY_UP.format(player_sentence=sentence))
        return
    success, message = await asyncio.to_thread(docker.start_mc_server)
    if success:
        await interaction.followup.send(strings.TMPL_START_SUCCESS)
        # Capture start time to avoid catching old 'Ready' logs
        now = datetime.datetime.now(datetime.timezone.utc)
        # Launch background task to notify when ready
        asyncio.create_task(background_wait_for_ready(interaction, since=now))
    else:
        await interaction.followup.send(strings.TMPL_STARTUP_ERROR.format(message=message))

@server_group.command(name=strings.CMD_STOP_NAME, description=strings.CMD_STOP_DESC)
@app_commands.checks.cooldown(1, 15)
async def server_stop(interaction: discord.Interaction):
    await check_and_execute_destructive_action(interaction, docker.stop_mc_server, "stop")

@server_group.command(name=strings.CMD_RESTART_NAME, description=strings.CMD_RESTART_DESC)
@app_commands.checks.cooldown(1, 15)
async def server_restart(interaction: discord.Interaction):
    await check_and_execute_destructive_action(interaction, docker.restart_mc_server, "restart")

@server_group.command(name=strings.CMD_STATUS_NAME, description=strings.CMD_STATUS_DESC)
async def server_status(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    info = await asyncio.to_thread(docker.get_server_status_info)
    status = info["status"]
    uptime = info["uptime"]
    embed = embeds.create_assistant_embed(strings.TITLE_SERVER_STATUS_CARD, "", "success" if status == "ACTIVE" else "warning")
    embed.add_field(name=strings.FIELD_STATUS, value=status, inline=True)
    if status == "ACTIVE":
        embed.add_field(name=strings.FIELD_UPTIME, value=uptime, inline=True)
        success, output = await asyncio.to_thread(docker.run_mc_command, "list")
        if success:
            parsed = rcon.parse_player_list(output)
            c = parsed['current']
            m = parsed['max']
            names = "\n".join(parsed['players']) if parsed['players'] else "None"
            embed.add_field(name=f"{strings.FIELD_PLAYERS_ONLINE} ({c}/{m})", value=names, inline=False)
        else:
            embed.add_field(name=strings.FIELD_PLAYERS_ONLINE, value="Couldn't fetch them! Is the server starting?", inline=False)
    await interaction.followup.send(content=strings.MSG_SERVER_STATUS_DESC, embed=embed)

async def manage_autocomplete(
    interaction: discord.Interaction,
    current: str,
) -> list[app_commands.Choice[str]]:
    allowed_containers = await asyncio.to_thread(docker.get_allowed_containers)
    return [
        app_commands.Choice(name=container, value=container)
        for container in allowed_containers if current.lower() in container.lower()
    ][:25]

@server_group.command(name=strings.CMD_MANAGE_NAME, description=strings.CMD_MANAGE_DESC)
@app_commands.describe(container_name=strings.CMD_MANAGE_ARG_DESC)
@app_commands.autocomplete(container_name=manage_autocomplete)
async def server_manage(interaction: discord.Interaction, container_name: str):
    if not utils.has_server_admin_role(interaction):
        await interaction.response.send_message(strings.TMPL_PERMISSION_DENIED, ephemeral=True)
        return
        
    await interaction.response.defer(ephemeral=False)
    
    # Check if the current container is running before switching
    if await asyncio.to_thread(docker.is_container_running):
        await interaction.followup.send(strings.MSG_CANNOT_CHANGE_WHILE_RUNNING)
        return
    
    success, reason = await asyncio.to_thread(docker.set_container_name, container_name)
    if success:
        await interaction.followup.send(strings.TMPL_TARGET_UPDATED.format(container_name=container_name))
    elif reason == "not_allowed":
        await interaction.followup.send(strings.TMPL_CONTAINER_NOT_ALLOWED)
    else:
        await interaction.followup.send(strings.MSG_CONFIG_ERROR)
