import discord
from random import randint
from discord import channel
from discord.ext import commands
import time
import os
import json
from colour import  Color
from typing import Union
import qrcode
from PIL import Image
from io import BytesIO


from config import developers , permissions_value
from core import image_to_byte_array


#https://discordapp.com/oauth2/authorize?client_id=674259662471823378&scope=bot&permissions=8


async def check_permission(ctx,perm_name,perm_value):
    permissions = ctx.channel.permissions_for(ctx.message.author)
    for permission in permissions :
        if permission[0] == perm_name :
            if permission[1] == perm_value:
                return True
            else:
                return False



async def update_static_channels(guild):
    categories = [category.name for category in guild.categories]
    if "server statics" in categories:
        members = guild.members
        bot = 0
        for member in members:
            if member.bot == True :
                bot += 1
        static_cat = [channel for channel in guild.channels if channel.name == "server statics"]
        to_edit = [channel for channel in guild.channels if channel.category_id == static_cat[0].id]
        for channel in to_edit:
            if "All Members :" in channel.name :
                await channel.edit(name = f"All Members : {len(members)}")
            elif "Users" in channel.name :
                await channel.edit(name = f"Users : {int(len(members)-bot)}")
            elif "Bots" in channel.name :
                await channel.edit(name = f"Bots : {bot}" )


