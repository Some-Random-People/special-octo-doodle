import os
from dotenv import load_dotenv, find_dotenv
import discord

load_dotenv(find_dotenv())
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

bot.run(os.getenv('TOKEN'))