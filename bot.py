import discord
from discord.ext import commands, tasks
from keys import bot_token, current_dir
import json
import random
import os
from itertools import cycle

# Make sure we are in the correct directory.
os.chdir(current_dir)

status = cycle(["Status 1", "Status 2", "Status 3", "Status 4"])

your_id = "ADD YOUR DISCORD ID HERE"

# Instance of the bot with a prefix.
client = commands.Bot(command_prefix=".")

# Check for ready state & change status/activity of bot.
@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.idle, activity=discord.Game("Admin Bot")
    )
    change_status.start()
    print("Bot is ready.")


# Handles error invalid command used.
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used.")


# Announce when member joins server.
# @client.event
# async def on_member_join(member):
#     print(f"{member} has joined a server.")


# Announce when member leaves server.
@client.event
async def on_member_remove(member):
    print(f"{member} has left a server.")


# Ping the bot.
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)} ms")


# Magic 8ball. Ask the bot a question & get back an answer.
# Can trigger by typing 8ball or eightball (due to aliases)
@client.command(aliases=["8ball", "eightball"])
async def _8ball(ctx, *, question):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Dont count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful.",
    ]

    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")


# Command to clear messages from channel. Amount is the number of messages to clear.
# Checks to make sure user has permissions.
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


# Check if the user issuing commands has the id set to your_id
def is_it_me(ctx):
    return ctx.author.id == your_id


# Custom check command that will test if is_it_me function is true.
# Use this as an example of a custom check using a function.
@client.command()
@commands.check(is_it_me)
async def custom_check(ctx):
    await ctx.send(f"Hi I am {ctx.author}")


# Error handling to specifically handle the clear command.
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify an amount of messages to delete.")


# Command to kick a member from the channel.
@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


# Command to ban a member from the channel.
@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {user.mention}")


# Command to un-ban a member from the channel.
@client.command()
async def unban(ctx, *, member):
    # Get all banned users.
    banned_users = await ctx.guild.bans()
    member_name, member_descriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.descriminator) == (member_name, member_descriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return


# Load a cog.
@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


# Unload a cog.
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")


# Reload a cog.
@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")


# Get all files within cogs directory with .py extension & load the cog.
def load_all_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # Remove the .py extension from the cog file while loading.
            client.load_extension(f"cogs.{filename[:-3]}")


# Call this when you what to load all cogs, if not comment out.
# load_all_cogs()

# Task that will change bot status every 10 seconds.
# Uses the status list to cycle different statuses.
@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


# Update user data when they join the channel.
@client.event
async def on_member_join(member):
    with open("users.json", "r") as f:
        users = json.load(f)

    await update_data(users, member)

    with open("users.json", "w") as f:
        json.dump(users, f)


# Update user data/experience/level when they send a message.
@client.event
async def on_message(message):
    with open("users.json", "r") as f:
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)

    with open("users.json", "w") as f:
        json.dump(users, f)


# Update user data including level & experience.
async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]["experience"] = 0
        users[user.id]["level"] = 1


# Add experience to a user.
async def add_experience(users, user, exp):
    users[user.id]["experience"] += exp


# Level up a user.
async def level_up(users, user, channel):
    experience = users[user.id]["experience"]
    lvl_start = users[user.id]["level"]
    lvl_end = int(experience ** (1 / 4))

    if lvl_start < lvl_end:
        await client.send(
            channel, "{} has leveled up to level {}".format(user.mention, lvl_end)
        )
        users[user.id]["level"] = lvl_end


# Run bot using token
client.run(bot_token)
