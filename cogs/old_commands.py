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


class Old_Commands(commands.Cog):
    def __init__(self, client):
        self.client = client   

    @commands.command()
    async def champ(self, ctx, *, args):
        champ = str(args)
        print(champ)
        Region = 'na1'
        DataDragonUrl = "https://ddragon.leagueoflegends.com/api/versions.json"

        PatchesData = urllib.request.urlopen(DataDragonUrl).read()
        Patches = json.loads(PatchesData)
        # print(Patches)
        CurrentPatch = Patches[0]
        # print(CurrentPatch)

        ChampionData = urllib.request.urlopen(f'http://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/data/en_US/champion.json').read()
        Champions = json.loads(ChampionData)
        # print(Champions["data"]["Ahri"])

        res = None
        for sub in Champions['data']:
            if Champions['data'][sub]['id'].casefold() == champ:
                res = sub
                break
        key = Champions['data'][res]['key']
        print(key)
        await ctx.send(key)

    @commands.command()
    async def basicprofile(self, ctx, *, args):
        """Basic username and level of summoner"""
        # STATS
        summoner = watcher.summoner.by_name('na1', args)
        print(summoner)
        stats = watcher.league.by_summoner('na1', summoner['id'])
        print(stats)
        summonerName = summoner['name']
        SummonerID = summoner['id']
        mastery = watcher.champion_mastery.by_summoner('na1', SummonerID)
        print("MASTERY")
        print(mastery)


        embed = discord.Embed(title='Profile')
        embed.add_field(name = 'Username', value= str(summonerName), inline = True)
        embed.add_field(name = 'Level', value = summoner['summonerLevel'], inline = True)

        embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def opgg(self, ctx, *, args):
        """Displays rank and stats of summoner"""
        # STATS
        summoner = watcher.summoner.by_name('na1', args)
        print(summoner)
        stats = watcher.league.by_summoner('na1', summoner['id'])
        print(stats)
        summonerPUUID = summoner['puuid']
        summonerID = summoner['accountId']
        summonerName = summoner['name']
        # Get the Solo Queue Values (find the Solo Queue Dictionary within stats)
        res = None
        for sub in stats:
            if sub['queueType'] == "RANKED_SOLO_5x5":
                res = sub
                break 
        n = stats.index(res)
        tier = stats[n]['tier']
        rank = stats[n]['rank']
        wins = int (stats[n]['wins'])
        losses = int (stats[n]['losses'])
        lp = stats[n]['leaguePoints']
        winrate = int (wins/(wins + losses) *100)

        

        # Discord Message Embed Style 
        embedgg = discord.Embed(
            title = f"{str(summonerName)}", 
            colour = discord.Colour.blue()
        )
        embedgg.add_field(name = 'Solo Queue Rank', value = f'{str(tier)} {str(rank)} with {str(lp)} LP and a {str(winrate)}% winrate', inline = False)

        await ctx.send(embed = embedgg)


def setup(client):
    client.add_cog(Old_Commands(client))