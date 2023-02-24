import discord
from discord.ext import commands


class Top(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    rank = discord.SlashCommandGroup("rank", "Check out what has changed")

    @rank.command()
    async def world(self, ctx):
        await ctx.respond("test")

    #@rank.command()
    #async def country(self, ctx):



def setup(bot):
    bot.add_cog(Top(bot))