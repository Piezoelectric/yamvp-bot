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
        self.mvp_message_queue = {}
        self.wait_time = wait_time
    
    def cog_unload(self):
        self.mvp_task.cancel()

    # == COMMANDS FOR REGISTERING THE MVP TASK TO A CHANNEL ==

    @commands.hybrid_command()
    async def start_loop(self, ctx):
        await ctx.send('Starting the loop and printing to this channel')
        self.cleanup_queue_task.start(ctx)
        self.mvp_task.start(ctx)

    @commands.hybrid_command()
    async def cancel_loop(self, ctx):
        await ctx.send('Cancelling the loop')
        self.mvp_task.cancel()
        self.cleanup_queue_task.cancel()

    # == THE ACTUAL MVP TASK ==

    @tasks.loop(seconds=5.0)
    async def mvp_task(self, ctx):
        self.image_parser.capture()
        outputs = self.image_parser.clean_and_parse()

        # Register mvp messages in the queue
        # Avoid registering duplicates by using channel+time as key
        for output in outputs:
            key = f'{output["channel"]}{output["time"]}'
            if key not in self.mvp_message_queue.keys():
                self.mvp_message_queue[key] = {
                    'was_broadcast': False,
                    'channel': output['channel'],
                    'time': output['time'],
                    'msg': output['msg']
                }
        
        # Send mvp messages in the queue (and mark them as sent)
        for mvp_key, mvp_data in self.mvp_message_queue.items():
            # await ctx.send(f'{mvp_key}, {mvp_data}')
            if mvp_data['was_broadcast'] == False:
                try:
                    await ctx.send(f':regional_indicator_m::regional_indicator_v::regional_indicator_p: :satellite:**{mvp_data["channel"]}** :clock:**{mvp_data["time"]}**\n\n*{mvp_data["msg"]}*')
                    self.mvp_message_queue[mvp_key]['was_broadcast'] = True
                except Exception:
                    pass

    @mvp_task.before_loop
    async def before_mvp_task(self):
        print('waiting to start mvp task until bot is ready')
        await self.bot.wait_until_ready()

    # == additional garbage cleanup task == 
    
    @tasks.loop(hours=3.0)
    async def cleanup_queue_task(self, ctx):
        self.mvp_message_queue = {}
        await ctx.send("Healthcheck. If you haven't seen one of these messages in six hours, let the bot owner know.")

    @cleanup_queue_task.before_loop
    async def before_cleanup_queue_task(self):
        print('waiting to start cleanup queue task until bot is ready')
        await self.bot.wait_until_ready()