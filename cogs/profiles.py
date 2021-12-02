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


class Profiles(commands.Cog):
    def __init__(self, client):
        self.client = client   

    @commands.command(name="prettyprofile", aliases=["p","profile","pretty"])
    async def profile(self, ctx, regioncode=None, *, summoner=None):
        """Shows summoner profile in a pretty way"""

        print(regioncode)
        if regioncode == "None":
            Region = "na1"
        else:
            Region = regioncode
        
        print(summoner)
        
        summonerWatch = watcher.summoner.by_name(Region, str(summoner))
        summonerName = summonerWatch['name']
        SummonerID = summonerWatch['id']
        summonerLevel = summonerWatch['summonerLevel']
        Icon = summonerWatch['profileIconId']
        # print(summonerWatch)
        stats = watcher.league.by_summoner(Region, SummonerID)
        # print(stats)
        # Get the Solo Queue Values (find the Solo Queue Dictionary within stats)
        res = None
        SOLODUO = True
        for sub in stats:
            if sub['queueType'] == "RANKED_SOLO_5x5":
                res = sub
                break
        if res == None:
            SOLODUO = False
        else: 
            n = stats.index(res)
            soloduotier = stats[n]['tier']
            soloduorank = stats[n]['rank']
            soloduowins = int (stats[n]['wins'])
            soloduolosses = int (stats[n]['losses'])
            soloduolp = stats[n]['leaguePoints']
            soloduowinrate = int (soloduowins/(soloduowins + soloduolosses) *100)

        res = None
        RANKEDFLEX = True
        for sub in stats:
            if sub['queueType'] == "RANKED_FLEX_SR":
                res = sub
                break
        if res == None:
            RANKEDFLEX = False
        else:
            n = stats.index(res)
            rankedflextier = stats[n]['tier']
            rankedflexrank = stats[n]['rank']
            rankedflexwins = int (stats[n]['wins'])
            rankedflexlosses = int (stats[n]['losses'])
            rankedflexlp = stats[n]['leaguePoints']
            rankedflexwinrate = int (rankedflexwins/(rankedflexwins + rankedflexlosses) *100)
        
        DataDragonUrl = "https://ddragon.leagueoflegends.com/api/versions.json"
        masteriesGrabbing = 3
        mastery = watcher.champion_mastery.by_summoner(Region, SummonerID)
        print("MASTERY")
        # print(mastery)
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
        # print(Patches)
        CurrentPatch = Patches[0]
        # print(CurrentPatch)
        
        ChampionData = urllib.request.urlopen(f'http://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/data/en_US/champion.json').read()
        Champions = json.loads(ChampionData)
        # print(Champions)

        champNames = []
        res = None

        for x in range(len(champId)):
            for sub in Champions['data']:
                if int(Champions['data'][sub]['key']) == champId[x]:
                    res = sub
                    break 
            data = Champions['data'][res]['name']
            champNames.append(data)
            print(data)
            
        champEmojiId = []
        
        with open('data/championicons.json', encoding='utf-8') as f:
            emojis = json.load(f)
        for i in range(len(champId)):
            for e in emojis:
                if int(e['KEY']) == champId[i]:
                    emoji_value = e['EMOJICODE']
                    champEmojiId.append(emoji_value)
        f.close()

        inLiveGame = True
        try:
            liveGame = watcher.spectator.by_summoner(Region, SummonerID)
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

            ChampionData = urllib.request.urlopen(f'http://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/data/en_US/champion.json').read()
            Champions = json.loads(ChampionData)
            # print(Champions)

            livechampNames = []
            res = None

            for x in range(len(champids)):
                for sub in Champions['data']:
                    if int(Champions['data'][sub]['key']) == champids[x]:
                        res = sub
                        break 
                data = Champions['data'][res]['name']
                livechampNames.append(data)
                print(data)

            Currenttime = 0
            timeinseconds = liveGame['gameLength']
            m, s = divmod(timeinseconds, 60)
            y = ""
            if s < 10:
                y = 0
        except:
            inLiveGame = False
            print("Not in Live Game")

        
        
        temp_embed = discord.Embed(description=f"Fetching your profile, wait a moment...", color=0xfda5b0)
        temp_embed.set_thumbnail(url=f'https://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/img/profileicon/{Icon}.png')
        msg = await ctx.send(embed=temp_embed)

        embed = discord.Embed(title=f'Profile: {summonerName}', description=f"Summary of the profile you asked for: \n \u200B", color=16742893)
        embed.set_thumbnail(url=f'https://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/img/profileicon/{Icon}.png')
        embed.add_field(name='Summoner Level', value=f'{summonerLevel}')
        embed.add_field(name='\u200B', value='\u200B')
        embed.add_field(name='\u200B', value='\u200B')
        if SOLODUO == True:
            embed.add_field(name='Ranked (Solo/Duo)', value = f'{str(soloduotier)} {str(soloduorank)} with {str(soloduolp)} LP and a {str(soloduowinrate)}% winrate')
        else:
            embed.add_field(name='Ranked (Solo/Duo)', value = 'N/A')
        embed.add_field(name='\u200B', value='\u200B')
        if RANKEDFLEX == True:
            embed.add_field(name='Ranked (Flex)', value = f'{str(rankedflextier)} {str(rankedflexrank)} with {str(rankedflexlp)} LP and a {str(rankedflexwinrate)}% winrate')
        else:
            embed.add_field(name='Ranked (Flex)', value = 'N/A')
        embed.add_field(name='Highest Champion Masteries', value=f'''
                        **[1]**  {champEmojiId[0]} {champNames[0]}: {champPoints[0]} pts
                        **[2]**  {champEmojiId[1]} {champNames[1]}: {champPoints[1]} pts
                        **[3]**  {champEmojiId[2]} {champNames[2]}: {champPoints[2]} pts
                        \u200B''')
        embed.add_field(name='\u200B', value='\u200B')
        if inLiveGame == True:
            embed.add_field(name='Live Game', value=f'''
            Playing {champidEmojiIds[0]} {livechampNames[0]} for {m}:{y}{s}
            Summoner Spells: {summspellEmojiIds[0]} and {summspellEmojiIds[1]}
            Main tree:{runestyleEmojiIds[0]} - {runeEmojiIds[0]} {runeEmojiIds[1]} {runeEmojiIds[2]} {runeEmojiIds[3]}
            Secondary tree: {runestyleEmojiIds[1]} - {runeEmojiIds[4]} {runeEmojiIds[5]}
            \u200B''')
        else:
            embed.add_field(name='Live Game', value=f'N/A')
        await asyncio.sleep(1)
        await msg.edit(embed=embed) 

    @commands.command()
    async def mp(self, ctx, intarg, *, args):
        # STATS
        Region = 'na1'
        DataDragonUrl = "https://ddragon.leagueoflegends.com/api/versions.json"
        # print(intarg)
        masteriesGrabbing = int(intarg)
        summoner = watcher.summoner.by_name(Region, args)
        Icon = summoner['profileIconId']
        print(summoner)
        summonerName = summoner['name']
        SummonerID = summoner['id']
        stats = watcher.league.by_summoner(Region, SummonerID)
        # print(stats)
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
        CurrentPatch = Patches[1]
        print(CurrentPatch)
        
        ChampionData = urllib.request.urlopen(f'http://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/data/en_US/champion.json').read()
        Champions = json.loads(ChampionData)
        # print(Champions)

        champNames = []
        res = None



        for x in range(len(champId)):
            for sub in Champions['data']:
                if int(Champions['data'][sub]['key']) == champId[x]:
                    res = sub
                    break 
            data = Champions['data'][res]['name']
            champNames.append(data)
            print(data)
            
        champEmojiId = []
        
        with open('data/championicons.json', encoding='utf-8') as f:
            emojis = json.load(f)
        for i in range(len(champId)):
            for e in emojis:
                if int(e['KEY']) == champId[i]:
                    emoji_value = e['EMOJICODE']
                    champEmojiId.append(emoji_value)
        f.close()

        """ print("NAMES")
        for sub in Champions['data']:
            text = Champions['data'][sub]['id']
            print(f'{text},', end ="")
            text = Champions['data'][sub]['id']
            print(f'\:{text}:,', end="")
            text = Champions['data'][sub]['key']
            print(f'{text}') """

        temp_embed = discord.Embed(description=f"Fetching your masteries, wait a moment...", color=0xfda5b0)
        temp_embed.set_thumbnail(url=f'https://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/img/profileicon/{Icon}.png')
        msg = await ctx.send(embed=temp_embed)

        embed = discord.Embed(title=f'Profile: {summonerName}', description=f"Masteries of the profile you asked for: \n \u200B", color=16742893)
        embed.set_thumbnail(url=f'https://ddragon.leagueoflegends.com/cdn/{CurrentPatch}/img/profileicon/{Icon}.png')
        for i in range(len(champPoints)):
            embed.add_field(name = f'**[{i+1}]** {champEmojiId[i]} {champNames[i]}: {champPoints[i]} mastery points', value = '\u200b', inline = False)
        embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)

        await asyncio.sleep(1)
        await msg.edit(embed=embed) 

def setup(client):
    client.add_cog(Profiles(client))