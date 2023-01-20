import discord
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.command(description="Sends the bot's latency.")
    async def test(self, ctx):
        await ctx.respond("Test successful!")


def setup(bot):
    bot.add_cog(Test(bot))
