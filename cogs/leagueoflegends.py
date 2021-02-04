from discord.ext import commands
import discord 
from riotwatcher import LolWatcher, ApiError
import json
from requests.exceptions import HTTPError
from random import randint


from config import LOL_token


watcher = LolWatcher(LOL_token)

def get_rank_icon(tier , rank) :
    with open("./data_base/lol_data/rank_icons.json") as images :
        rank_icons = json.load(images)
    return rank_icons[tier][rank]
    

def get_user(user_discord_id):
    with open("./data_base/users_data.json" , "r") as users_data :
        lolaccounts = json.load(users_data)
    if "LOL" in lolaccounts[str(user_discord_id)] :
        if lolaccounts[str(user_discord_id)]["LOL"] != None : 
            return lolaccounts[str(user_discord_id)]["LOL"]
    return None

def get_map(map_id:int) :
    with open("./data_base/lol_data/maps.json" , "r") as maps_data :
        maps = json.load(maps_data)
    for Map in maps :
        if Map['mapId'] == map_id :
            return Map['mapName']
    return "invalid map id"

def get_queue(queue_id:int) :
    with open("./data_base/lol_data/queues.json" , "r") as queues_data :
        queues = json.load(queues_data)
    for queue in queues :
        if queue['queueId'] == queue_id :
            return queue['description']
    return "invalid queue id"

def check_user(match_detail,looking_4_id : str):
    players = match_detail['participantIdentities']  
    for player in players :
        if player["player"]["summonerId"] == looking_4_id :
            return player["participantId"]

def get_champ(champ_id) :
    with open("./data_base/lol_data/champion.json" , "r" , encoding="utf-8") as champion :
        champion_file = json.load(champion)
    champions = champion_file['data']
    for champ in champions :
        if champions[champ]['key'] == str(champ_id) :
            return champions[champ]['name']
    return "invalid champ id"


def stats(match_detail,user_game_id : int) :
    return match_detail['participants'][int(user_game_id-1)]

def Win_Ratio(wins,losses) :
    result =  (wins*100)/(wins + losses)
    return int(result)

def win(match_detail,user_game_id) :
    user_stats = stats(match_detail,user_game_id)
    if user_stats['stats']['win'] == True :
        return "victory"
    return 'defeated'

def get_first(match_detail,user_game_id : int) :
    user_stats = stats(match_detail,user_game_id)
    result = ''
    try :
        if user_stats['stats']['firstBloodAssist'] :
            result += "`"+'First Blood Assist'+"`  "
        if user_stats['stats']['firstBloodKill'] :
            result += "`"+'first Blood Kill'+"`"
        if user_stats['stats']['firstTowerAssist'] :
            result += "`"+'first Tower Assist'+"`  "
        if user_stats['stats']['firstTowerKill'] :
            result += "`"+'first Tower Kill'+"`  "


    except :
        pass
    return result
    

def get_items(item_id):
    with open("./data_base/lol_data/items.json" , "r") as items_file :
        items_data = json.load(items_file)
    items = items_data['data']
    for item in items :
        if item == str(item_id) :
            return items[item]['name']
    return "invalid item id"

def get_tags(tagList):
    result = ""
    for tag in tagList :
        result += "`"+str(tag)+"` "
    return result


