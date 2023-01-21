import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.command(description="Sends the bot's latency.")
    async def test(self, ctx, userid: str):
        response = requests.get(f"https://osu.ppy.sh/api/v2/users/{userid}/",
                                headers={"Authorization": f"Bearer {os.getenv('OSU_TOKEN')}"},
                                )
        await ctx.respond(response.json()["statistics"]["pp"])


def setup(bot):
    bot.add_cog(Test(bot))
