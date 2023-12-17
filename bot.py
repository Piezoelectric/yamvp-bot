import discord

intents = discord.Intents.default()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

client.run('NzI4Nzg1NTI5Njc5NzczNzU4.G-JvNS.7_RQMS0qLRsoJ3zACA2AnAF19LJruS_YWvpG4Y')