import random

import discord
from discord.ext import commands

from Utilities.kahoot import KahootBot
from main import database


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["eightball", "8ball", "8-ball"])
    async def eight_ball(self, ctx, question):
        responses = '''As I see it, yes.
                  Ask again later.
                  Better not tell you now.
                  Cannot predict now.
                  Concentrate and ask again.
                  Don’t count on it.
                  It is certain.
                  It is decidedly so.
                  Most likely.
                  My reply is no.
                  My sources say no.
                  Outlook not so good.
                  Outlook good.
                  Reply hazy, try again.
                  Signs point to yes.
                  Very doubtful.
                  Without a doubt.
                  Yes.
                  Yes – definitely.
                  You may rely on it.'''.split("\n")
        answer = random.choice(responses)
        await ctx.send(answer)

    @commands.command(aliases=["kahootbot", "kbot"])
    async def kahoot(self, ctx, *args):
        _vars = [None, None, None, 0.0, 0.0, False]
        for idx, (arg, var) in enumerate(zip(args, _vars)):
            _vars[idx] = arg
        if None in _vars[:3]:
            raise commands.errors.MissingRequiredArgument() from None
        username, game_pin, game_id, max_delay, min_delay, debug = _vars
        kahoot_bot = KahootBot(debug=debug, minimum_answer_delay=min_delay, maximum_answer_delay=max_delay)
        if debug:
            warning_msg = await ctx.send(
                "Client Message: [Warning] --> If the bot fails, please note: This bot only works with public "
                "kahoots, and it can only answer True/False and Quiz Type questions.")
            await warning_msg.delete(delay=5)
            async for message in kahoot_bot.play_game(username, game_pin, game_id):
                bot_msg = await ctx.send(message)
                await bot_msg.delete(delay=5)


def setup(bot):
    bot.add_cog(Fun(bot))
