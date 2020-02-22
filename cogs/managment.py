import discord
import random
from discord.ext import commands
import time
import os


async def check_permission(ctx,perm_name,perm_value):
	permissions = ctx.channel.permissions_for(ctx.message.author)
	for permission in permissions :
		if permission[0] == perm_name :
			if permission[1] == perm_value:
				return True
			else:
				return False
# permissions =('create_instant_invite','kick_members','ban_members','administrator','manage_channels','manage_guild','add_reactions','view_audit_log','priority_speaker', 'stream', 'read_messages','send_messages','send_tts_messages','manage_messages','embed_links','attach_files','read_message_history','mention_everyone','external_emojis','view_guild_insights','connect','speak','mute_members','deafen_members', 'move_members', 'use_voice_activation','change_nickname','manage_nicknames','manage_roles','manage_webhooks','manage_emojis')


class managment(commands.Cog):
	"""FUCK OFF"""
	def __init__(self, client):
		self.client = client

	


	#EVENTS	

	@commands.Cog.listener()
	async def on_member_join(self ,member):
		print (f'{member} has joined a server .')

	@commands.Cog.listener()
	async def on_member_remove(self ,member):
		print(f'{member} has left a server')



		

	#COMMANDS


	@commands.command()
	async def roles1(self,ctx):
		await print(discord.Memeber.roles)


	@commands.command()
	async def add_channel(self,ctx,channel_name,salon_name=None):
		permission= await check_permission(ctx,"manage_channels",True)
		if permission == True:
			guild = ctx.message.guild.channel
			print (guild)
			await guild.create_text_channel(channel_name,category='CHAT')
			await ctx.send(f'introduce our new channel {channel_name}')
			await ctx.send('use it wisely')
		else :
			await ctx.send('u can\'t give me orders')

	@commands.command(pass_context = True)
	async def purge(self,ctx , amount=5):
		permission= await check_permission(ctx,"manage_messages",True)
		if permission == True:
			if amount == 0 :
				await ctx.send('fuck off')
			else:
				await ctx.channel.purge(limit=amount)
		else :
			await ctx.send("fuck off")
			time.sleep(10)
			await ctx.channel.purge(limit=1)

	@commands.command()
	async def kick(self,ctx, member : discord.Member ,* , reason=None):
		permission= await check_permission(ctx,"administrator",True)
		if permission == True:
			await member.kick(reason=reason)
		else :
			await ctx.send("I don't think so")

	@commands.command()
	async def ban(self,ctx, member : discord.Member ,* , reason=None):
		permission= await check_permission(ctx,"administrator",True)
		if permission == True:
			await member.ban(reason=reason)
			await ctx.send(f'Banned {member.mention}')
		else :
			await ctx.send("I don't think so")

	@commands.command()
	async def ping(self,ctx):
		await ctx.send(f' {round(self.client.latency * 1000)} fuckin\' ms')

	@commands.command()
	async def unban(self,ctx ,*,member ):
		permission= await check_permission(ctx,"administrator",True)
		if str(ctx.message.author) == "wassim#4406" or permission == True:
			banned_users = await ctx.guild.bans()
			member_name , member_discriminator = member.split("#")

			for ban_entry in banned_users:
				user =ban_entry.user

				if(user.name,user.discriminator) == (member_name,member_discriminator):
					await ctx.guild.unban(user)
					await ctx.send(f'Unbanned {user.mention}')
					return 

	@commands.command(pass_context=True)
	async def rename(self,ctx, member: discord.Member, new_name):
		permission= await check_permission(ctx,"manage_nicknames",True)
		if permission==True:
			await member.edit(nick=new_name)
			await ctx.send(f'Nickname was changed for {member.mention} ')
			pass
		if member == ctx.message.author:
			await member.edit(nick=new_name)
			await ctx.send('do it yourself next time u lazy pig ')
			pass
		if str(ctx.message.author) == 'wassim#4406':
			await member.edit(nick=new_name)
			await ctx.send('how can i say no to u')
			pass
		else:
			await ctx.send('U bloody piece of shit u dont have a manage Nicknames permission go kiss the owner ass to give u one')


	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def role(self,ctx,role=None,user=None):
		if check_permission('manage_roles',True):
			if role in ctx.message.channel.roles and user == None:
				await ctx.send('give it to who , u r mom ??')
			if role == None and user == None:
				await ctx.send('pls bitch put a role')
			if False:
				pass

		else:
			await ctx.send('repeat it and u r a dead man')
			await ctx.send('next time make sure u have role managment permission')



def setup(client):
	client.add_cog(managment(client))
