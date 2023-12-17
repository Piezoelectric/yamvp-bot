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

    def cog_unload(self):
        self.printer.cancel()

    @commands.hybrid_command()
    async def test(self, ctx):
        await ctx.send("respondse")
    
    @commands.hybrid_command()
    async def invite(self, ctx):
        await ctx.send(f'Invite me to your server: {INVITE_LINK}')

    # == TASK-RELATED COMMANDS ==
        
    @commands.hybrid_command()
    async def start_loop(self, ctx):
        await ctx.send('starting the loop')
        self.printer.start(ctx)

    @commands.hybrid_command()
    async def cancel_loop(self, ctx):
        await ctx.send('cancelling the loop')
        self.printer.cancel()

    # == THE ACTUAL TASK ==

    @tasks.loop(seconds=5.0)
    async def printer(self, ctx):
        await ctx.send(f'task test: {self.index}')
        self.index += 1

    @printer.before_loop
    async def before_printer(self):
        print('waiting to start task until bot is ready')
        await self.bot.wait_until_ready()

@bot.event
async def on_ready():
    await bot.add_cog(DefaultCommands(bot))
    synced = await bot.tree.sync()
    print(f'We have logged in as {bot.user}, synced commands {[c.name for c in synced]}')

if __name__ == '__main__':
    load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    bot.run(BOT_TOKEN)