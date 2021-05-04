import os

import discord
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot = commands.Bot(command_prefix=".", intents=intents)


@bot.event
async def on_ready():
    print("The bot is now online!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): return
    raise error


@bot.command()
async def load(ctx, extension):
    if ctx.guild.owner == ctx.message.author:
        try:
            bot.load_extension(f"Cogs.{extension}")
            await ctx.send("Success!")
        except commands.errors.ExtensionAlreadyLoaded:
            await ctx.send("That extension is already loaded!")
        except commands.errors.ExtensionNotFound:
            await ctx.send("That extension does not exist!")
    else:
        await ctx.send("You don't have access to this command")


@bot.command()
async def unload(ctx, extension):
    if ctx.guild.owner == ctx.message.author:
        try:
            bot.unload_extension(f"Cogs.{extension}")
            await ctx.send("Success!")
        except commands.errors.ExtensionNotLoaded:
            await ctx.send("That extension is already unloaded!")
        except commands.errors.ExtensionNotFound:
            await ctx.send("That extension does not exist!")
    else:
        await ctx.send("You don't have access to this command")


for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"Cogs.{filename[:-3]}")

bot.run(os.environ.get('SECRET_KEY'))