class management(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.name = "management"
        self.emoji = "️:gear:"
        self.call_name = "management"


    @commands.Cog.listener()
    async def on_member_join(self,member):
        await update_static_channels(member.guild)

    @commands.Cog.listener()
    async def on_member_remove(self ,member):
        await update_static_channels(member.guild)

    @commands.Cog.listener()
    async def on_relationship_add(self,relationship):
        await relationship.accept()
        file = discord.File("./image/hello.jpg", filename = "hello.jpg")
        await relationship.user.send(file = file)

    @commands.command(aliases = ["cp","chp","CP","CHP"],description = "[new prefix]" ,brief ="obviously change prefix")
    @commands.has_permissions(view_audit_log=True)
    async def change_prefix(self,ctx,prefix):
    	with open('json/prefixes.json','r') as f:
    		prefixes = json.load(f)
    	if ctx.guild != None and prefix!=None:
	    	if prefix == 'default':
	    		prefixes[str(ctx.guild.id)] = ['fck ', 'Fck ','FCK ']
	    	else:
	    		prefixes[str(ctx.guild.id)] = prefix
	    	await ctx.send(f'the prefix has been changed to ***{prefixes[str(ctx.guild.id)]}***')
	    	with open('./json/prefixes.json','w') as f:
	    		json.dump(prefixes,f ,indent=4)	


    @commands.command(aliases = ["ad" , "addchannel"],description = '[channel name] [salon name if u want]', brief ="create new channel")
    @commands.has_permissions(manage_channels=True)
    async def add_channel(self,ctx,channel_name,salon_name=None):
        '''[channel name] [salon name if u want]'''

        guild = ctx.message.guild
        await discord.Guild.create_text_channel(guild,channel_name)
        await ctx.send(f'introduce our new channel {channel_name}')
        await ctx.send('use it wisely')



    @commands.command(pass_context = True,aliases=["clean","clear"],description = '[amount of message]',brief= "delete old messages")
    @commands.has_permissions(manage_messages = True)
    async def purge(self,ctx , amount=5):
        '''[amount of message]'''

        if amount == 0 :
            await ctx.send('fuck off',delete_after=10)
        else:
            try :
                await ctx.channel.purge(limit=amount+1)
            except AttributeError :
                await ctx.send("DM channels dosen't support purge command")


    @commands.command(description = "[member name] [reason if u want]" , brief = "kick memebers from the server but they can come back")
    @commands.has_permissions(kick_members = True)
    async def kick(self,ctx, member : discord.Member ,* , reason=None):
        '''[member name] [reason if u want]'''
        
        await member.kick(reason=reason)
        

    @commands.command(description = "[member name] [reason if u want]",brief = "ban members they can't return only if the unbanned")
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, member : discord.Member ,* , reason=None):
        '''[member name] [reason if u want]'''
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.name}')

    @commands.command(description = "  " , brief = "i am not going to explain this")
    async def ping(self,ctx):
        '''i am not going to explain this'''
        await ctx.send(f' {round(self.client.latency * 1000)} fuckin\' ms')

    @commands.command(description = "[member name] u can ban more than one at time" , brief ="give banned members permission to join the server again")
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx ,*,member ):
        '''[member name] u can ban more than one at time'''

        banned_users = await ctx.guild.bans()
        member_name , member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user =ban_entry.user

            if(user.name,user.discriminator) == (member_name,member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return 

    @commands.command(aliases = ["name"],description = "[mention member] [new name]" , brief = "give members new nick names")
    @commands.has_permissions(manage_nicknames = True)
    async def rename(self,	ctx, member: discord.Member, new_name):
        '''[mention member] [new name]'''

        await member.edit(nick=new_name)
        await ctx.send(f'Nickname was changed for {member.mention} ')

    @commands.command(aliases = ["QRinvite",'QRinv',"qrinv"],description = "[nothing]" , brief = "send an invite in a QR code ")
    # @commands.bot_has_permissions(create_invite = True)
    async def qrinvite(self,ctx):
        invite = await ctx.message.guild.channels[2].create_invite(temporary = False,unique =False)
        qr = qrcode.QRCode(version=1,box_size=10,border=5)
        qr.add_data(invite)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img_bytes =image_to_byte_array(img)
        file = discord.File(img_bytes,filename="QR_Code.jpg")

        await ctx.send(file=file)

    @commands.command(aliases = ["QR"],description = "[text to print in the QR code]" , brief = "send an invite in a QR code ")
    # @commands.bot_has_permissions(create_invite = True)
    async def qr(self,ctx, *,link ):
        invite = link
        qr = qrcode.QRCode(version=1,box_size=10,border=5)
        qr.add_data(invite)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img_bytes =image_to_byte_array(img)
        file = discord.File(img_bytes,filename="QR_Code.jpg")

        await ctx.send(file=file)
            

    @commands.command()
    async def card(self,ctx,user:discord.Member =None):
        member = user or ctx.message.author
        embed = discord.Embed(title = f"{member.name} profile" , colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
        embed.set_author(name = f"Asked by : {ctx.message.author.name}",icon_url=ctx.message.author.avatar_url)
        if member.nick :
            embed.add_field(name = "Server nickname : " , value = member.nick,inline=False)
        embed.add_field(name = "Created at :" , value = str(member.created_at)[:-10],inline=False)
        embed.add_field(name = "Joined at :", value = str(member.joined_at)[:-10],inline=False)
        embed.add_field(name = "Full name",value = f"{member.name}#{member.discriminator}")
        if member.premium_since :
            embed.add_field(name = "Premium since :" , value = member.premium_since,inline=False)
        if member.activities :
            embed.add_field(name = "Activities : " , value = member.activities[0].name,inline=False)
        if member.bot:
            embed.add_field(name = f"{member.name}" , value = "is a BOT!!",inline=False)



        embed.set_thumbnail(url =member.avatar_url)


        await ctx.send(embed = embed)

    @commands.command(aliases = ["nr","newrole"],description = "[role name]" ,brief = "add roles",usage= 'the role will have a random color and no permission and it should be listed with @evreyone to upgrade it use the upgrade command')
    @commands.has_permissions(manage_roles=True)
    async def new_role(self,ctx,role):
        '''[role name]'''
        
        if discord.utils.get(ctx.guild.roles, name=role) not in ctx.guild.roles :
            # role_perms = discord.Permissions(administrator = False)
            await ctx.guild.create_role(name=role,colour=discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)),permissions = discord.Permissions.general())
            await ctx.send(f'***{role}*** has been created')
        else:
            await ctx.send(f'{role} already exist')


    @commands.command()
    async def bring_members(self,ctx):
        invite = await ctx.message.guild.channels[2].create_invite()
        for guild in self.client.guilds :
            members_asked_to_join = []
            for member in guild.members :
                if member not in members_asked_to_join :
                    try :
                        await member.send(invite)
                        await member.send("sorry for bothering you but those guys are crazy")
                        members_asked_to_join.append(member)
                    except discord.errors.Forbidden :
                        await ctx.send(f"Cannot send messages to this user {member.name}")
                    except:
                        pass
        print("i send invites now we wait")

    @commands.command(aliases = ["gr","giverole"],description = "[role name] [member]" , brief = "give roles" ,usage= 'if the role dosen\'t exist it will create it and give it a random color and no permission and it should be listed with @evreyone to upgrade it use the upgrade command')
    @commands.has_permissions(manage_roles = True)
    async def give_role(self,ctx,role_name: Union[discord.Role , str] =None, member:discord.Member = None):

        ''' [role name] [member] '''

        if role_name != None :
            if member != None :
                if isinstance(role_name,str):
                    role = discord.utils.get(ctx.guild.roles, name=role_name)
                if role_name in ctx.guild.roles:
                    if member in role_name.members:
                        await ctx.send(f'{member} already has {role_name}')
                    else :
                        await member.add_roles(role_name)
                        await ctx.send('done!!!')
                elif role_name not in ctx.guild.roles:
                    role = await ctx.guild.create_role(name=role_name,colour=discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))                    
                    await member.add_roles(role)
                    await ctx.send('done!!!')
                else: 
                    await ctx.send("something wrong happened , sorry bro") 
            else :
                await ctx.send('yaaa mention somebody dude')
        else :
            await ctx.send("give him what dude , rewrite it again and make sure to mention a role")

    
    @commands.command(aliases = ["edit" ,"update"],description = "[role name u want to upgrade] [parametre] [value]" , brief = "edit roles",usage = "parametres and values : \n -- name : any thing discord will accept as role name \n -- permissions : check discord permissions or help perms \n -- colour : colour name ,hex colour or rgb code \n -- hoist : True ,true, yes anything else will be a no \n -- mentionable : same as hoist \n -- position : should be a number")
    @commands.has_permissions(manage_roles = True)
    async def upgrade(self,ctx,role : Union[discord.Role,str],parametre : str ,value):


        if isinstance (role,str) :
            await ctx.send(f'there is no role named {role} \nyou probably have to mention it')
            return 
        elif parametre == 'name' :
            await role.edit(name = value )
            await ctx.send(f"{role} is {value}")
            return
        elif parametre in ['permissions',"permission"] :
            if value in permissions_value :
                perms = permissions_value[value]

                await role.edit(permissions = perms)

                await ctx.send(f'{role} now have the permission {value}')
                
            else :
                await ctx.send(f'there is no permission named {value}')


        elif parametre in ['colour','color'] :
            try :
                color = Color(value)
            except ValueError :
                await ctx.send(f"{value} is not a recognized color")
                return


            await role.edit(colour = discord.Colour.from_rgb(int(color.rgb[0]*255),int(color.rgb[1]*255),int(color.rgb[2]*255)))
            await ctx.send(f"the role {role} has a new color : {color}")


        elif parametre == 'hoist' :
            if value in ["True",'true','yes'] :
                await role.edit(hoist = True)
                await ctx.send("done, now it should be shown separately in the member list ")
            else :
                await role.edit(hoist = False)
                await ctx.send("done, now it should be shown with other roles in the member list ")

        elif parametre =="mentionable":
            if value in ["True",'true','yes'] :
                await role.edit(mentionable  = True)
                await ctx.send("done, now evreyone can mention this role ")

            else :
                await role.edit(mentionable = False)
                await ctx.send("done, now no one can mention this role ")
        elif parametre =="position":
            try :
                pos = int(value)
                await role.edit(position  = pos)
                await ctx.send("done !!!")
            except ValueError :
                await ctx.send("value must be a number")
            
        else : 
            await ctx.send("unkown parametre")

    @commands.command(aliases = ["remove role" ,"rr" ,"removerole"],description = "[role_name]", brief ="delete usless roles")
    @commands.has_permissions(manage_roles = True)
    async def remove_role(self,ctx,role:discord.Role):
        '''remove_role [role_name]'''

        if role in ctx.guild.roles :
            await role.delete()
            await ctx.send('done !!')
        else :
            await ctx.send(f'{role} dosen\'t existe')

    @commands.command(aliases = ["serv-stats"],description = "[on/off]",brief = "show server statics as channels")
    @commands.has_permissions(manage_channels=True)
    async def statics(self,ctx,option = "on"):
        guild = ctx.message.guild
        categories = [category.name for category in guild.categories]

        if option == "on":
            if "server statics" not in categories:
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(connect=False)
                }
                category = await guild.create_category("server statics")
                await category.edit(position = 0)
                members = guild.members
                await guild.create_voice_channel(name = f"All Members : {len(members)}",category = category,overwrites=overwrites)
                bot = 0
                for member in members:
                    if member.bot == True :
                        bot += 1
                await guild.create_voice_channel(name = f"Users : {int(len(members)-bot)}",category = category,overwrites=overwrites)
                await guild.create_voice_channel(name = f"Bots : {bot}",category = category,overwrites=overwrites)
            else:
                await ctx.send('already activated')
        elif option != 'on':
            if "server statics" in categories:
                static_cat = [channel for channel in guild.channels if channel.name == "server statics"]
                to_delete = [channel for channel in guild.channels if channel.category_id == static_cat[0].id]
                for to_delete_channel in to_delete :
                    await to_delete_channel.delete()
                await static_cat[0].delete()

    @commands.command(aliases = ["keep"],description = "[any text]",brief = "save data")
    async def hold(self,ctx,*,item):
        with open("data_base/users_data.json","r") as data_base_file:
            data_base = json.load(data_base_file)
        
        if str(ctx.message.author.id) not in data_base:
            data_base[str(ctx.message.author.id)] = {"name" : str(ctx.message.author.name)}
        
        if str(ctx.message.author.id) in data_base:
            if "hold" not in data_base[str(ctx.message.author.id)] :
                data_base[str(ctx.message.author.id)]["hold"] = []

            if "hold" in data_base[str(ctx.message.author.id)] :
                data_base[str(ctx.message.author.id)]["hold"].append(item)
        
        with open("data_base/users_data.json","w") as data_base_file:
            json.dump(data_base,data_base_file,indent = 4)

    @commands.command(aliases = ["sh","showholdfolder","saves"],description = "[nothing]",brief = "show saved data")
    async def holdFolder(self,ctx):
        with open("data_base/users_data.json","r") as data_base_file:
            data_base = json.load(data_base_file)

        if str(ctx.message.author.id) not in data_base:
            await ctx.send("unauthorized access")

        elif str(ctx.message.author.id) in data_base:
            if "hold" not in data_base[str(ctx.message.author.id)] :
                await ctx.send(f'your folder is empty {ctx.message.author.mention}')
            if "hold"  in data_base[str(ctx.message.author.id)] :   
                embed = discord.Embed(title = f"{ctx.message.author.name.upper()}'s hold Folder" , colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
                for index,item in enumerate(data_base[str(ctx.message.author.id)]["hold"]):
                    embed.add_field(name = f"`{index}`" , value = item)
                await ctx.send(embed = embed)


@commands.command()
async def update_guilds(self,ctx):
    with open('./data_base/prefixes.json',"r") as guilds :
        guilds = json.load(guilds)

    guilds_list = self.client.guilds
     

def setup(client):
    client.add_cog(management(client))
