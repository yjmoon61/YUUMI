import discord
from discord.ext import commands
import json
import traceback
import re
import os
from dotenv import load_dotenv

import urllib

load_dotenv()
version = str(os.getenv('VERSION'))

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client   
   
    @commands.command()
    async def repeat(self, ctx, message=None):
        message = message or "Hello ;)"
        author = ctx.author
        await ctx.send(f'{author} sent "{message}"')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    async def elisha(self, ctx):
        await ctx.send('Hi Elisha!')

    @commands.command()
    async def simplify(self, ctx):
        Region = 'na1'
        DataDragonUrl = "https://ddragon.leagueoflegends.com/api/versions.json"

        PatchesData = urllib.request.urlopen(DataDragonUrl).read()
        Patches = json.loads(PatchesData)
        # print(Patches)
        CurrentPatch = Patches[0]
        # print(CurrentPatch)

        Items = urllib.request.urlopen(f'http://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/data/en_US/item.json').read()
        itemData = json.loads(Items)
        itemlist2= [ (id,x['name'])  for id, x in itemData['data'].items() ]
        print(itemlist2)

        itemcount = list(itemData['data'].keys())
        for x in range(len(itemcount)):
            print(itemData['data'][itemcount[x]]['name'])

def setup(client):
    client.add_cog(Fun(client))