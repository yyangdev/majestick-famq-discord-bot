import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from database.tickets_db import init_db

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    await bot.load_extension('tickets')

@bot.event
async def on_ready():
    init_db()
    print(f'Бот {bot.user} запущен')
    await load_extensions()
    print('Система заявок загружена')

bot.run(TOKEN)