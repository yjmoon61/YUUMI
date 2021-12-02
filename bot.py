import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext import tasks
import asyncio
import os
import urllib
import json

load_dotenv()
token = str(os.getenv('TOKEN'))

client = commands.Bot(command_prefix='y- ')

@tasks.loop(seconds=20.0)
async def my_background_task():
    DataDragonUrl = "https://ddragon.leagueoflegends.com/api/versions.json"
    PatchesData = urllib.request.urlopen(DataDragonUrl).read()
    Patcher = json.loads(PatchesData)
    cPatch = Patcher[0]
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='y- help'))
    await asyncio.sleep(10)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'on patch: {cPatch}'))

@client.event
async def on_ready():
    print("Yuumi is up and running <3")
    await client.wait_until_ready()
    my_background_task.start()

client.load_extension('cogs.fun')
client.load_extension('cogs.in_game_builds')
client.load_extension('cogs.runes')
client.load_extension('cogs.match_data')
client.load_extension('cogs.profiles')
client.load_extension('cogs.skins')
client.load_extension('cogs.leaderboard')

client.run(token)