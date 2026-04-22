import os
from discord import Embed

def create_assistant_embed(title: str, description: str, state: str) -> Embed:
    if state == "success":
        color = 0x00CED1  # Cyan/Teal
    elif state == "fail":
        color = 0xFF4500  # Red
    elif state == "warning":
        color = 0xFFA500  # Orange
    else:
        color = 0x00CED1

    embed = Embed(title=title, description=description, color=color)
    # Note: Thumbnails removed to ensure neutral presentation. 
    # For a premium look, custom icons can be attached via discord.File in the command handler.
    return embed
