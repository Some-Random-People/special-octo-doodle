import os
import mongo
from dotenv import load_dotenv, find_dotenv
import discord

load_dotenv(find_dotenv())
bot = discord.Bot()
cogs_list = [
    "users_req",
    "hello",
    "verify",
    "recent"
]

bot.database = mongo.Mon()
bot.database.connect()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')


bot.run(os.getenv("TOKEN"))
