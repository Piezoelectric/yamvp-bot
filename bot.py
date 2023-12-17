from discord.ext import tasks, commands

class DefaultCommands(commands.Cog):
    def __init__(self, bot, ip, inv_l):
        self.bot = bot
        self.index = 0
        self.image_parser = ip
        self.invite_link = inv_l

    def cog_unload(self):
        self.printer.cancel()

    @commands.hybrid_command()
    async def test(self, ctx):
        await ctx.send("respondse")
    
    @commands.hybrid_command()
    async def invite(self, ctx):
        await ctx.send(f'Invite me to your server: {self.invite_link}')

    # == TASK-RELATED COMMANDS ==
        
    @commands.hybrid_command()
    async def start_loop(self, ctx):
        await ctx.send('Starting the loop and printing to this channel')
        self.printer.start(ctx)

    @commands.hybrid_command()
    async def cancel_loop(self, ctx):
        await ctx.send('Cancelling the loop')
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