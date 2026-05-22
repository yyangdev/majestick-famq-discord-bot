import discord
from discord.ext import commands
from .create_ticket import RPModal, CAPModal
from .close_ticket import active_tickets

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
            title="Regent Famq",
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

async def setup(bot):
    await bot.add_cog(TicketsCog(bot))