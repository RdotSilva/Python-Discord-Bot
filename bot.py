import discord
from discord.ext import commands

# Instance of the bot with a prefix.
client = commands.Bot(command_prefix = '.')

# Check for ready state
@client.event 
async def on_ready():
    print('Bot is ready.')