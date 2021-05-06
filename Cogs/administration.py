import asyncio

import discord
from discord.ext import commands


class Administration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["deletemsgs", "delmsgs", "delmessages", "deletemessages", "purgemsgs", "purgemessages"])
    async def purge(self, ctx, n, user: discord.Member = None):
        mod = 1 if user is None else 2
        if n == "all" or n == "max":
            n = len(await ctx.message.channel.history().flatten())
        if int(n) > (100 - mod):
            n = str(100 - mod)
        print(n)
        try:
            if not str(int(n)).isdigit(): return
        except ValueError:
            return
        messages = []
        for message in await ctx.message.channel.history(limit=int(n) + mod).flatten():
            messages.append(message) if message.author == user or user is None else None
        if ctx.message not in messages: messages.append(ctx.message)
        await ctx.message.channel.delete_messages(messages)
        if n == str(100 - mod): n += " (max)"
        bot_message = await ctx.send(f"Deleted {n} messages.")
        await asyncio.sleep(2)
        await bot_message.delete()


def setup(bot):
    bot.add_cog(Administration(bot))
