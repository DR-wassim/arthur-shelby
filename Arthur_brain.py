from discord.ext import commands , tasks
import discord
from random import randint
import json
from itertools import cycle


from config import developers , perms ,defualt_prefix ,Status , discord_access_token
from core import listToString , cogsList ,collect_personal_data,collect_data


def get_prefix(bot, message):
    with open('./data_base/prefixes.json','r') as f :
        prefixes = json.load(f)
    if not message.guild or str(message.guild.id) not in prefixes :
        return defualt_prefix
    return commands.when_mentioned_or(*prefixes[str(message.guild.id)]["prefix"])(bot, message)
intents = discord.Intents.all()
#################################################################### ahaya
client = commands.Bot(command_prefix=get_prefix,intents = intents)
#################################################################### al fo9
status = cycle(Status)
client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)
    print('u son of bitch ,I am in ,As {0.user}'.format(client))
    change_status.start()

@tasks.loop(seconds = 10)
async def change_status():
    await client.change_presence(status=discord.Status.idle,activity =discord.Game(next(status)))
    

@client.command()
async def help(ctx , option :str = None) :
    prefix = ctx.prefix
    if option == None :
        embed = discord.Embed(title = "*** HELP MENU ***",colour =discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
        embed.set_author(name ="asked by  : " + str(ctx.message.author.name),icon_url=ctx.message.author.avatar_url)
        passed_cog = ["CommandErrorHandler" ]

        for cog_name in cogsList() :
            if cog_name in passed_cog :
                continue
            if cog_name in ["developers","FBPage"] and int(ctx.message.author.id) not in developers : 
                continue
            cog = client.get_cog(cog_name)
            if cog :
                if not cog.emoji :
                    cog.emoji == ":exploding_head:"
                embed.add_field(name = f'{cog.emoji}  {cog.name}' ,value = f"`{prefix}help {cog.call_name}`")
            else : 
                print(f"error {cog_name}")
        embed.add_field(name = "Check our Facebook MEMES Page" , value= "[here](https://www.facebook.com/ArthurTheMemesBot/)",inline=False)
        await ctx.send(embed = embed)

        return

    if option in ['perms',"permission",'permissions' , "perm"] :
        embed = discord.Embed(title = "discord permissions" ,colour =discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
        embed.add_field(name = "permissions" ,value = listToString(perms,"-"))
        embed.add_field(name = "Check our Facebook MEMES Page" , value= "[here](https://www.facebook.com/ArthurTheMemesBot/)",inline=False)
        embed.set_footer(text = "you probably should copy paste them")
        await ctx.send(embed = embed)

    if option in cogsList() or option.capitalize() in cogsList() or option.lower() in cogsList() or option.upper() in cogsList() :
        # if option == "developers" and int(ctx.message.author.id) in developers :
        #     pass
        if option == "developers" and int(ctx.message.author.id) not in developers :
            await ctx.send('yaa keep dreaming')
            return
        cog = client.get_cog(option) or client.get_cog(option.capitalize()) 
        if cog != None :
            cog_commands = cog.get_commands()
            embed = discord.Embed(title = f"*** HELP {cog.emoji} {str(cog.name).upper()} MENU ***".center(40))
            embed.set_author(name ="asked by  : " + str(ctx.message.author.name),icon_url=ctx.message.author.avatar_url)
            all_commands = ""
            for command in cog_commands :
                all_commands += "- `"+str(command)+"` -" 
            embed.add_field(name = f"commands : with {ctx.prefix} before every one " , value = all_commands ,inline=False )
            embed.add_field(name = "Check our Facebook MEMES Page" , value= "[here](https://www.facebook.com/ArthurTheMemesBot/)",inline=False)
            embed.set_footer(text=f'for more information about the command use {ctx.prefix} help <command name>')
            await ctx.send(embed = embed)
        else : 
            await ctx.send(f"`no command called '{option}' found`")

        return
        
    commandsdict = {}
    aliases = {}
    for cog_name in cogsList():
        cog = client.get_cog(cog_name)
        if cog != None :
            commands = cog.get_commands()
            for command in commands :
                commandsdict[command.name] = {'name' : command.name ,'description' : command.description , "brief" : command.brief , 'aliases' : command.aliases , "usage" : command.usage} # ,"positionInMemory" : command 
                for aliase in command.aliases :
                    aliases[aliase] = command.name

        
    if option in commandsdict.keys() or option in aliases.keys() or option.capitalize() in commandsdict.keys() or option.capitalize() in aliases.keys():
        if option in aliases.keys() :
            option = aliases[option]
        embed = discord.Embed(title = f"{ctx.prefix}{option} Info" ,colour =discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))

        if commandsdict[option]['description'] :
            embed.add_field(name = "parametres  : " , value=commandsdict[option]['description'] , inline= False)
        else : 
            embed.add_field(name = "parametres  : " , value="no parametres" , inline= False)
        
        if  commandsdict[option]['brief'] :
            embed.add_field(name = "brief  : " , value=commandsdict[option]['brief'],inline=True)
        else : 
            embed.add_field(name = "brief  : " , value="no brief" , inline= False)

        if  commandsdict[option]['aliases'] :
            embed.add_field(name = "aliases  : " , value=listToString(commandsdict[option]['aliases'],"-") ,inline=True)
        else : 
            embed.add_field(name = "aliases  : " , value="no aliases" , inline= False)
        
        if  commandsdict[option]['usage'] :
            embed.add_field(name = "details  : " , value=commandsdict[option]['usage'] ,inline=False)
        else : 
            embed.add_field(name = "details  : " , value="no details" , inline= False)

        await ctx.send(embed=embed)

        return
    
    if option not in cogsList() and option != None and option not in commandsdict.keys() and option not in ['perms',"permission",'permissions' , "perm"]: 
        await ctx.send(f"there is no command called {option}")

@client.event
async def on_guild_join(guild):
    with open('./data_base/prefixes.json','r') as f:
        guilds_we_have = json.load(f)

    guilds_we_have[str(guild.id)] = {"prefix" : defualt_prefix,"rection_msg_id" : 0}

    with open('./data_base/prefixes.json','w') as f:
        json.dump(guilds_we_have,f ,indent=4)

    collect_data(guild)

@client.event
async def on_guild_remove(guild):
    with open('./data_base/prefixes.json','r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('./data_base/prefixes.json','w') as f:
        json.dump(prefixes,f ,indent=4)

@client.event
async def on_member_join(member):
    collect_personal_data(member)

for cog in cogsList():
    try :
        client.load_extension(f'cogs.{cog}')
    except :
        pass
client.run(discord_access_token)