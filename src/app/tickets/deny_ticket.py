import discord
from datetime import datetime
from .close_ticket import active_tickets

class DenyButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Отказать", style=discord.ButtonStyle.danger)
    
    async def callback(self, interaction: discord.Interaction):
        modal = DenyReasonModal(interaction.channel)
        await interaction.response.send_modal(modal)

class DenyReasonModal(discord.ui.Modal):
    def __init__(self, channel):
        super().__init__(title="Отклонение заявки")
        self.channel = channel
        
        self.reason = discord.ui.TextInput(
            label="Причина отказа",
            placeholder="Укажите причину отказа",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=500
        )
        self.add_item(self.reason)
    
    async def on_submit(self, interaction: discord.Interaction):
        log_channel = discord.utils.get(interaction.guild.channels, name="📋ᥙᴛ᧐ᴦᥙ-ɜᥲяʙ᧐κ")
        if not log_channel:
            log_channel = await interaction.guild.create_text_channel("📋ᥙᴛ᧐ᴦᥙ-ɜᥲяʙ᧐κ")
        
        ticket_info = active_tickets.get(self.channel.id)
        applicant_id = ticket_info["user_id"] if ticket_info else None
        applicant = interaction.guild.get_member(applicant_id) if applicant_id else "Неизвестно"
        
        embed = discord.Embed(
            title="❌ ЗАЯВКА ОТКЛОНЕНА",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        
        embed.add_field(name="Заявитель", value=applicant.mention if applicant != "Неизвестно" else "Неизвестно", inline=False)
        embed.add_field(name="Причина", value=self.reason.value, inline=False)
        embed.add_field(name="Рекрут", value=interaction.user.mention, inline=False)
        
        await log_channel.send(embed=embed)
        
        await self.channel.send(f"❌ Заявка отклонена! Причина: {self.reason.value}")
        await interaction.response.send_message("Заявка отклонена. Тикет будет удалён.", ephemeral=True)
        
        if self.channel.id in active_tickets:
            del active_tickets[self.channel.id]
        await self.channel.delete()