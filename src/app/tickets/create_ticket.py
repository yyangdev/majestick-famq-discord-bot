import discord
from datetime import datetime
import json
from database.tickets_db import save_ticket
from .views import FullTicketView

class RPModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="RP ЗАЯВКА")
        
        self.ign_static = discord.ui.TextInput(
            label="Никнейм в игре и статик",
            placeholder="Ваш игровой ник и статик (если есть)",
            required=True,
            max_length=100
        )
        self.add_item(self.ign_static)
        
        self.ooc_name = discord.ui.TextInput(
            label="OOC имя и возраст",
            placeholder="Ваше реальное имя и возраст",
            required=True,
            max_length=100
        )
        self.add_item(self.ooc_name)
        
        self.families = discord.ui.TextInput(
            label="Семьи в которых вы состояли",
            placeholder="Перечислите все семьи, где вы были",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=300
        )
        self.add_item(self.families)
        
        self.reason = discord.ui.TextInput(
            label="Почему именно наша семья",
            placeholder="Ваша мотивация",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=500
        )
        self.add_item(self.reason)
        
        self.online = discord.ui.TextInput(
            label="Средний онлайн в день и прайм тайм",
            placeholder="Сколько часов в день играете / в какое время",
            required=True,
            max_length=100
        )
        self.add_item(self.online)
    
    async def on_submit(self, interaction: discord.Interaction):
        await self.create_ticket(interaction, "RP ЗАЯВКА", "rp")
    
    async def create_ticket(self, interaction: discord.Interaction, topic: str, ticket_type: str):
        guild = interaction.guild
        member = interaction.user
        
        category = discord.utils.get(guild.categories, name="ТИКЕТЫ")
        if not category:
            category = await guild.create_category("ТИКЕТЫ")
        
        answers = json.dumps({
            "Никнейм и статик": self.ign_static.value,
            "OOC имя и возраст": self.ooc_name.value,
            "Семьи": self.families.value,
            "Мотивация": self.reason.value,
            "Онлайн": self.online.value
        }, ensure_ascii=False)
        
        channel_name = f"rp-{member.name}".lower()
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        admin_role = discord.utils.get(guild.roles, name="Admin")
        if admin_role:
            overwrites[admin_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        support_role = discord.utils.get(guild.roles, name="Support")
        if support_role:
            overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
        
        save_ticket(channel.id, member.id, member.name, topic, ticket_type, answers, datetime.now().isoformat())
        
        embed = discord.Embed(
            title=topic,
            color=discord.Color.gold(),
            timestamp=datetime.now()
        )
        embed.add_field(name="От кого", value=member.mention, inline=False)
        embed.add_field(name="Никнейм в игре и статик", value=self.ign_static.value, inline=False)
        embed.add_field(name="OOC имя и возраст", value=self.ooc_name.value, inline=False)
        embed.add_field(name="Семьи", value=self.families.value, inline=False)
        embed.add_field(name="Мотивация", value=self.reason.value, inline=False)
        embed.add_field(name="Онлайн", value=self.online.value, inline=False)
        
        view = FullTicketView()
        
        await channel.send(embed=embed, view=view)
        await channel.send(f"{member.mention} {admin_role.mention if admin_role else ''} {support_role.mention if support_role else ''}")
        
        await interaction.response.send_message(f"Заявка создана! Перейдите в {channel.mention}", ephemeral=True)

class CAPModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="CAPT ЗАЯВКА")
        
        self.ign = discord.ui.TextInput(
            label="Никнейм в игре",
            placeholder="Ваш игровой ник",
            required=True,
            max_length=50
        )
        self.add_item(self.ign)
        
        self.static = discord.ui.TextInput(
            label="Статик",
            placeholder="Ваш статик",
            required=False,
            max_length=50
        )
        self.add_item(self.static)
        
        self.ooc_name = discord.ui.TextInput(
            label="OOC имя и возраст",
            placeholder="Ваше реальное имя и возраст",
            required=True,
            max_length=100
        )
        self.add_item(self.ooc_name)
        
        self.otkat = discord.ui.TextInput(
            label="Откат сайга и спешик 2+ минуты гангейм",
            placeholder="Ваши откаты",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=200
        )
        self.add_item(self.otkat)
        
        self.mcl = discord.ui.TextInput(
            label="Откаты MCL каптов и МП",
            placeholder="Ваши откаты в MCL",
            style=discord.TextStyle.paragraph,
            required=False,
            max_length=200
        )
        self.add_item(self.mcl)
    
    async def on_submit(self, interaction: discord.Interaction):
        await self.create_ticket(interaction, "CAPT ЗАЯВКА", "capt")
    
    async def create_ticket(self, interaction: discord.Interaction, topic: str, ticket_type: str):
        guild = interaction.guild
        member = interaction.user
        
        category = discord.utils.get(guild.categories, name="ТИКЕТЫ")
        if not category:
            category = await guild.create_category("ТИКЕТЫ")
        
        answers = json.dumps({
            "Никнейм": self.ign.value,
            "Статик": self.static.value if self.static.value else "Не указан",
            "OOC имя и возраст": self.ooc_name.value,
            "Откаты": self.otkat.value,
            "MCL откаты": self.mcl.value if self.mcl.value else "Не указаны"
        }, ensure_ascii=False)
        
        channel_name = f"capt-{member.name}".lower()
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        admin_role = discord.utils.get(guild.roles, name="Admin")
        if admin_role:
            overwrites[admin_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        support_role = discord.utils.get(guild.roles, name="Support")
        if support_role:
            overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
        
        save_ticket(channel.id, member.id, member.name, topic, ticket_type, answers, datetime.now().isoformat())
        
        embed = discord.Embed(
            title=topic,
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.add_field(name="От кого", value=member.mention, inline=False)
        embed.add_field(name="Никнейм в игре", value=self.ign.value, inline=False)
        embed.add_field(name="Статик", value=self.static.value if self.static.value else "Не указан", inline=False)
        embed.add_field(name="OOC имя и возраст", value=self.ooc_name.value, inline=False)
        embed.add_field(name="Откаты", value=self.otkat.value, inline=False)
        embed.add_field(name="MCL откаты", value=self.mcl.value if self.mcl.value else "Не указаны", inline=False)
        
        view = FullTicketView()
        
        await channel.send(embed=embed, view=view)
        await channel.send(f"{member.mention} {admin_role.mention if admin_role else ''} {support_role.mention if support_role else ''}")
        
        await interaction.response.send_message(f"Заявка создана! Перейдите в {channel.mention}", ephemeral=True)