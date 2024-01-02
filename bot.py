from discord.ext import tasks, commands
from image_parse import ImageParser

BASE_URI = 'https://discord.com/api/oauth2/authorize?client_id='
PERMISSIONS_STRING = '&permissions=2048&scope=bot+applications.commands'

MVP_ICONS = ':regional_indicator_m::regional_indicator_v::regional_indicator_p:'

class DefaultCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def test(self, ctx):
        await ctx.send("response")
    
    @commands.hybrid_command()
    async def invite(self, ctx):
        self.client_id = self.bot.user.id 
        await ctx.send(f'Invite me to your server: {BASE_URI}{self.client_id}{PERMISSIONS_STRING}')

class MvpCommands(commands.Cog):
    def __init__(self, bot, filepath, bbox):
        self.bot = bot
        self.image_parser = ImageParser(filepath, bbox)
        self.mvp_message_queue = {}
        self.registered_channels = set()

    def cog_load(self):
        self.cleanup_queue_task.start()
        self.mvp_task.start()
        # self.debug_task.start()
    
    def cog_unload(self):
        self.mvp_task.cancel()
        self.mvp_message_queue = {}
        self.registered_channels = set()

        self.mvp_task.cancel()
        self.cleanup_queue_task.cancel()

    # == COMMANDS FOR REGISTERING THE MVP OUTPUT TO A CHANNEL ==

    @commands.hybrid_command()
    async def register_channel(self, ctx):
        await ctx.send('The MVP bot will now print to this channel')
        print(f"Registered: {ctx.channel.id}")
        self.registered_channels.add(ctx.channel)

    @commands.hybrid_command()
    async def unregister_channel(self, ctx):
        await ctx.send('The MVP bot will **not** print to this channel')
        print(f"Unregistered: {ctx.channel.id}")
        self.registered_channels.discard(ctx.channel)


    # == THE ACTUAL MVP TASK ==

    @tasks.loop(seconds=20.0)
    async def mvp_task(self):
        self.image_parser.capture()
        outputs = self.image_parser.clean_and_parse()
        
        try:
            self.enqueue_outputs(outputs)
            await self.broadcast_to_channels()
        except Exception:
            pass

    @mvp_task.before_loop
    async def before_mvp_task(self):
        print('waiting to start mvp task until bot is ready')
        await self.bot.wait_until_ready()

    def enqueue_outputs(self, outputs):
        # Register mvp messages in the queue
        # Avoid registering duplicates by using channel+time as key
        for output in outputs:
            key = f'{output["channel"]}{output["time"]}'
            if key not in self.mvp_message_queue.keys():
                self.mvp_message_queue[key] = {
                    'was_broadcast': False,
                    'channel': output['channel'],
                    'time': output['time'],
                    'msg': output['msg'],
                    'location': output['location']
                }

    async def broadcast_to_channels(self):
        # Send mvp messages in the queue (and mark them as sent)
        for mvp_key, mvp_data in self.mvp_message_queue.items():
            # await ctx.send(f'{mvp_key}, {mvp_data}')
            if mvp_data['was_broadcast'] == False:
                for ch in list(self.registered_channels):
                    await ch.send(f'{MVP_ICONS} :satellite:**{mvp_data["channel"]}** :clock:**{mvp_data["time"]}**\n\n*{mvp_data["msg"]}*')
                    self.mvp_message_queue[mvp_key]['was_broadcast'] = True

    # == additional garbage cleanup task == 
    
    @tasks.loop(hours=3.0)
    async def cleanup_queue_task(self):
        self.mvp_message_queue = {}
        for ch in list(self.registered_channels):
            await ch.send("Healthcheck. If you haven't seen one of these messages in six hours, let the bot owner know.")

    @cleanup_queue_task.before_loop
    async def before_cleanup_queue_task(self):
        print('waiting to start cleanup queue task until bot is ready')
        await self.bot.wait_until_ready()

    # == debug task ==
        
    @tasks.loop(seconds=5.0)
    async def debug_task(self):
        # print(self.registered_channels)
        pass 