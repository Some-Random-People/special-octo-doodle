import os
from dotenv import load_dotenv, find_dotenv
import discord

load_dotenv(find_dotenv())

bot = discord.Bot()

bot.run(os.getenv('TOKEN'))
