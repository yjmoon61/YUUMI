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


class Summoner(commands.Cog):
    def __init__(self, client):
        self.client = client   
   
    @commands.command()
    async def opgg(self, ctx, *, args):
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

    @commands.command()
    async def profile(self, ctx, *, args):
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
    async def pretty(self, ctx, *, args):
        champion = str(args)
        temp_embed = discord.Embed(description=f"Fetching your profile, wait a moment...", color=0xfda5b0)
        temp_embed.set_thumbnail(url=f'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion}_1.jpg')
        msg = await ctx.send(embed=temp_embed)

        embed = discord.Embed(title=f'Profile: champion', description=f"Summary of the profile you asked for: \n \u200B", color=0xfda5b0)
        embed.set_thumbnail(url=f'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion}_1.jpg')
        embed.add_field(name='Summoner Level', value=f'hi \n \u200B')
        embed.add_field(name='\u200B', value='\u200B')
        embed.add_field(name='\u200B', value='\u200B')
        embed.add_field(name='Ranked (Solo/Duo)', value=f'hi \n \u200B')
        embed.add_field(name='\u200B', value='\u200B')
        embed.add_field(name='Ranked (Flex)', value=f'hi \n \u200B')
        embed.add_field(name='\u200B', value='\u200B')
        embed.add_field(name='Highest Champion Mastery', value=f'''
                        **[1]** test:,
                        **[2]** test:,
                        **[3]** test:,
                        \u200B''')
        embed.add_field(name='Live Game', value='hm')
        await asyncio.sleep(1)
        await msg.edit(embed=embed) 


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

    @commands.command()
    async def champ(self, ctx, *, args):
        champ = str(args)
        print(champ)
        Region = 'na1'
        DataDragonUrl = "https://ddragon.leagueoflegends.com/api/versions.json"

        PatchesData = urllib.request.urlopen(DataDragonUrl).read()
        Patches = json.loads(PatchesData)
        # print(Patches)
        CurrentPatch = Patches[1]
        # print(CurrentPatch)

        ChampionData = urllib.request.urlopen(f'http://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/data/en_US/champion.json').read()
        Champions = json.loads(ChampionData)
        print(Champions["data"]["Ahri"])

        res = None
        for sub in Champions['data']:
            if Champions['data'][sub]['id'].casefold() == champ:
                res = sub
                break
        key = Champions['data'][res]['key']
        print(key)
        await ctx.send(key)


            

def setup(client):
    client.add_cog(Summoner(client))