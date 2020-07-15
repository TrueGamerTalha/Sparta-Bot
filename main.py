import discord
from discord.ext import commands

token = open("token.txt", "r").read()
prefix = "s!"
bot = commands.Bot(command_prefix=prefix,
                   description="Description yet to be added...")


@bot.event
async def on_ready():
    print("Bot is ready...")


@bot.event
async def on_member_join(member):
    channels = member.guild.channels

    for channel in channels:
        if "welcome" in str(channel):
            print(f"{member} has joined the server...")
            await channel.send(f"Welcome, {member.mention}, to the Official Sparta々Gaming Server")


@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hi, I am Sparta Bot!")


bot.run(token)
