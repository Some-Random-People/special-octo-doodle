import os
import mongo
from dotenv import load_dotenv, find_dotenv
import discord
from discord.ext import commands

load_dotenv(find_dotenv())
bot = discord.Bot()
cogs_list = [
    "users_req",
    "hello",
    "verify",
    "recent",
    "top"
]

bot.database = mongo.Mon()
bot.database.connect()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("This command is currently on cooldown.", ephemeral=True)
    else:
        raise error

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')


bot.run(os.getenv("TOKEN"))
