import discord
from discord.ext import commands
from keys import bot_token
import random

# Instance of the bot with a prefix.
client = commands.Bot(command_prefix = '.')

# Check for ready state
@client.event 
async def on_ready():
    print('Bot is ready.')

# Announce when member joins server.
@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

# Announce when member leaves server.
@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

# Ping the bot.
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')


@client.command(aliases=['8ball', 'eightball'])
async def _8ball(ctx, *, question):
    

    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


# Run bot using token
client.run(bot_token)