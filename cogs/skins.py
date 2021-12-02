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

import aiohttp
import DiscordUtils

load_dotenv()
key = str(os.getenv('RIOT_API'))
watcher = LolWatcher(key)


class Skins(commands.Cog):
    def __init__(self, client):
        self.client = client   

    @commands.command()
    async def paginate(self, ctx):
        embed1 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 1")
        embed2 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 2")
        embed3 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 3")
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
        paginator.add_reaction('⏮️', "first")
        paginator.add_reaction('⏪', "back")
        paginator.add_reaction('🔐', "lock")
        paginator.add_reaction('⏩', "next")
        paginator.add_reaction('⏭️', "last")
        embeds = [embed1, embed2, embed3]
        await paginator.run(embeds)

    @commands.command()
    async def skins(self, ctx, *, args):
        champ =str(args)
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

        for sub in Champions['data']:
            if Champions['data'][sub]['id'].casefold() == champ.casefold():
                properName = Champions['data'][sub]['id']
        # print(properName)

        oneChampData = urllib.request.urlopen(f'https://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/data/en_US/champion/{properName}.json').read()
        oneChamp = json.loads(oneChampData)

        skincount = []
        skinname = []
        for x in range(len(oneChamp['data'][properName]['skins'])):
            skincount.append(oneChamp['data'][properName]['skins'][x]['num'])
            skinname.append(oneChamp['data'][properName]['skins'][x]['name'])


        
        embeds = []
        for x in range(len(skincount)):
            imageURL = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{properName}_{skincount[x]}.jpg"
            embedNew = discord.Embed(color=ctx.author.color).add_field(name=f"{properName} Skin #{x+1} out of {len(skincount)}", value=f"{skinname[x]}")
            embedNew.set_image(url=imageURL)
            embeds.append(embedNew)
    
        paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
        await paginator.run(embeds)

    @commands.command()
    async def tiles(self, ctx, *, args):
        champ =str(args)
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

        for sub in Champions['data']:
            if Champions['data'][sub]['id'].casefold() == champ:
                properName = Champions['data'][sub]['id']
        # print(properName)

        oneChampData = urllib.request.urlopen(f'https://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/data/en_US/champion/{properName}.json').read()
        oneChamp = json.loads(oneChampData)

        skincount = []
        skinname = []
        for x in range(len(oneChamp['data'][properName]['skins'])):
            skincount.append(oneChamp['data'][properName]['skins'][x]['num'])
            skinname.append(oneChamp['data'][properName]['skins'][x]['name'])


        
        embeds = []
        for x in range(len(skincount)):
            imageURL = f"https://ddragon.leagueoflegends.com/cdn/img/champion/tiles/{properName}_{skincount[x]}.jpg"
            embedNew = discord.Embed(color=ctx.author.color).add_field(name=f"{properName} Tile #{x+1} out of {len(skincount)}", value=f"{skinname[x]}")
            embedNew.set_image(url=imageURL)
            embeds.append(embedNew)
    
        paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
        await paginator.run(embeds)


def setup(client):
    client.add_cog(Skins(client))