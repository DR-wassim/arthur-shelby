from random import randint
import discord
from discord.ext import commands,tasks
from discord.ext.commands.core import check
from asyncio import TimeoutError as TE
import json

def check_user(id,id1) :
    return id == id1

class Reaction_role(commands.Cog):
    def __init__(self,client) :
        self.client = client
        self.name = "Reaction Role"
        self.emoji = ":loudspeaker:"
        self.call_name = "reaction_role"

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if payload.member :
            if not payload.member.bot :
                with open("./data_base/prefixes.json","r") as file :
                    guilds = json.load(file)
                if str(payload.guild_id) in guilds :
                    reactions = guilds[str(payload.guild_id)]["rection_msg_id"]
                    # print(reactions)
                    if str(payload.message_id) in reactions :
                        if payload.emoji.name in reactions[str(payload.message_id)]["emoji_roles"] :
                            guild = self.client.get_guild(payload.guild_id)
                            role = guild.get_role(int(reactions[str(payload.message_id)]["emoji_roles"][payload.emoji.name]))
                            member = payload.member
                            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        # print(payload)
        # guild = self.client.get_guild(payload.guild_id)
        # member = payload.member or guild.get_member(payload.user_id)
        if payload.member :
            if not payload.member.bot :
                with open("./data_base/prefixes.json","r") as file :
                    guilds = json.load(file)
                if str(payload.guild_id) in guilds :
                    reactions = guilds[str(payload.guild_id)]["rection_msg_id"]
                    if str(payload.message_id) in reactions :
                        if payload.emoji.name in reactions[str(payload.message_id)]["emoji_roles"] :
                            role = guild.get_role(int(reactions[str(payload.message_id)]["emoji_roles"][payload.emoji.name]))
                            await member.remove_roles(role)

    @commands.command(aliases = ["delete_auto_role" , "drp"],description = "[message id]",brief = "delete auto role")
    @commands.bot_has_permissions(manage_roles = True)
    @commands.has_permissions(manage_roles = True)
    async def delete_rp(self,ctx,role_id:int):
        with open("./data_base/prefixes.json","r") as file :
                guilds = json.load(file)

        if str(id) in guilds[str(ctx.message.guild.id)]["rection_msg_id"].keys() :
            guilds[str(ctx.message.guild.id)]["rection_msg_id"].pop(str(id))
        else :
            await ctx.send('there is no reaction role wit this ID')
            
        with open("./data_base/prefixes.json","w") as file :
            json.dump(guilds,file,indent=4)

    @commands.command(aliases = [ "crr", "rrole"],description = "follow the steps",brief = "activate auto role")
    @commands.bot_has_permissions(manage_roles = True)
    @commands.has_permissions(manage_roles = True)
    async def create_reaction_role(self,ctx):
        msg = None
        await ctx.send(f"follow my steps {ctx.message.author.mention} and we should complete this task easily mate")
        await ctx.send(f'{ctx.message.author.mention} mention a text channel where i post reaction roles')
        channel = None
        try :
            channel = await self.client.wait_for('message',timeout = 60.0,check =lambda msg :check_user(msg.author.id,ctx.message.author.id))

            channel = self.client.get_channel(int(channel.content.replace("<#","").replace(">","")))

        except TE:
            await ctx.send(f'how dare u {ctx.message.author.mention} ignore me u littel pice of shit i was talking to you')
            return
            
        await ctx.send(f'mention the roles and react with emoijies in one message in that form \n (:slight_frown: : sad / :cry: : cry / ... / etc ) and ')
        try :
            msg = await self.client.wait_for("message",timeout = 60.0 ,check = lambda msg : check_user(msg.author.id,ctx.message.author.id) )

        except  TE :
            await ctx.send(f'how dare u {ctx.message.author.mention} ignore me u littel pice of shit i was talking to you')
            return

        if msg :
            output = ""
            emojies = []
            roless = {}
            roles = msg.content.replace(" ","").split("/")
            guild_roles = [i.id for i in ctx.message.guild.roles]

            for role_data in roles:
                role_data = role_data.split(":")
                role = role_data[1]
                role_id = role.replace(" ","").replace("<@&","").replace(">","")

                emoji = role_data[0]
                roless[emoji] = role_id
                output += f"{emoji} : {role} \n"
                emojies.append(emoji)

            embed = discord.Embed(title = "Reaction Roles" ,colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
            embed.add_field(name = "React to get a role", value = output)

            to_send = await channel.send(embed = embed)
            for emoji in emojies :
                await to_send.add_reaction(emoji)

            with open("./data_base/prefixes.json","r") as file :
                guilds = json.load(file)
            
            if not guilds[str(ctx.message.guild.id)]["rection_msg_id"] :
                guilds[str(ctx.message.guild.id)]["rection_msg_id"] = {}
            guilds[str(ctx.message.guild.id)]["rection_msg_id"][str(to_send.id)] = {"channel_id" : channel.id,'emoji_roles':roless}
             
            with open("./data_base/prefixes.json","w") as file :
                json.dump(guilds,file,indent=4)


    @commands.command()
    async def clone(self,ctx,template:str=None,target:str=None):

        def check_reaction(reaction,user):
            if user == target_owner:
                if reaction.emoji == "✅":
                    return "mute"
                if reaction.emoji == "🚫":
                    return 'unmute'
            return False

        template = discord.utils.get(self.client.guilds, name = template)
        target = discord.utils.get(self.client.guilds, name = target)
        target_owner = target.get_member(target.owner_id)

        embed = discord.Embed(title = f"{target.name.upper()} RECONSTRUCTION PLAN" , colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
        embed.add_field(name = f"{ctx.message.author.mention} please bring {target_owner.name}#{str(target_owner)} ",value= f"we need the approve of {target_owner.name} the owner of {target.name} to complete this task")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction()
        await msg.add_reaction('🔊')
        try :
            result = await self.client.wait_for('reaction_add',timeout= 180.0, check=lambda reaction ,user: check_reaction(reaction,user))
        except :
            pass

        if result[0].emoji == "✅" :
            await ctx.send('ok than let\'s start')

        if result[0].emoji == "🚫" :
            return

        guilds = self.client.guilds
        if template and target :
            if template in guilds and target in guilds :

                
                me  = self.client.get_user(ctx.message.author.id)
                roles_to_delete = target.roles
                await me.send(' 1 - Deleting roles...')
                for role in roles_to_delete :
                    if not role.is_default():
                        try :
                            await role.delete()
                        except :
                            await me.send(f'there is a problem with {role.name} i will pass it')
                await me.send(' 1 - Complete ')

                roles = template.roles
                await me.send(' 2 - creating new roles...')
                for role in roles :
                    if not role.is_default():
                        try :
                            created_role = await target.create_role(name = role.name , permissions =role.permissions ,colour = role.colour ,hoist  =role.hoist ,mentionable =role.mentionable ,reason = "template Universe role" )
                        except :
                            await me.send(f'there is a problem with {role.name} i will pass it')
                await me.send(' 2 - Complete ')

                await me.send(' 3 - deleteing categories')
                channles_to_delete = target.categories
                for category in channles_to_delete :
                    await category.delete()
                await me.send(' 3 - Complete ')


                await me.send(' 4 - deleteing channels')
                channels_to_delete = target.channels
                for channel in channels_to_delete :
                    await channel.delete()
                await me.send(' 4 - Complete ')

                await me.send(' 5 - creating new channels')

                categories = template.by_category()
                for grp in categories :
                    category = None
                    if grp[0] :
                        category = await target.create_category(name = grp[0].name ,overwrites = grp[0].overwrites )
                        
                    if grp[1] :
                        for channel in grp[1] :
                            place = category or target
                            input = channel.overwrites
                            output = {}
                            
                            for r in input :
                                if isinstance(r , discord.Role):
                                    role = discord.utils.get(target.roles, name=r.name)
                                    output[role] = input[r]

                                if isinstance(r , discord.Member) and r in target.members:
                                    role = discord.utils.get(target.members, name=r.name)
                                    output[role] = input[r]

                            if isinstance(channel,discord.TextChannel):
                                await place.create_text_channel(name =channel.name ,overwrites =output ,position =channel.position ,topic = channel.topic ,slowmode_delay = channel.slowmode_delay ,nsfw =channel.nsfw ,reason = "bcz Arthur said it should be dummy" )
                            if isinstance(channel,discord.VoiceChannel):
                                await place.create_voice_channel(name =channel.name ,overwrites =output ,position =channel.position ,reason = "bcz Arthur said it should be dummy" ,bitrate =channel.bitrate ,user_limit =channel.user_limit )

                await me.send(' 5 - Complete ')
                await me.send(f'{target.name} server is ready to use ')
                
def setup(client):
    client.add_cog(Reaction_role(client))