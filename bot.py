import discord
from discord.ext import commands
from keys import bot_token

# Instance of the bot with a prefix.
client = commands.Bot(command_prefix = '.')

# Check for ready state
@client.event 
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')


# Run bot using token
client.run(bot_token)