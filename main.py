import os

import discord
import pyrebase
from discord.ext import commands

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot = commands.Bot(command_prefix=".", intents=intents)

config = {
    "apiKey": "AIzaSyBZ9Ts2by4Nf_yWHkmoiuYCAOopAKTGOlk",
    "authDomain": "discord-bot-bc11f.firebaseapp.com",
    "databaseURL": "https://discord-bot-bc11f-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "discord-bot-bc11f",
    "storageBucket": "discord-bot-bc11f.appspot.com",
    "messagingSenderId": "826213918460",
    "appId": "1:826213918460:web:b8f7cfab4d1cd7a3ef1979",
    "measurementId": "G-PPN082QXGT"
}
firebase = pyrebase.initialize_app(config)
database = firebase.database()


@bot.event
async def on_ready():
    print("The bot is now online!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): return
    if isinstance(error, commands.MemberNotFound): return
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
