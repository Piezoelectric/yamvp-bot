import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from image_parse import ImageParser
from bot import DefaultCommands, MvpCommands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
INVITE_LINK = 'https://discord.com/api/oauth2/authorize?client_id=728785529679773758&permissions=2048&scope=bot+applications.commands'

default_commands_cog = DefaultCommands(bot, INVITE_LINK)

TESSERACT_FILEPATH = os.getenv('TESSERACT_FILEPATH')
BBOX = tuple([int(a) for a in os.getenv('CAPTURE_REGION').split(',')])

mvp_commands_cog = MvpCommands(bot, TESSERACT_FILEPATH, BBOX, 5)

@bot.event
async def on_ready():
    await bot.add_cog(default_commands_cog)
    await bot.add_cog(mvp_commands_cog)
    synced = await bot.tree.sync()
    print(f'We have logged in as {bot.user}\n',
          f'synced commands: {[c.name for c in synced]}\n')

if __name__ == '__main__':
    bot.run(BOT_TOKEN)