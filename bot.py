from discord.ext import tasks, commands
from image_parse import ImageParser

class DefaultCommands(commands.Cog):
    def __init__(self, bot, inv_l):
        self.bot = bot
        self.invite_link = inv_l

    @commands.hybrid_command()
    async def test(self, ctx):
        await ctx.send("respondse")
    
    @commands.hybrid_command()
    async def invite(self, ctx):
        await ctx.send(f'Invite me to your server: {self.invite_link}')

class MvpCommands(commands.Cog):
    def __init__(self, bot, filepath, bbox, wait_time):
        self.bot = bot
        self.image_parser = ImageParser(filepath, bbox)
        self.mvp_messages = {}
        self.wait_time = wait_time
    
    def cog_unload(self):
        self.mvp_task.cancel()

    # == COMMANDS FOR REGISTERING THE TASK TO A CHANNEL ==

    @commands.hybrid_command()
    async def start_loop(self, ctx):
        await ctx.send('Starting the loop and printing to this channel')
        self.mvp_task.start(ctx)

    @commands.hybrid_command()
    async def cancel_loop(self, ctx):
        await ctx.send('Cancelling the loop')
        self.mvp_task.cancel()

    # == THE ACTUAL TASK ==

    @tasks.loop(seconds=5.0)
    async def mvp_task(self, ctx):
        self.image_parser.capture()
        output = self.image_parser.clean_and_parse()
        await ctx.send(output)

    @mvp_task.before_loop
    async def before_mvp_task(self):
        print('waiting to start task until bot is ready')
        await self.bot.wait_until_ready()