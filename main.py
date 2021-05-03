import os

import discord
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot = commands.Bot(command_prefix=".", intents=intents)


@bot.command()
async def load(ctx, extension):
    if ctx.guild.owner == ctx.message.author:
        try:
            bot.load_extension(f"Cogs.{extension}")
            await ctx.send("Success!")
        except commands.errors.ExtensionAlreadyLoaded:
            await ctx.send("That extension is already loaded!")
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
    else:
        await ctx.send("You don't have access to this command")


for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"Cogs.{filename[:-3]}")

bot.run("ODAxMTkwMzcyNjU4MjQ5Nzg5.YAdErg.GhmrPslptekPnu70nn2ZwwwbYO8")
