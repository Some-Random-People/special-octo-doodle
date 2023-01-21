import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Pp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.command(description="Checks player's pp")
    async def pp(self, ctx, userid: str):
        response = requests.get(f"https://osu.ppy.sh/api/v2/users/{userid}/",
                                headers={"Authorization": f"Bearer {os.getenv('OSU_TOKEN')}"},
                                )
        await ctx.respond(response.json()["statistics"]["pp"])

    @discord.command(description = "Show profile")
    async def profile(self, ctx, userid: str):
        response = requests.get(f"https://osu.ppy.sh/api/v2/users/{userid}/",
                                headers={"Authorization": f"Bearer {os.getenv('OSU_TOKEN')}"},
                                )

        if response.status_code == 404:
            embed = discord.Embed(
                title="Verification error",
                description=f"User with user id {userid} not found.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return

        response = response.json()
        if response["is_active"]:
            active_status = ":green_circle:"
        else:
            active_status = ":red_circle:"
        if response["is_online"]:
            online_status = ":green_circle:"
        else:
            online_status = ":red_circle:"



        embed = discord.Embed(
            title=userid + "'s Profile",
            description=f":flag_{response['country_code'].lower()}:",
            color = discord.Colour.blurple(),
        )
        embed.add_field(name="Active", value=active_status, inline=True)
        embed.add_field(name="Online", value=online_status, inline=True)
        embed.add_field(name="", value="")
        embed.add_field(name="Stats", value=f"Global Rank: {response['statistics']['global_rank']}"
                                            f"\nCountry Rank: {response['statistics']['country_rank']}"
                                            f"\nPP: {response['statistics']['pp']}"
                                            f"\nPlaytime: {response['statistics']['play_time']//3600}h"
                    )

        embed.set_thumbnail(url=response["avatar_url"])

        await ctx.respond("Hello! Here's a cool embed.", embed=embed)


def setup(bot):
    bot.add_cog(Pp(bot))