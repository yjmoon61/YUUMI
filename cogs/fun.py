import discord
from discord.ext import commands
import json
import traceback
import re
import os
from dotenv import load_dotenv

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
            

def setup(client):
    client.add_cog(Fun(client))