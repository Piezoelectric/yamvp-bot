import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

INVITE_LINK = 'https://discord.com/api/oauth2/authorize?client_id=728785529679773758&permissions=2048&scope=bot+applications.commands'

class DefaultCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @commands.hybrid_command()
    async def test(self, ctx):
        await ctx.send("respondse")
    
    @commands.hybrid_command()
    async def invite(self, ctx):
        await ctx.send(f'Invite me to your server: {INVITE_LINK}')
    
    @tasks.loop(seconds=5.0)
    async def printer(self):
        print(f'task test: {self.index}')
        self.index += 1

@bot.event
async def on_ready():
    await bot.add_cog(DefaultCommands(bot))
    synced = await bot.tree.sync()
    print(f'We have logged in as {bot.user}, synced commands {[c.name for c in synced]}')

if __name__ == '__main__':
    load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    bot.run(BOT_TOKEN)