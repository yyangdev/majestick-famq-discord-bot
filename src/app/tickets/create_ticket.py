import discord
from datetime import datetime
import json

import config
from database.tickets_db import save_ticket
from .views import FullTicketView
from utils.logger import logger


class TicketModal(discord.ui.Modal):
    def __init__(self, title, ticket_type, fields):
        super().__init__(title=title)
        self.ticket_type = ticket_type
        self.inputs = {}

        for label, placeholder, required, max_length in fields:
            style = discord.TextStyle.paragraph if max_length > 150 else discord.TextStyle.short
            inp = discord.ui.TextInput(
                label=label,
                placeholder=placeholder,
                style=style,
                required=required,
                max_length=max_length,
            )
            self.inputs[label] = inp
            self.add_item(inp)

    async def on_submit(self, interaction: discord.Interaction):
        logger.info(f"Пользователь {interaction.user} подал {self.ticket_type} заявку")
        await create_ticket(interaction, self.title, self.ticket_type, self.inputs)


async def create_ticket(interaction, topic, ticket_type, inputs):
    guild = interaction.guild
    member = interaction.user

    try:
        await interaction.response.send_message("Создаю заявку...", ephemeral=True)
    except discord.InteractionResponded:
        pass

    try:
        apply_role = discord.utils.get(guild.roles, name=config.ROLE_APPLIED)
        if apply_role:
            await member.add_roles(apply_role)

        try:
            dm = await member.create_dm()
            await dm.send(config.DM_MESSAGE)
        except discord.Forbidden:
            pass

        category = discord.utils.get(guild.categories, name=config.TICKETS_CATEGORY_NAME)
        if not category:
            category = await guild.create_category(config.TICKETS_CATEGORY_NAME)

        answers = {label: inp.value for label, inp in inputs.items()}
        channel_name = f"{ticket_type}-{member.name}".lower()

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        for role_name in [
            config.ROLE_RECRUITER,
            config.ROLE_OWNER,
            config.ROLE_DEP_OWNER,
            config.ROLE_ADMIN,
            config.ROLE_SUPPORT,
        ]:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)

        save_ticket(
            channel.id,
            member.id,
            member.name,
            topic,
            ticket_type,
            json.dumps(answers, ensure_ascii=False),
            datetime.now().isoformat(),
        )

        embed = discord.Embed(title=topic, color=discord.Color.gold(), timestamp=datetime.now())
        embed.add_field(name="От кого", value=member.mention, inline=False)
        for label, value in answers.items():
            embed.add_field(name=label, value=value or "—", inline=False)

        role_mentions = []
        for role_name in [config.ROLE_RECRUITER, config.ROLE_OWNER, config.ROLE_DEP_OWNER]:
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                role_mentions.append(role.mention)

        await channel.send(embed=embed, view=FullTicketView())
        if role_mentions:
            await channel.send(f"{member.mention} {' '.join(role_mentions)}")

        await interaction.edit_original_response(content=f"Заявка создана! {channel.mention}")
        logger.info(f"Заявка {ticket_type} создана для {member.name} в {channel.name}")

    except Exception as e:
        logger.error(f"Ошибка создания заявки: {e}")
        await interaction.edit_original_response(content=config.ERROR_TICKET_CREATE)

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
        logger.info(f"Пользователь {interaction.user.name} ({interaction.user.id}) начал подачу CAPT заявки")
        await self.create_ticket(interaction, "CAPT ЗАЯВКА", "capt")
    
    async def create_ticket(self, interaction: discord.Interaction, topic: str, ticket_type: str):
        guild = interaction.guild
        member = interaction.user
        
        try:
            apply_role = discord.utils.get(guild.roles, name="Подал заявку")
            if apply_role:
                await member.add_roles(apply_role)
                logger.debug(f"Выдана роль 'Подал заявку' пользователю {member.name}")
            
            # Отправляем ЛС пользователю
            try:
                dm_channel = await member.create_dm()
                await dm_channel.send("Вы подали заявку в фаму Regent ожидайте скоро ее рассмотрят один из наших рекрутов")
                logger.debug(f"Отправлено ЛС пользователю {member.name}")
            except discord.Forbidden:
                logger.warning(f"Не удалось отправить ЛС пользователю {member.name} - закрытые сообщения")
            except Exception as e:
                logger.error(f"Ошибка отправки ЛС пользователю {member.name}: {e}", exc_info=True)
            
            category = discord.utils.get(guild.categories, name="ТИКЕТЫ")
            if not category:
                category = await guild.create_category("ТИКЕТЫ")
                logger.info("Создана категория 'ТИКЕТЫ' для CAPT заявок")
        
            answers = json.dumps({
                "Никнейм": self.ign.value,
                "Статик": self.static.value if self.static.value else "Не указан",
                "OOC имя и возраст": self.ooc_name.value,
                "Откаты": self.otkat.value,
                "MCL откаты": self.mcl.value if self.mcl.value else "Не указаны"
            }, ensure_ascii=False)

            channel_name = f"capt-{member.name}".lower()

            # Роли которые видят тикет и тегаются
            recruiter_role = discord.utils.get(guild.roles, name="𝐑𝐞𝐜𝐫𝐮𝐢𝐭👨🏻‍💻")
            owner_role = discord.utils.get(guild.roles, name="𝙊𝙬𝙣𝙚𝙧👑")
            dep_owner_role = discord.utils.get(guild.roles, name="𝘿𝙚𝙥.O𝙬𝙣𝙚𝙧⭐")

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }

            # Добавляем роли для просмотра тикета
            if recruiter_role:
                overwrites[recruiter_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            if owner_role:
                overwrites[owner_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
            if dep_owner_role:
                overwrites[dep_owner_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

            admin_role = discord.utils.get(guild.roles, name="Admin")
            if admin_role:
                overwrites[admin_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

            support_role = discord.utils.get(guild.roles, name="Support")
            if support_role:
                overwrites[support_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

            channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
            logger.info(f"Создан тикет-канал {channel.name} для пользователя {member.name}")

            save_ticket(channel.id, member.id, member.name, topic, ticket_type, answers, datetime.now().isoformat())
            logger.debug(f"CAPT заявка сохранена в БД для канала {channel.id}")

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

            # Собираем упоминания ролей
            role_mentions = []
            if recruiter_role:
                role_mentions.append(recruiter_role.mention)
            if owner_role:
                role_mentions.append(owner_role.mention)
            if dep_owner_role:
                role_mentions.append(dep_owner_role.mention)

            await channel.send(embed=embed, view=view)
            await channel.send(f"{member.mention} {' '.join(role_mentions)}")

            await interaction.response.send_message(f"Заявка создана! Перейдите в {channel.mention}", ephemeral=True)
            logger.info(f"CAPT заявка успешно создана для пользователя {member.name} в канале {channel.mention}")
        except Exception as e:
            logger.error(f"Ошибка при создании CAPT заявки для пользователя {member.name}: {e}", exc_info=True)
            await interaction.response.send_message("Произошла ошибка при создании заявки. Попробуйте позже.", ephemeral=True)