import discord
from discord.ext import commands
import aiohttp
from PIL import Image
from io import BytesIO

from core import image_to_byte_array


async def _fetch_profile_pic(url:str):
    async with aiohttp.ClientSession() as session :
        async with session.get(str(url)) as resp:
            if resp.status == 200 :
                data = await resp.read()
                img = Image.open(BytesIO(data))
                return img


class fun(commands.Cog):    
    def __init__(self,client):
        self.client = client
        self.name = "fun"
        self.emoji = ":confetti_ball:"
        self.call_name = "fun"

    @commands.command(description = "[mention someone]",brief = "i can milk you meme",aliases = ["i_can_milk_you"])
    async def milk(self,ctx,target:discord.Member = None):
        member = target or ctx.message.author

        if member == ctx.message.author:
            milker = self.client.user
        elif member == target :
            milker = ctx.message.author

        bg_img = Image.open("image/i_can_milk_you.jpg","r")

        profile_pic = await _fetch_profile_pic(member.avatar_url)
        profile_pic = profile_pic.resize((128,128))

        milker_pic = await _fetch_profile_pic(milker.avatar_url)
        milker_pic = milker_pic.resize((200,200))

        bg_img.paste(profile_pic,(600,220))
        bg_img.paste(milker_pic,(100,150))

        img_bytes = image_to_byte_array(bg_img)

        file = discord.File(img_bytes,filename="milk.jpg")
        await ctx.send(file = file)

    @commands.command(name = '3dragons',description = "[mention 2 or 3 friends]",brief = "3 dragons meme",aliases = ["3dragons_meme"])
    async def _3dragons(self,ctx,target:discord.Member = None,target1:discord.Member = None,silly:discord.Member = None):
        if target1 == None :
            await ctx.send('please mention enough members')
            return
        if silly == None :
            silly = target1
            target1 = target
            target = ctx.message.author

        bg_img = Image.open("image/3dragons.jpg","r")
        
        
        silly_pic = await _fetch_profile_pic(silly.avatar_url)
        target1_pic = await _fetch_profile_pic(target1.avatar_url)
        target_pic = await _fetch_profile_pic(target.avatar_url)

        silly_pic = silly_pic.resize((200,200))
        target1_pic = target1_pic.resize((200,200))
        target_pic = target_pic.resize((200,200))

        bg_img.paste(silly_pic,(550,300))
        bg_img.paste(target1_pic,(300,300))
        bg_img.paste(target_pic,(20,300))

        img_bytes = image_to_byte_array(bg_img)

        file = discord.File(img_bytes,filename="3dragons.jpg")
        await ctx.send(file = file)
        
def setup(client):
    client.add_cog(fun(client))


