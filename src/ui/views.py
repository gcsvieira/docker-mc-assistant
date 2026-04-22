import discord
import asyncio
import datetime
from ui import strings

class AdminOverrideView(discord.ui.View):
    def __init__(self, action_callback, original_message, action_name: str, action_past_tense: str):
        super().__init__(timeout=60)
        self.action_callback = action_callback
        self.original_message = original_message
        self.action_name = action_name
        self.action_past_tense = action_past_tense

    @discord.ui.button(label=strings.BTN_DO_IT, style=discord.ButtonStyle.danger)
    async def do_it(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        
        await interaction.response.edit_message(content=strings.MSG_GOT_IT, view=self)
        
        try:
            await self.original_message.edit(content=strings.TMPL_FORCE_EXECUTED.format(action_past_tense=self.action_past_tense))
        except Exception:
            pass
            
        success, msg = await asyncio.to_thread(self.action_callback)
        if success and self.action_name == "restart":
            from ops.tasks import background_wait_for_ready
            await interaction.followup.send(strings.TMPL_RESTART_SUCCESS)
            # Capture restart time to avoid catching old 'Ready' logs
            now = datetime.datetime.now(datetime.timezone.utc)
            asyncio.create_task(background_wait_for_ready(interaction, action="restart", since=now))

    @discord.ui.button(label=strings.BTN_NEVERMIND, style=discord.ButtonStyle.primary)
    async def nevermind(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content=strings.MSG_GOT_IT, view=self)
