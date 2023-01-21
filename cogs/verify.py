import os
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.command(description="Verify your osu! account.")
    async def verify(self, ctx, osu_userid: str):
        response = requests.get(f"https://osu.ppy.sh/api/v2/users/{osu_userid}/",
                                headers={"Authorization": f"Bearer {os.getenv('OSU_TOKEN')}"},
                                )
        response = response.json()
        embed = discord.Embed(
            title=f"Verification {response['username']}",
            description="You started the verification process.",
            color=discord.Color.green()
        )
        embed.add_field(name="How to verify?", value="To verify you account you have to play map that is shown below. "
                                                     "You have to do that in 15 minutes.", inline=False)
        embed.add_field(name="Map", value=f"Name: Example name \nArtist: Example artist \nMapper: Example mapper \n"
                                          f"Difficulty: Example difficulty \n"
                                          f"[Website](https://osu.ppy.sh/beatmapsets/842412#osu/1762733)")
        embed.set_image(url="https://assets.ppy.sh/beatmaps/842412/covers/list@2x.jpg?1650668705")

        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Verify(bot))
