import discord
import random
from discord.ext import commands
import time
import os



client = commands.Bot(command_prefix =lambda x,y: y if y.content.startswith=='fck' else 'fck')


@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.idle, activity = discord.CustomActivity('PEAKY BLINDERS'))
	print('u son of bitch ,I am in ,As {0.user}'.format(client))


@client.event
async def on_message(message):
	channel = message.channel
	await channel.send('hi')

@client.event
async def on_member_join(member):
	print("Recognised that a member called " + member.name + " joined")


@client.event
async def load(ctx ,extension):
	client.load_extension(f'cogs.{extension}')

@client.event
async def unload(ctx ,extension):
	client.unload_extension(f'cogs.{extension}')

@client.event
async def reload(ctx ,extension):
	client.unload_extension(f'cogs.{extension}')
	client.load_extension(f'cogs.{extension}')	


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')



client.run('Njc0MjU5NjYyNDcxODIzMzc4.XkCQ4A.xA6CxHSdgEy7l3ObkAlsRmg1u1I')
	