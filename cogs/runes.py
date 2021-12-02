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
import urllib

load_dotenv()
key = str(os.getenv('RIOT_API'))
watcher = LolWatcher(key)


class Runes(commands.Cog):
    def __init__(self, client):
        self.client = client   

    @commands.command()
    async def runes(self, ctx, *, args):
        # STATS
        Region = 'na1'
        DataDragonUrl = "https://ddragon.leagueoflegends.com/api/versions.json"
        masteriesGrabbing = 10
        summoner = watcher.summoner.by_name(Region, args)
        print(summoner)
        summonerName = summoner['name']
        SummonerID = summoner['id']
        stats = watcher.league.by_summoner(Region, SummonerID)
        print(stats)
        mastery = watcher.champion_mastery.by_summoner(Region, SummonerID)
        print("MASTERY")
        print(mastery)
        champPoints = []
        champId = []
        # Conviently already sorted in highest to lowest mastery order
        for x in range(masteriesGrabbing):
            nameofSummoner = mastery[x]['championPoints']
            champPoints.append(nameofSummoner)
            champidentification = mastery[x]['championId']
            champId.append(champidentification)
            

        PatchesData = urllib.request.urlopen(DataDragonUrl).read()
        Patches = json.loads(PatchesData)
        print(Patches)
        CurrentPatch = Patches[0]
        print(CurrentPatch)
        
        RuneData = urllib.request.urlopen(f'https://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/data/en_US/runesReforged.json').read()
        Runes = json.loads(RuneData)
        # print(Champions)

        print("Runes")
        for i in range(len(Runes)):
            text = Runes[i]['key']
            print(f'{text},', end ="")
            text = Runes[i]['key']
            print(f'\:{text}:,', end="")
            text = Runes[i]['id']
            print(f'{text}')
            for sub1 in range(len(Runes[i]['slots'])):
                for sub2 in range(len(Runes[i]['slots'][sub1]['runes'])):
                    text = Runes[i]['slots'][sub1]['runes'][sub2]['key']
                    print(f'{text},', end ="")
                    text = Runes[i]['slots'][sub1]['runes'][sub2]['key']
                    print(f'\:{text}:,', end="")
                    text = Runes[i]['slots'][sub1]['runes'][sub2]['id']
                    print(f'{text}')

        runeEmojiId = []
        
        with open('data/runesReforged.json', encoding='utf-8') as f:
            emojis = json.load(f)
        for i in range(len(emojis)):
            for e in emojis:
                emoji_value = e['EMOJICODE']
                runeEmojiId.append(emoji_value)
        f.close()


        embed = discord.Embed(
            title='Profile',
            colour = 16742893
        )
        embed.add_field(name = 'Username', value= str(summonerName), inline = True)
        embed.add_field(name = 'Level', value = summoner['summonerLevel'], inline = True)
        for i in range(20):
            embed.add_field(name = f'{runeEmojiId[i]}', value = '\u200b', inline = False)
        embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)


        await ctx.send(embed=embed)

    @commands.command()
    async def sumspells(self, ctx, *, args):
        # STATS
        Region = 'na1'
        DataDragonUrl = "https://ddragon.leagueoflegends.com/api/versions.json"
        masteriesGrabbing = 10
        summoner = watcher.summoner.by_name(Region, args)
        print(summoner)
        summonerName = summoner['name']
        SummonerID = summoner['id']
        stats = watcher.league.by_summoner(Region, SummonerID)
        print(stats)
        mastery = watcher.champion_mastery.by_summoner(Region, SummonerID)
        print("MASTERY")
        print(mastery)
        champPoints = []
        champId = []
        # Conviently already sorted in highest to lowest mastery order
        for x in range(masteriesGrabbing):
            nameofSummoner = mastery[x]['championPoints']
            champPoints.append(nameofSummoner)
            champidentification = mastery[x]['championId']
            champId.append(champidentification)
            

        PatchesData = urllib.request.urlopen(DataDragonUrl).read()
        Patches = json.loads(PatchesData)
        print(Patches)
        CurrentPatch = Patches[0]
        print(CurrentPatch)
        
        SummData = urllib.request.urlopen(f'https://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/data/en_US/summoner.json').read()
        SummonerSpells = json.loads(SummData)
        # print(Champions)

        print("SummonerSpells")
        for sub in SummonerSpells['data']:
            text = SummonerSpells['data'][sub]['id']
            print(f'{text},', end ="")
            text = SummonerSpells['data'][sub]['id']
            print(f'\:{text}:,', end="")
            text = SummonerSpells['data'][sub]['key']
            print(f'{text}')

        """ runeEmojiId = []
        
        with open('data/runesReforged.json', encoding='utf-8') as f:
            emojis = json.load(f)
        for i in range(len(emojis)):
            for e in emojis:
                emoji_value = e['EMOJICODE']
                runeEmojiId.append(emoji_value)
        f.close() """


        embed = discord.Embed(
            title='Profile',
            colour = 16742893
        )
        embed.add_field(name = 'Username', value= str(summonerName), inline = True)
        embed.add_field(name = 'Level', value = summoner['summonerLevel'], inline = True)
        """         for i in range(20):
            embed.add_field(name = f'{runeEmojiId[i]}', value = '\u200b', inline = False) """
        embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)


        await ctx.send(embed=embed)
            

def setup(client):
    client.add_cog(Runes(client))