import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from image_parse import ImageParser
from bot import DefaultCommands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

INVITE_LINK = 'https://discord.com/api/oauth2/authorize?client_id=728785529679773758&permissions=2048&scope=bot+applications.commands'

load_dotenv()

TESSERACT_FILEPATH = os.getenv('TESSERACT_FILEPATH')
BBOX = tuple(os.getenv('CAPTURE_REGION').split(','))
BOT_TOKEN = os.getenv('BOT_TOKEN')

ip = ImageParser(TESSERACT_FILEPATH, BBOX)
cog = DefaultCommands(bot, ip, INVITE_LINK)

@bot.event
async def on_ready():
    await bot.add_cog(cog)
    synced = await bot.tree.sync()
    print(f'We have logged in as {bot.user}\n',
          f'synced commands {[c.name for c in synced]}\n',
          bot.get_cog('DefaultCommands').invite_link)

if __name__ == '__main__':
    bot.run(BOT_TOKEN)