import discord
from datetime import datetime
from database.tickets_db import get_ticket

class VoiceCallButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Вызвать на обзвон", style=discord.ButtonStyle.primary)
    
    async def callback(self, interaction: discord.Interaction):
        view = VoiceSelectView(interaction.channel)
        await interaction.response.send_message("Выберите канал для обзвона:", view=view, ephemeral=True)

class VoiceSelectView(discord.ui.View):
    def __init__(self, channel):
        super().__init__(timeout=60)
        self.ticket_channel = channel
        
        voice1 = discord.ui.Button(
            label="🔊Обзвон 1",
            style=discord.ButtonStyle.success,
            custom_id="voice1"
        )
        voice1.callback = self.voice1_callback
        self.add_item(voice1)
        
        voice2 = discord.ui.Button(
            label="🔊Обзвон 2",
            style=discord.ButtonStyle.success,
            custom_id="voice2"
        )
        voice2.callback = self.voice2_callback
        self.add_item(voice2)
        
        voice3 = discord.ui.Button(
            label="🔊Обзвон 3",
            style=discord.ButtonStyle.success,
            custom_id="voice3"
        )
        voice3.callback = self.voice3_callback
        self.add_item(voice3)
    
    async def voice1_callback(self, interaction: discord.Interaction):
        await self.send_call_message(interaction, "🔊Обзвон 1")
    
    async def voice2_callback(self, interaction: discord.Interaction):
        await self.send_call_message(interaction, "🔊Обзвон 2")
    
    async def voice3_callback(self, interaction: discord.Interaction):
        await self.send_call_message(interaction, "🔊Обзвон 3")
    
    async def send_call_message(self, interaction: discord.Interaction, voice_channel_name: str):
        ticket = get_ticket(self.ticket_channel.id)
        applicant_id = ticket["user_id"] if ticket else None
        applicant = interaction.guild.get_member(applicant_id) if applicant_id else None
        
        recruiter = interaction.user
        
        voice_channel = discord.utils.get(interaction.guild.voice_channels, name=voice_channel_name)
        
        if not voice_channel:
            await self.ticket_channel.send(f"❌ Канал {voice_channel_name} не найден!")
            await interaction.response.send_message(f"Канал {voice_channel_name} не найден", ephemeral=True)
            return
        
        await self.ticket_channel.send(f"**Рекрут** {recruiter.mention} **вызвал** {applicant.mention if applicant else 'заявителя'} **на обзвон**")
        await self.ticket_channel.send(f"{applicant.mention if applicant else 'Заявитель'} зайдите в канал {voice_channel.mention}")
        
        await interaction.response.send_message(f"Вызов отправлен в {voice_channel.mention}", ephemeral=True)