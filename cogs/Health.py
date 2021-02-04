from discord.ext import commands
import discord
from random import randint
from utils.codes import alpha2 ,alpha3

import aiohttp
import asyncio

async def get_data():
    async with aiohttp.ClientSession() as session :
        async with session.get("https://api.covid19api.com/summary") as resp :
            data = await resp.json()
            return data

async def contry_index():
    data =await get_data()
    index = []
    for contry_info in data["Countries"]:
        index.append(contry_info['Country'])
    
    return index

contries = asyncio.get_event_loop().run_until_complete(contry_index())

def make_embeds(data,name,author):
    
    embed = discord.Embed(title = f'Coronavirus Cases | {name.capitalize()}',colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
    embed.set_author(name ="asked by  : " + str(author.name),icon_url=author.avatar_url)
    embed.add_field(name= ':face_vomiting:  Confirmed' , value = f"***{round(data['TotalConfirmed'],2)}***(+{round(data['NewConfirmed'],2)})", inline = True)
    embed.add_field(name= ':skull_crossbones:  Deaths' , value = f"***{round(data['TotalDeaths'],2)}***(+{round(data['NewDeaths'],2)})", inline = True)
    embed.add_field(name= ':ok_hand:  Recovered' , value = f"***{round(data['TotalRecovered'],2)}***(+{round(data['NewRecovered'],2)})", inline = True)
    embed.add_field(name= ':radioactive:  Active Cases' , value = f"***{round(data['TotalConfirmed'],2) - round(data['TotalRecovered'],2) - round(data['TotalDeaths'],2)}***", inline = True)
    embed.add_field(name= ':skull:  Mortality Rate' , value = f"{ round((data['TotalDeaths']*100)/data['TotalConfirmed'],2) }%", inline = True)
    embed.add_field(name= ':heartbeat:   Recovery Rate' , value = f"{ round((data['TotalRecovered']*100)/data['TotalConfirmed'],2) }%", inline = True)
    embed.set_footer(text="special thanks to api.covid19api.com for the data")
    
    return embed 


class Health(commands.Cog) :
    def __init__ (self,bot):
        self.bot = bot
        self.name = "Health"
        self.emoji = "️:medical_symbol:"
        self.call_name = "Health"

    @commands.command(aliases = ["covid","corona","c19" ])
    async def covid19 (self,ctx,*,contry :str = "all"):
        data = await get_data()
        if contry == 'all':
            embed = make_embeds(data['Global'],'Global',ctx.author)

        elif contry.lower().capitalize() in contries :

            embed = make_embeds(data["Countries"][contries.index(contry.lower().capitalize())],contry.lower().capitalize(),ctx.author) 

        elif contry.upper() in alpha2 :
            embed = make_embeds(data["Countries"][contries.index(alpha2[contry.upper()])],alpha2[contry.upper()],ctx.author)

        elif contry.upper() in alpha3 :
            embed = make_embeds(data["Countries"][contries.index(alpha3[contry.upper()])],alpha3[contry.upper()],ctx.author)

        
        else :
            embed = discord.Embed(title = "*** undefiend contry ***",colour = discord.Colour.red())
            embed.add_field(name = contry ,value= 'can\'t find a match')

        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Health(bot))