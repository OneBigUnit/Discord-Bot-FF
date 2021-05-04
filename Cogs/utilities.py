import discord
from discord.ext import commands


class Utilities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ping"])
    async def latency(self, ctx):
        latency = self.bot.latency

        if latency <= 50:
            colour = discord.Color.green
        elif latency > 300:
            colour = discord.Color.red
        else:
            colour = discord.Color.orange

        embed = discord.Embed(
            title="Bot Latency Test",
            color=colour()
        )
        embed.add_field(name="Latency", value=f"{round(latency, 2)}ms", inline=True)
        embed.set_thumbnail(
            url="https://media.istockphoto.com/vectors/wifi-icon-on-black-background-black-flat-style-vector"
                "-illustration-vector-id1170032746?k=6&m=1170032746&s=170667a&w=0&h=HaCvZNq"
                "-lI3FIzIM2Z9QO6mR0qrQQ443if2m6xQeS94=")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utilities(bot))
