import discord
from discord import app_commands
from ui import strings, embeds

@app_commands.command(name=strings.CMD_GETTING_STARTED_NAME, description=strings.CMD_GETTING_STARTED_DESC)
async def getting_started(interaction: discord.Interaction):
    await interaction.response.send_message(embed=embeds.create_assistant_embed(
        strings.TITLE_GETTING_STARTED_CARD, 
        strings.MSG_GETTING_STARTED_BODY, 
        "success"
    ), ephemeral=False)
