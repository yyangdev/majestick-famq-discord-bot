import discord
from discord.ext import commands
from .create_ticket import RPModal, CAPModal
from database.tickets_db import get_stats, get_all_tickets

class TicketTypeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
        rp_button = discord.ui.Button(
            label="RP ЗАЯВКА",
            style=discord.ButtonStyle.success,
            custom_id="rp"
        )
        rp_button.callback = self.rp_callback
        self.add_item(rp_button)
        
        capt_button = discord.ui.Button(
            label="CAPT ЗАЯВКА",
            style=discord.ButtonStyle.primary,
            custom_id="capt"
        )
        capt_button.callback = self.capt_callback
        self.add_item(capt_button)
    
    async def rp_callback(self, interaction: discord.Interaction):
        modal = RPModal()
        await interaction.response.send_modal(modal)
    
    async def capt_callback(self, interaction: discord.Interaction):
        modal = CAPModal()
        await interaction.response.send_modal(modal)

class TicketsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='regent')
    async def regent_apply(self, ctx):
        embed = discord.Embed(
            title="Regent Family",
            description="Путь в семью Regent начинается здесь!\n\n"
                        "Заявки в семью принимаются только на сервер Orlando.\n"
                        "Уведомление о приглашении на обзвон отправляется в ваш тикет на заявку в семью!\n\n"
                        "**Срок рассмотрения заявки:** до 24 часов (по занятости рекрутов).\n"
                        "**Важно:** если заявка неполная — заявка будет автоматически ОТКЛОНЕНА.\n\n"
                        "**Дополнительные правила к подаче заявки:**\n"
                        "• Откаты с GG — не более 1 недели назад (не менее 5 минут).\n"
                        "• Откаты с МП (ВЗЗ, MCL, Capt) — не более 60 дней назад.\n"
                        "• Откаты должны быть с сайги и со спешика или тяжки (на выбор, по одному откату для каждого указанного ганга).\n\n"
                        "Если вы являетесь представителем СТАКА, который планировал присоединиться к нашей фаме — напишите нам в личные сообщения @Choopstickk @.yyang.\n\n"
                        "**В случае нарушений условий или некорректной подачи заявки — заявка АВТОМАТИЧЕСКИ ОТКЛОНЯЕТСЯ.**\n"
                        "Подать заявку можно только при открытом наборе.",
            color=discord.Color.blue()
        )
        view = TicketTypeView()
        await ctx.send(embed=embed, view=view)
    
    @commands.command(name='stats')
    @commands.has_permissions(administrator=True)
    async def show_stats(self, ctx):
        stats = get_stats()
        
        embed = discord.Embed(
            title="Статистика заявок",
            color=discord.Color.gold()
        )
        
        embed.add_field(name="Всего заявок", value=stats['total'], inline=True)
        embed.add_field(name="Принято", value=stats['accepted'], inline=True)
        embed.add_field(name="Отклонено", value=stats['denied'], inline=True)
        embed.add_field(name="Открыто", value=stats['open'], inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='history')
    @commands.has_permissions(administrator=True)
    async def show_history(self, ctx, limit: int = 10):
        tickets = get_all_tickets(limit)
        
        if not tickets:
            await ctx.send("Нет заявок в истории")
            return
        
        embed = discord.Embed(
            title="История заявок",
            color=discord.Color.blue()
        )
        
        for ticket in tickets:
            status_emoji = "✅" if ticket['status'] == 'accepted' else "❌" if ticket['status'] == 'denied' else "🟡"
            embed.add_field(
                name=f"{status_emoji} {ticket['topic']}",
                value=f"От: <@{ticket['user_id']}>\n{ticket['created_at'][:10]}",
                inline=False
            )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(TicketsCog(bot))