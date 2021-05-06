import discord
from discord.ext import commands

from Utilities.xp_system import update_data, add_experience, level_up, sort_xp_data, ratelimit_check
from main import database


class XP_System(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cooldown = commands.CooldownMapping.from_cooldown(5.0, 60.0, commands.BucketType.user)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if not msg.author.bot:
            if ratelimit_check(self.cooldown, msg) is not None:
                return

            xp_data = database.child("XP Data").get().val()
            if xp_data is None:
                xp_data = {}
            else:
                xp_data = dict(xp_data)

            xp_data = await update_data(xp_data, msg.author, msg.guild)
            xp_data = await add_experience(xp_data, msg.author, msg.guild)
            xp_data = await level_up(xp_data, msg.author, msg.channel, msg.guild)

            database.child("XP Data").set(xp_data)

    @commands.command(aliases=["lvl", "rank"])
    async def level(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author

        xp_data = database.child("XP Data").get().val()
        if xp_data is None:
            xp_data = {}
        else:
            xp_data = sort_xp_data(dict(xp_data)[f"{ctx.guild}_{ctx.guild.id}"])

        try:
            user_level = xp_data[str(user).replace("#", "_")]["level"]
            user_experience = xp_data[str(user).replace("#", "_")]["experience"]
        except KeyError:
            user_level, user_experience = 1, 0
        try:
            user_rank = list(xp_data.keys()).index(str(user).replace("#", "_")) + 1
        except ValueError:
            user_rank = None
        xp_required_for_current_level = int(((user_level - 1) / 0.3) ** 2)
        xp_required_for_next_level = int((user_level / 0.3) ** 2)
        level_xp_total = xp_required_for_next_level - xp_required_for_current_level
        user_xp_in_current_level = user_experience - xp_required_for_current_level
        filled_boxes_number = int(((user_xp_in_current_level / level_xp_total) * 20) // 1)
        unfilled_boxes_number = 20 - filled_boxes_number
        progress_bar = f"{':blue_square:' * filled_boxes_number}{':white_large_square:' * unfilled_boxes_number}"

        embed = discord.Embed(
            title=f"{str(user)[:-5]}'s Ranking Statistics:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Name", value=str(user)[:-5], inline=True)
        embed.add_field(name="Total XP", value=str(user_experience), inline=True)
        embed.add_field(name="Messages Sent", value=str(int(user_experience / 5)), inline=True)
        embed.add_field(name="Level", value=str(user_level), inline=True)
        embed.add_field(name="Server Rank", value=str(user_rank), inline=True)
        embed.add_field(name="XP Before Level Up", value=str(level_xp_total - user_xp_in_current_level), inline=True)
        embed.add_field(name="Level Progress", value=progress_bar, inline=False)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["levels", "rankings", "lb"])
    async def leaderboard(self, ctx):
        xp_data = database.child("XP Data").get().val()
        if xp_data is None:
            xp_data = {}
        else:
            xp_data = sort_xp_data(dict(xp_data)[f"{ctx.guild}_{ctx.guild.id}"])

        embed = discord.Embed(
            title=f"'{ctx.guild}' Server Rankings:",
            color=discord.Color.blue()
        )

        for idx, (user, user_data) in enumerate(xp_data.items()):
            if idx == 20:
                break
            embed.add_field(name=f"{idx + 1}: {user[:-5]}",
                            value=f"Total XP: {user_data['experience']}\nCurrent Level: {user_data['level']}",
                            inline=False)
        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(XP_System(bot))
