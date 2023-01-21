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
        user_data = self.bot.database.check_user_discord(ctx.author.id)
        if user_data:
            if user_data["connected"]:
                embed = discord.Embed(
                    title="Verification error",
                    description=f"You are already verified.",
                    color=discord.Color.red()
                )
                await ctx.respond(embed=embed, ephemeral=True)
                return
            elif user_data["timestamp"] > datetime.now():
                embed = discord.Embed(
                    title="Verification error",
                    description=f"You are already in verification process. "
                                f"Please wait until {user_data['timestamp'].strftime('%d/%m/%Y %H:%M:%S')}.",
                    color=discord.Color.red()
                )
                await ctx.respond(embed=embed, ephemeral=True)
                return

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
        user_response = user_response.json()

        user_data = self.bot.database.check_user_osu(user_response["id"])
        if user_data:
            if user_data["connected"]:
                embed = discord.Embed(
                    title="Verification error",
                    description=f"This osu! account is already verified.",
                    color=discord.Color.red()
                )
                await ctx.respond(embed=embed, ephemeral=True)
                return
            elif user_data["timestamp"] > datetime.now():
                embed = discord.Embed(
                    title="Verification error",
                    description=f"This osu! account is already in veryfication process. "
                                f"Please wait until {user_data['timestamp'].strftime('%d/%m/%Y %H:%M:%S')}.",
                    color=discord.Color.red()
                )
                await ctx.respond(embed=embed, ephemeral=True)
                return

        map_id = roll()
        map_response = requests.get(f"https://osu.ppy.sh/api/v2/beatmaps/{map_id}/",
                                    headers={"Authorization": f"Bearer {os.getenv('OSU_TOKEN')}"},
                                    )
        map_response = map_response.json()
        to_add = datetime(date.today().year, date.today().month, date.today().day, 15, 0, 0)
        timestamp = datetime.now() + timedelta(minutes=15)
        embed = discord.Embed(
            title=f"Verification {user_response['username']}",
            description="You started the verification process.",
            color=discord.Color.green()
        )
        embed.add_field(name="How to verify?",
                        value=f"To verify you account you have to play map that is shown below using No Fail then "
                              f"type '/complete'. You have to do that in 15 minutes."
                              f"\n**{timestamp.strftime('%d/%m/%Y %H:%M:%S')}**",
                        inline=False)
        embed.add_field(name="Map",
                        value=f"[osu! beatmap website]({map_response['url']})"
                              f"\nTitle: {map_response['beatmapset']['title']}"
                              f"\nArtist: {map_response['beatmapset']['artist']}"
                              f"\nMapper: {map_response['beatmapset']['creator']}"
                              f"\nDifficulty: {map_response['version']}")
        embed.set_image(url=map_response["beatmapset"]["covers"]["list@2x"])
        self.bot.database.verify(ctx.author.id, user_response["id"], map_id, timestamp)
        await ctx.respond(embed=embed, ephemeral=True)

    @discord.command(description="Verify your osu! account.")
    async def complete(self, ctx):
        user_data = self.bot.database.check_user_discord(ctx.author.id)
        if user_data:
            if user_data["connected"]:
                embed = discord.Embed(
                    title="Verification error",
                    description=f"You are already verified.",
                    color=discord.Color.red()
                )
                await ctx.respond(embed=embed, ephemeral=True)
                return
            elif user_data["timestamp"] > datetime.now():
                response = requests.get(f"https://osu.ppy.sh/api/v2/users/{user_data['osuId']}/scores/recent",
                                        headers={"Authorization": f"Bearer {os.getenv('OSU_TOKEN')}"})
                response = response.json()
                if str(response[0]["beatmap"]["id"]) == str(user_data["map"]) and "NF" in response[0]["mods"]:
                    self.bot.database.add_user(ctx.author.id, user_data["osuId"])
                    embed = discord.Embed(
                        title="Verification complete",
                        description=f"Your account is now verified.",
                        color=discord.Color.green()
                    )
                    await ctx.respond(embed=embed, ephemeral=True)
                    return
                else:
                    embed = discord.Embed(
                        title="Verification error",
                        description=f"You have not played the map that was shown in verification process or you are "
                                    f"not using NF.",
                        color=discord.Color.red()
                    )
                    await ctx.respond(embed=embed, ephemeral=True)
                    return
            else:
                embed = discord.Embed(
                    title="Verification error",
                    description=f"Time expired. Try to use '/verify' again.",
                    color=discord.Color.red()
                )
                await ctx.respond(embed=embed, ephemeral=True)
                return
        else:
            embed = discord.Embed(
                title="Verification error",
                description=f"You are not in verification process.\nTry to use '/verify' first.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return


def setup(bot):
    bot.add_cog(Verify(bot))
