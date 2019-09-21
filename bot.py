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

# Magic 8ball. Ask the bot a question & get back an answer.
# Can trigger by typing 8ball or eightball (due to aliases)
@client.command(aliases=['8ball', 'eightball'])
async def _8ball(ctx, *, question):
    responses = [
        'It is certain.',
        'It is decidedly so.',
        'Without a doubt.',
        'Yes - definitely.',
        'You may rely on it.',
        'As I see it, yes.',
        'Most likely.',
        'Outlook good.',
        'Yes.',
        'Signs point to yes.',
        'Reply hazy, try again.',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        'Dont count on it.',
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.', 
        'Very doubtful.']

    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

# Command to clear messages from channel. Amount is the number of messages to clear.
@client.command()
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

# Command to kick a member from the channel.
@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)

# Command to ban a member from the channel.
@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {user.mention}')

# Command to un-ban a member from the channel.
@client.command()
async def unban(ctx, *, member):
    # Get all banned users.
    banned_users = await ctx.guild.bans()
    member_name, member_descriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.descriminator) == (member_name, member_descriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

# Run bot using token
client.run(bot_token)