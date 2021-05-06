import random

import discord
from discord.ext import commands


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

    @commands.command(aliases=["pp", "peepee", "ppsize"])
    async def penis(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        first_pp = database.child("Fun").child(f"{ctx.guild}_{ctx.guild.id}").child(
            str(user).replace("#", "_")).get().val() is None and ctx.message.author == user

        length = random.randint(0, 20)
        diagram = "8" + f"{'=' * length}" + "D"

        if first_pp:
            database.child("Fun").child(f"{ctx.guild}_{ctx.guild.id}").child(str(user).replace("#", "_")).set(
                {"First Penis Score": diagram})

        await ctx.send(f"{user.mention}'s penis size: {diagram}")

    @commands.command(aliases=["firstpp", "actuallpp", "actualpenis"])
    async def firstpenis(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        data = database.child("Fun").child(f"{ctx.guild}_{ctx.guild.id}").child(str(user).replace("#", "_")).get().val()
        if data is None:
            await ctx.send(f"{user.mention} has not used .pp yet")
        else:
            data = dict(data)
            await ctx.send(f"{user.mention}'s first penis score was: {data['First Penis Score']}")


def setup(bot):
    bot.add_cog(Fun(bot))
