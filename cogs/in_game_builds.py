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

import DiscordUtils

load_dotenv()
key = str(os.getenv('RIOT_API'))
watcher = LolWatcher(key)


class In_Game_Builds(commands.Cog):
    def __init__(self, client):
        self.client = client   

    @commands.command()
    async def all_live(self, ctx, *, args):
        summonerWatch = watcher.summoner.by_name('na1', args)
        summonerName = summonerWatch['name']
        SummonerID = summonerWatch['id']
        liveGame = watcher.spectator.by_summoner('na1', SummonerID)
        print(liveGame)
        print("LIVE GAME DETAILS")
        Participants = liveGame['participants']
        summnames = []
        runes = []
        runestyles = []
        summspells = []
        champids = []

        for i in range(10):
            nameofSummoner = Participants[i]['summonerName']
            summnames.append(nameofSummoner)
            for j in range(len(Participants[i]['perks']['perkIds'])):
                runes.append(Participants[i]['perks']['perkIds'][j])
            runestyles.append(Participants[i]['perks']['perkStyle'])
            runestyles.append(Participants[i]['perks']['perkSubStyle'])
            summspells.append(Participants[i]['spell1Id'])
            summspells.append(Participants[i]['spell2Id'])
            champids.append(Participants[i]['championId'])

        runeEmojiIds = []
        runestyleEmojiIds = []
        summspellEmojiIds = []
        champidEmojiIds= []
        
        with open('data/runesReforged.json', encoding='utf-8') as f:
            emojis = json.load(f)
        for i in range(len(runes)):
            for e in emojis:
                if int(e['KEY']) == runes[i]:
                    emoji_value = e['EMOJICODE']
                    runeEmojiIds.append(emoji_value)
        for i in range(len(runestyles)):
            for e in emojis:
                if int(e['KEY']) == runestyles[i]:
                    emoji_value = e['EMOJICODE']
                    runestyleEmojiIds.append(emoji_value)
        f.close()

        with open('data/summonerspells.json', encoding='utf-8') as f:
            emojis = json.load(f)
        for i in range(len(summspells)):
            for e in emojis:
                if int(e['KEY']) == summspells[i]:
                    emoji_value = e['EMOJICODE']
                    summspellEmojiIds.append(emoji_value)
        f.close()

        with open('data/championicons.json', encoding='utf-8') as f:
            emojis = json.load(f)
        for i in range(len(champids)):
            for e in emojis:
                if int(e['KEY']) == champids[i]:
                    emoji_value = e['EMOJICODE']
                    champidEmojiIds.append(emoji_value)
        f.close()


        # Discord Message Embed Style
        embeds = []
        for i in range(5):
            embedNew = discord.Embed(title = f"{str(summonerName)}\'s live game", 
            colour = 16742893).add_field(name = f'Blue Side Player {i+1}\'s Summoner Name:', value = f'{summnames[i]}')
            embedNew.add_field(name='\u200B', value='\u200B')
            embedNew.add_field(name='\u200B', value='\u200B')
            embedNew.add_field(name = f'Champion:', value = f'{champidEmojiIds[i]}')
            embedNew.add_field(name='\u200B', value='\u200B')
            embedNew.add_field(name = f'Summoner Spells:', value = f'{summspellEmojiIds[2*i]} and {summspellEmojiIds[2*i+1]}')
            embedNew.add_field(name = f'Main tree: {runestyleEmojiIds[2*i]}', value = f'{runeEmojiIds[9*i]} {runeEmojiIds[9*i + 1]} {runeEmojiIds[9*i + 2]} {runeEmojiIds[9*i + 3]}')
            embedNew.add_field(name='\u200B', value='\u200B')
            embedNew.add_field(name = f'Secondary tree: {runestyleEmojiIds[2*i+1]}', value = f'{runeEmojiIds[9*i+4]} and {runeEmojiIds[9*i+5]}')
            embeds.append(embedNew)
        for i in range(5):
            embedNew = discord.Embed(title = f"{str(summonerName)}\'s live game", 
            colour = 16742893).add_field(name = f'Red Side Player {i+1}\'s Summoner Name:', value = f'{summnames[i+5]}')
            embedNew.add_field(name='\u200B', value='\u200B')
            embedNew.add_field(name='\u200B', value='\u200B')
            embedNew.add_field(name = f'Champion:', value = f'{champidEmojiIds[i+5]}')
            embedNew.add_field(name='\u200B', value='\u200B')
            embedNew.add_field(name = f'Summoner Spells:', value = f'{summspellEmojiIds[2*i+10]} and {summspellEmojiIds[2*i+11]}')
            embedNew.add_field(name = f'Main tree: {runestyleEmojiIds[2*i+10]}', value = f'{runeEmojiIds[9*i+45]} {runeEmojiIds[9*i + 46]} {runeEmojiIds[9*i + 47]} {runeEmojiIds[9*i + 48]}')
            embedNew.add_field(name='\u200B', value='\u200B')
            embedNew.add_field(name = f'Secondary tree: {runestyleEmojiIds[2*i+11]}', value = f'{runeEmojiIds[9*i+49]} and {runeEmojiIds[9*i+50]}')
            embeds.append(embedNew)
        
        paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
        await paginator.run(embeds)
        
    @commands.command()
    async def i_live(self, ctx, *, args):
        summonerWatch = watcher.summoner.by_name('na1', args)
        summonerName = summonerWatch['name']
        SummonerID = summonerWatch['id']
        liveGame = watcher.spectator.by_summoner('na1', SummonerID)
        print(liveGame)
        print("LIVE GAME DETAILS")
        Participants = liveGame['participants']
        summnames = []
        runes = []
        runestyles = []
        summspells = []
        champids = []

        i = 0
        for temp in range(len(Participants)):
            if summonerName == Participants[temp]['summonerName']:
                i = temp
                break
        summnames.append(summonerName)
        for j in range(len(Participants[i]['perks']['perkIds'])):
            runes.append(Participants[i]['perks']['perkIds'][j])
        runestyles.append(Participants[i]['perks']['perkStyle'])
        runestyles.append(Participants[i]['perks']['perkSubStyle'])
        summspells.append(Participants[i]['spell1Id'])
        summspells.append(Participants[i]['spell2Id'])
        champids.append(Participants[i]['championId'])

        runeEmojiIds = []
        runestyleEmojiIds = []
        summspellEmojiIds = []
        champidEmojiIds= []
        
        with open('data/runesReforged.json', encoding='utf-8') as f:
            emojis = json.load(f)
        for i in range(len(runes)):
            for e in emojis:
                if int(e['KEY']) == runes[i]:
                    emoji_value = e['EMOJICODE']
                    runeEmojiIds.append(emoji_value)
        for i in range(len(runestyles)):
            for e in emojis:
                if int(e['KEY']) == runestyles[i]:
                    emoji_value = e['EMOJICODE']
                    runestyleEmojiIds.append(emoji_value)
        f.close()

        with open('data/summonerspells.json', encoding='utf-8') as f:
            emojis = json.load(f)
        for i in range(len(summspells)):
            for e in emojis:
                if int(e['KEY']) == summspells[i]:
                    emoji_value = e['EMOJICODE']
                    summspellEmojiIds.append(emoji_value)
        f.close()

        with open('data/championicons.json', encoding='utf-8') as f:
            emojis = json.load(f)
        for i in range(len(champids)):
            for e in emojis:
                if int(e['KEY']) == champids[i]:
                    emoji_value = e['EMOJICODE']
                    champidEmojiIds.append(emoji_value)
        f.close()

        DataDragonUrl = "https://ddragon.leagueoflegends.com/api/versions.json"
        PatchesData = urllib.request.urlopen(DataDragonUrl).read()
        Patches = json.loads(PatchesData)
        # print(Patches)
        CurrentPatch = Patches[1]
        # print(CurrentPatch)

        ChampionData = urllib.request.urlopen(f'http://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/data/en_US/champion.json').read()
        Champions = json.loads(ChampionData)
        # print(Champions)

        champNames = []
        res = None

        for x in range(len(champids)):
            for sub in Champions['data']:
                if int(Champions['data'][sub]['key']) == champids[x]:
                    res = sub
                    break 
            data = Champions['data'][res]['name']
            champNames.append(data)
            print(data)

        Currenttime = 0
        timeinseconds = liveGame['gameLength']
        m, s = divmod(timeinseconds, 60)
        y = ""
        if s < 10:
            y = 0

        # Discord Message Embed Style
        embeds = []
        embedNew = discord.Embed(title = f"{str(summonerName)}\'s live game", 
        colour = 16742893).add_field(name = f'Match Data:', value = f'Playing {champidEmojiIds[0]} {champNames[0]} for {m}:{y}{s}', inline = False)
        embedNew.add_field(name = f'Summoner Spells:', value = f'{summspellEmojiIds[0]} and {summspellEmojiIds[1]}', inline = False)
        embedNew.add_field(name = f'Main tree: {runestyleEmojiIds[0]}', value = f'{runeEmojiIds[0]} {runeEmojiIds[1]} {runeEmojiIds[2]} {runeEmojiIds[3]}')
        embedNew.add_field(name='\u200B', value='\u200B')
        embedNew.add_field(name = f'Secondary tree: {runestyleEmojiIds[1]}', value = f'{runeEmojiIds[4]} and {runeEmojiIds[5]}')
        embeds.append(embedNew)
        
        await ctx.send(embed=embedNew)
            

def setup(client):
    client.add_cog(In_Game_Builds(client))