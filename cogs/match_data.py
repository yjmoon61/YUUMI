from datetime import datetime
import discord
from discord.ext import commands
import json
import traceback
import re
import os
from dotenv import load_dotenv
from riotwatcher import LolWatcher
from discord import Embed, Member

import asyncio
import urllib

load_dotenv()
key = str(os.getenv('RIOT_API'))
watcher = LolWatcher(key)


class Match_Data(commands.Cog):
    def __init__(self, client):
        self.client = client   

    @commands.command()
    async def live(self, ctx, *, args):
        summonerWatch = watcher.summoner.by_name('na1', args)
        summonerName = summonerWatch['name']
        SummonerID = summonerWatch['id']
        liveGame = watcher.spectator.by_summoner('na1', SummonerID)
        print("LIVE GAME DETAILS")
        Participants = liveGame['participants']
        blueside = []
        redside = []
        for x in range(0,5):
            nameofSummoner = Participants[x]['summonerName']
            blueside.append(nameofSummoner)
            nameofSummoner2 = Participants[x+5]['summonerName']
            redside.append(nameofSummoner2)
        print(blueside)
        print(redside)

        # Discord Message Embed Style 
        embedgg = discord.Embed(
            title = f"{str(summonerName)}", 
            colour = discord.Colour.blue()
        )
        embedgg.add_field(name = 'Live Game', value = f'Blue Side Players: {*blueside, } || Red Side Players: {*redside, }', inline = False)

        await ctx.send(embed = embedgg)

def setup(client):
    client.add_cog(Match_Data(client))