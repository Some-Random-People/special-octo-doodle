import discord
from discord.ext import commands


class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.command(description="Sends a nice message to user")
    async def hello(self, ctx):
        await ctx.respond("Hello!")

    @discord.command(description="Checks latency")
    async def ping(self, ctx):
        print(self.bot.latency)
        await ctx.respond(f"Pong! Latency is {round(self.bot.latency*1000)}ms")


def setup(bot):
    bot.add_cog(Hello(bot))