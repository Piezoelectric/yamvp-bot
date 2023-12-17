import discord
from discord import Interaction
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

INVITE_LINK = 'https://discord.com/api/oauth2/authorize?client_id=728785529679773758&permissions=2048&scope=bot+applications.commands'

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f'We have logged in as {bot.user}, synced commands {synced}')

@bot.hybrid_command()
async def test(ctx):
    await ctx.send("respondse")

@bot.hybrid_command()
async def invite(ctx):
    await ctx.send(f'Invite me to your server: {INVITE_LINK}')

if __name__ == '__main__':
    bot.run('NzI4Nzg1NTI5Njc5NzczNzU4.G-JvNS.7_RQMS0qLRsoJ3zACA2AnAF19LJruS_YWvpG4Y')