class leagueoflegends(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.name = "League Of Legends"
        self.emoji = ":video_game:"
        self.call_name = "leagueoflegends"

    @commands.command(aliases = ["login"],description='[your game name] [region (optional) defualt : EUW]' ,brief = "connect to your lol account")
    async def lollogin(self,ctx,name : str , region : str = "EUW1"):
        user = None
        try :
            user = watcher.summoner.by_name(region, name)
        except HTTPError as e :
            status_code = e.response.status_code
            if status_code == 404 :
                await ctx.send(f"invalid name or region please use {ctx.prefix}help lollogin for more information")
            if status_code == 403 :
                await ctx.send('the riot game has forbidened us from access to their servers for unkown resaons')
            print("requests.exceptions.HTTPError" + str(status_code))
        if user != None :
            with open("./data_base/users_data.json" , "r") as users_data :
                lolaccounts = json.load(users_data)
            if 'LOL' not in lolaccounts[str(ctx.message.author.id)] or lolaccounts[str(ctx.message.author.id)]["LOL"] == None :
                lolaccounts[str(ctx.message.author.id)]["LOL"] = {"name" : user['name'] ,"id" : user['id'] , "region" : region}

                embed = discord.Embed(title = f"{lolaccounts[str(ctx.message.author.id)]['LOL']['name']} 's profile" , colour= discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
                embed.set_author(name ="profile owner  : " + str(ctx.message.author.name),icon_url=ctx.message.author.avatar_url)
                embed.add_field(name = 'status' , value= f"{ctx.message.author.name} loged in  {lolaccounts[str(ctx.message.author.id)]['LOL']['name']}")

                await ctx.send(embed = embed)


                with open("./data_base/users_data.json" , "w") as users_data :
                    json.dump(lolaccounts,users_data,indent = 4)
        else :
            await ctx.send("try again with a valid name")

    @commands.command(aliases = ["logout"],description = "[no parametres]",brief = "log out from your account")
    async def lollogout(self,ctx):
        with open("./data_base/users_data.json" , "r") as users_data :
            lolaccounts = json.load(users_data)
        if 'LOL' in lolaccounts[str(ctx.message.author.id)] :

            embed = discord.Embed(title = f"{lolaccounts[str(ctx.message.author.id)]['LOL']['name']} 's profile" , colour= discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
            embed.set_author(name ="profile owner  : " + str(ctx.message.author.name),icon_url=ctx.message.author.avatar_url)
            embed.add_field(name = 'status' , value= f"{ctx.message.author.name} loged out from {lolaccounts[str(ctx.message.author.id)]['LOL']['name']}")

            await ctx.send(embed = embed)

            del lolaccounts[str(ctx.message.author.id)]["LOL"]
            with open("./data_base/users_data.json" , "w") as users_data :
                json.dump(lolaccounts,users_data,indent = 4)

    @commands.command(aliases = ["tier"] , description = "no parametres" , brief = "show user rank in LOL")
    async def lolrank (self,ctx):
        User = get_user(ctx.message.author.id)
        if User != None :
            my_ranked_stats = watcher.league.by_summoner(User['region'],User['id'])
            for rank in my_ranked_stats: 
                embed = discord.Embed(title = f"{User['name']} 's profile" , colour= discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
                embed.set_author(name ="profile owner  : " + str(ctx.message.author.name),icon_url=ctx.message.author.avatar_url)
                embed.add_field(name="***" + str(rank["queueType"]).replace("_"," ") + "***" ,value=f"TIER : {rank['tier']} {rank['rank']} ",inline=False)
                embed.add_field(name = "statics" ,value = f"wins : {rank['wins']} | losses : {rank['losses']} | Win Ratio : {Win_Ratio(rank['wins'],rank['losses'])} %",inline=False)
                embed.set_thumbnail(url = get_rank_icon(rank['tier'],rank['rank']))
                await ctx.send(embed=embed)
        else :
            await ctx.send(f'please use the lollogin command to authorise the access to your data')

    @commands.command(aliases = ["matchlist","match" ] , description = "[number of matches] defualt = 1" , brief = "show last matches in LOL")
    async def last(self,ctx, matches_num : int = 1) :
        async with ctx.typing():
            user = get_user(ctx.message.author.id)
            if user != None :
                try :
                    lol_user = watcher.summoner.by_name(user['region'], user['name'])
                    matches = watcher.match.matchlist_by_account(user['region'], lol_user['accountId'])
                

                except HTTPError as e :
                    status_code = e.response.status_code
                    if status_code == 404 :
                        await ctx.send(f"invalid name or region please use {ctx.prefix}help lollogin for more information")
                    if status_code == 403 :
                        await ctx.send('the riot game has forbidened us from access to their servers for unkown resaons')
                    print("requests.exceptions.HTTPError" + str(status_code))
                    return


                matches = matches["matches"]
                for matche_index in range(matches_num) :
                    embed = discord.Embed(title = f" {user['name']}'s last matches" , colour= discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
                    embed.set_author(name ="profile owner  : " + str(ctx.message.author.name),icon_url=ctx.message.author.avatar_url)
                    matche = matches[matche_index]
                    match_detail = watcher.match.by_id(user["region"], matche['gameId'])
                    user_num = check_user(match_detail , user["id"])
                    user_stats = stats(match_detail,user_num)

                    embed.add_field(
                        name = f" --- matche ---       `{win(match_detail,user_num)}`" ,
                        value = f"{get_map(match_detail['mapId'])} | `{get_queue(match_detail['queueId'])}` | {match_detail['gameMode']} | {user_stats['timeline']['role']} {user_stats['timeline']['lane']}",inline = False)

                    embed.add_field(name = "Duration : " ,value = f" {str(int(match_detail['gameDuration']/60))} mins ",inline = True)
                    embed.add_field(name = "K/D/A : " ,value = f" {str(user_stats['stats']['kills'])}/{str(user_stats['stats']['deaths'])}/{str(user_stats['stats']['assists'])} ",inline = True)
                    embed.add_field(name = "champ : " ,value = f" {get_champ(user_stats['championId'])} lvl {str(user_stats['stats']['champLevel'])} ",inline = True)
                    embed.add_field(name = "Game Info :" ,value = f"total Minions Killed : {user_stats['stats']['totalMinionsKilled']} \n {get_first(match_detail,user_num)}",inline = True)

                    await ctx.send(embed = embed)

            else : 
                await ctx.send(f"{ctx.message.author.name} you don't have account registred \n please use the {ctx.prefix} lollogin command or help command")


    @commands.command()
    async def champ(self,ctx,champ_name : str) :
        with open("./data_base/lol_data/champion.json" , "r" , encoding="utf-8") as champion :
            champion_file = json.load(champion)
        champions = champion_file['data']
        if champ_name.capitalize() in champions :
            for champ in champions :
                if champ.lower() == champ_name.lower() :
                    embed = discord.Embed(title = f"LEAGUE OF LEGENDS CHAMPS {champions[champ]['version']}" , colour= discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
                    embed.add_field(name = f"{champions[champ]['name'].upper()} INFO CARD",value=f"***{champions[champ]['name']} {champions[champ]['title']}*** \n {champions[champ]['blurb']} \n attack  : {champions[champ]['info']['attack']} ***|*** defense  : {champions[champ]['info']['defense']} ***|*** magic  : {champions[champ]['info']['magic']} ***|*** difficulty  : {champions[champ]['info']['difficulty']} \n {get_tags(champions[champ]['tags'])}")
                    embed.set_image(url=f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champions[champ]['name']}_0.jpg")

                    await ctx.send(embed = embed)
        else :
            await ctx.send(f'ther is no champion named ***{champ_name}*** \n make sure you spell it right')



def setup(client):
    client.add_cog(leagueoflegends(client))