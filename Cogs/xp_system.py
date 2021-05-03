import json

from discord.ext import commands

from Utilities.xp_system import update_data, add_xp, level_up


class XP_System(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("server_xp_data.json", "r+") as f:
            data = json.load(f)

        await update_data(data, member)

        with open("server_xp_data.json", "w+") as f:
            json.dump(data, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        with open("server_xp_data.json", "r+") as f:
            data = json.load(f)

        await update_data(data, str(message.author))
        await add_xp(data, str(message.author), 5)
        await level_up(data, str(message.author))

        with open("server_xp_data.json", "w+") as f:
            json.dump(data, f)


def setup(bot):
    bot.add_cog(XP_System(bot))
