import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
from Functions.roll_beatmap import roll
from datetime import datetime, date, timedelta

load_dotenv(find_dotenv())


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.command(description="Verify your osu! account.")
    async def verify(self, ctx, osu_userid: str):
        map_id = roll()
        user_response = requests.get(f"https://osu.ppy.sh/api/v2/users/{osu_userid}/",
                                     headers={"Authorization": f"Bearer {os.getenv('OSU_TOKEN')}"},
                                     )
        if user_response.status_code == 404:
            embed = discord.Embed(
                title="Verification error",
                description=f"User with user id {osu_userid} not found.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return
        map_response = requests.get(f"https://osu.ppy.sh/api/v2/beatmaps/{map_id}/",
                                    headers={"Authorization": f"Bearer {os.getenv('OSU_TOKEN')}"},
                                    )
        map_response = map_response.json()
        user_response = user_response.json()
        to_add = datetime(date.today().year, date.today().month, date.today().day, 15, 0, 0)
        timestamp = datetime.now() + timedelta(minutes=15)
        timestamp = timestamp.strftime("%d/%m/%Y %H:%M:%S")
        embed = discord.Embed(
            title=f"Verification {user_response['username']}",
            description="You started the verification process.",
            color=discord.Color.green()
        )
        embed.add_field(name="How to verify?", value=f"To verify you account you have to play map that is shown below. "
                                                     f"You have to do that in 15 minutes. {timestamp}", inline=False)
        embed.add_field(name="Map", value=f"[osu! beatmap website]({map_response['url']})"
                                          f"\nTitle: {map_response['beatmapset']['title']}"
                                          f"\nArtist: {map_response['beatmapset']['artist']}"
                                          f"\nMapper: {map_response['beatmapset']['creator']}"
                                          f"\nDifficulty: {map_response['version']}")
        embed.set_image(url=map_response["beatmapset"]["covers"]["list@2x"])

        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Verify(bot))
