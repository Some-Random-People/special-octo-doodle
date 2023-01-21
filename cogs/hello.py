import discord
from discord.ext import commands


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.command(description="Sends a nice message to user")
    async def hello(self, ctx):
        await ctx.respond(self.bot.database.asd())


def setup(bot):
    bot.add_cog(Hello(bot))