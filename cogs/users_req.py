import os
import discord
import requests
from Functions.rank_plot import plots
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


# All Api about user requests are here
class Users_req(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.command(description="Checks player's pp")
    async def pp(self, ctx, userid: str):
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
        await ctx.respond(f"{userid}'s pp: {response.json()['statistics']['pp']}", ephemeral=True)

    @discord.command(description="Show profile")
    async def profile(self, ctx, userid: str):
        response = requests.get(f"https://osu.ppy.sh/api/v2/users/{userid}",
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
        userid_num = response["id"]
        best_score = requests.get(f"https://osu.ppy.sh/api/v2/users/{userid_num}/scores/best",
                                  headers={"Authorization": f"Bearer {os.getenv('OSU_TOKEN')}"})
        best_score = best_score.json()

        if response["is_active"]:
            active_status = ":green_circle:"
        else:
            active_status = ":red_circle:"
        if response["is_online"]:
            online_status = ":green_circle:"
        else:
            online_status = ":red_circle:"

        plots(response["rank_history"]["data"])

        embed = discord.Embed(
            title="",
            description=f"[:flag_{response['country_code'].lower()}: {response['country']['name']}](https://osu.ppy.sh/rankings/osu/performance?country={response['country_code']})",
            color=discord.Colour.nitro_pink()
        )

        if response['playstyle']:
            playstyle = ""
            for x in response['playstyle']:
                playstyle += x
                playstyle += ", "
            playstyle = playstyle[:-2]
        else:
            playstyle = "Not set"

        embed.add_field(name="Active", value=active_status, inline=True)
        embed.add_field(name="Online", value=online_status, inline=True)
        embed.add_field(name="", value="")
        embed.add_field(name="Stats", value=f"Global Rank: {response['statistics']['global_rank']}"
                                            f"\nCountry Rank: {response['statistics']['country_rank']}"
                                            f"\nPP: {response['statistics']['pp']}"
                                            f"\nPlaytime: {response['statistics']['play_time'] // 3600}h"
                                            f"\nAccuracy: {round(response['statistics']['hit_accuracy'],2)}%"
                                            f"\nPlaystyle: {playstyle}"
                                            f"\nTop play: {best_score[0]['pp']} pp"
                        )
        embed.add_field(name="Grades", value=f"<:ssh:1078792293072506961> {response['statistics']['grade_counts']['ssh']}"
                                             f"\n<:ss:1078793122626154546> {response['statistics']['grade_counts']['ss']}"   
                                             f"\n<:sh:1078793120499650650> {response['statistics']['grade_counts']['sh']}"
                                             f"\n<:s_:1078793117651697844> {response['statistics']['grade_counts']['s']}"
                                             f"\n<:a_:1078793108571037868> {response['statistics']['grade_counts']['a']}"
                        )

        embed.set_thumbnail(url=response["avatar_url"])
        file = discord.File("./Temp/plot.png", filename="plot.png")
        embed.set_image(url="attachment://plot.png")
        embed.set_author(name=response['username'] + "'s Profile", url=f"https://osu.ppy.sh/users/{userid_num}")
        await ctx.respond(file=file, embed=embed)


def setup(bot):
    bot.add_cog(Users_req(bot))
