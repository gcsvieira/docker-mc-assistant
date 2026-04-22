import discord
from ui import strings

def has_server_admin_role(interaction: discord.Interaction) -> bool:
    if isinstance(interaction.user, discord.Member):
        return any(role.name == strings.DISCORD_ADMIN_ROLE for role in interaction.user.roles)
    return False
