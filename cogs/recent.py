import os
import discord
import requests
from Functions.map_pp_stats import calculate_pp, calculate_ss_pp
from Functions.name_to_id import name_to_id
from discord.ext import commands
from discord.commands import Option
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Recent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.command(description="Shows recent play")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def recent(self, ctx, osu_userid: Option(str, "Enter osu user id", required=False)):
        if not osu_userid:
            user_data = self.bot.database.check_user_discord(ctx.author.id)
            if not user_data or not user_data["connected"]:
                await ctx.respond(f"Try to verify using /verify or enter osu user id using /recent <osu user id>",
                                  ephemeral=True)
                return
            osu_userid = user_data["osuId"]
        else:
            osu_userid = name_to_id(osu_userid)
        recent_play = requests.get(f"https://osu.ppy.sh/api/v2/users/{osu_userid}/scores/recent",
                                    headers={"Authorization": f"Bearer {os.getenv('OSU_TOKEN')}"},
                                    )
        if recent_play.status_code == 404:
            embed = discord.Embed(
                title="Verification error",
                description=f"User with user id {osu_userid} not found.",
                color=discord.Color.red()
            )
            await ctx.respond(embed=embed, ephemeral=True)
            return
        recent_play = recent_play.json()
        if recent_play:
            mods = recent_play[0]["mods"]
            mods_str = " "
            if mods:
                mods_str = " +"
                for x in mods:
                    mods_str += x
            embed = discord.Embed(
                title=f"{recent_play[0]['user']['username']}'s recent play",
                description=f"**{recent_play[0]['beatmapset']['title']} [{recent_play[0]['beatmap']['version']}]"
                            f"{mods_str} [{recent_play[0]['beatmap']['difficulty_rating']}🟊]**",
                color=discord.Color.green()
            )
            text = ""
            map_id = recent_play[0]["beatmap"]["id"]
            counmt_300 = recent_play[0]["statistics"]["count_300"]
            count_100 = recent_play[0]["statistics"]["count_100"]
            count_50 = recent_play[0]["statistics"]["count_50"]
            count_miss = recent_play[0]["statistics"]["count_miss"]
            if mods.count("FL") > 0 or mods.count("HT") > 0 or mods.count("NF") > 0:
                text += "PP counting for this mod is not supported yet\n"
                performance_max = calculate_ss_pp(map_id, mods)
            else:
                performance, performance_max = calculate_pp(map_id, recent_play[0]["max_combo"], counmt_300,
                                                            count_100, count_50, count_miss, mods)
                text += f"PP: {round(performance.pp, 2)} / {round(performance_max.pp, 2)}\n"
            text += f"Accuracy: {round(recent_play[0]['accuracy'] * 100, 2)}\n"
            text += f"Combo: {recent_play[0]['max_combo']} / {performance_max.difficulty.max_combo}\n"
            text += f"Score: {recent_play[0]['score']}\n"
            text += f"300/100/50/X: {counmt_300}/{count_100}/{count_50}/{count_miss}\n"
            text += f"Rank: :regional_indicator_{recent_play[0]['rank'].lower()}:\n"
            embed.add_field(name="", value=text, inline=False)
            embed.set_image(url=recent_play[0]["beatmapset"]["covers"]["cover@2x"])
            embed.set_thumbnail(url=recent_play[0]["user"]["avatar_url"])
            await ctx.respond(embed=embed)
        else:
            await ctx.respond(f"No recent play")
        return


def setup(bot):
    bot.add_cog(Recent(bot))
