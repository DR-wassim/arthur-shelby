import discord
from discord.ext import commands

class class_name(commands.Cog):

	def __init__(self, client):
		self.client = client 







def setup(client):
	client.add_cog(class_name(client))