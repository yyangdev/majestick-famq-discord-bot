import discord

active_tickets = {}

class CloseButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Закрыть тикет", style=discord.ButtonStyle.danger)
    
    async def callback(self, interaction: discord.Interaction):
        channel = interaction.channel
        if channel.id in active_tickets:
            del active_tickets[channel.id]
        await interaction.response.send_message("Тикет закрывается...")
        await channel.delete()

class CloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CloseButton())