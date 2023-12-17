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
        self.mvp_task.start(ctx)
        self.cleanup_queue_task.start()

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
        # Avoid registering duplicates by using the message itself as a key
        for output in outputs:
            if output['msg'] not in self.mvp_message_queue.keys():
                self.mvp_message_queue[output['msg']] = {
                    'was_broadcast': False,
                    'channel': output['channel'],
                    'time': output['time']
                }
        
        # Send mvp messages in the queue (and mark them as sent)
        for mvp_msg, mvp_data in self.mvp_message_queue.items():
            # await ctx.send(f'{mvp_msg}, {mvp_data["was_broadcast"]}')
            if mvp_data['was_broadcast'] == False:
                try:
                    await ctx.send(f'MVP {mvp_data["channel"]} {mvp_data["time"]}')
                    self.mvp_message_queue[mvp_msg]['was_broadcast'] = True
                except Exception:
                    pass

    @mvp_task.before_loop
    async def before_mvp_task(self):
        print('waiting to start mvp task until bot is ready')
        await self.bot.wait_until_ready()

    # == additional garbage cleanup task == 
    
    @tasks.loop(minutes=1.0)
    async def cleanup_queue_task(self):
        self.mvp_message_queue = {}

    @cleanup_queue_task.before_loop
    async def before_cleanup_queue_task(self):
        print('waiting to start cleanup queue task until bot is ready')
        await self.bot.wait_until_ready()