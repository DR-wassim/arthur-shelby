from logging import error
import discord
from discord.ext.commands.core import is_owner
import facebook
import praw
import json
from discord.ext import commands ,tasks
import aiohttp
import aiofiles
from random import randint,choice

from config import client_id , client_secret ,user_agent , fb_access_token ,owner_id ,facebookPageAdmins 
from core import update_memes , delete_meme , block_meme

reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,user_agent=user_agent)

graph = facebook.GraphAPI(access_token=fb_access_token )


async def fetch_image(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp :
            if resp.status == 200 :
                f = await aiofiles.open(f"./image/meme.{link[-3:]}","wb")
                await f.write(await resp.read())
                await f.close()
                return open(f"./image/meme.{link[-3:]}","rb")
            else :
                return None


def getApprovedMemes() -> dict:
    with open("./data_base/approved_memes.json","r") as file :
        memes = json.load(file)
    return memes["memes"]

def removeFromApprovedMemes(meme : dict) :
    with open("./data_base/approved_memes.json","r") as file :
        memes = json.load(file)
    memes["memes"].remove(meme)
    with open("./data_base/approved_memes.json","w") as file :
        json.dump(memes,file,indent=4)

class FBPage(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.name = "Facebook Page Manager"
        self.emoji = ":regional_indicator_f:"
        self.call_name = "FBPage"

    @commands.Cog.listener()
    async def on_ready(self):
        self.regularPost.start()
        


    @commands.command(aliases = ["sap","approveds"] ,brief ="manage approved memes")
    async def surf_approved_memes(self,ctx):
        data = getApprovedMemes()

        if not data :
            await ctx.send("there is no approved memes :'(")
            return
        close = False

        def check_reaction(reaction,user):
            if user.id in facebookPageAdmins:
                if reaction.emoji == "❤️" or reaction.emoji == "👎" or reaction.emoji == "⬅️" or reaction.emoji == "➡️" or reaction.emoji == "❌" :
                    return True
            return False

        index = 0

        msg = None

        while not close :
            meme = data[index]
            embed = discord.Embed(title = f"from {meme['subreddit']}" ,colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
            embed.add_field(name = "Check our Facebook MEMES Page" , value= "[here](https://www.facebook.com/ArthurMemes-100739768442266)",inline=False)
            embed.add_field(name = f'{meme["score"]} :thumbsup: | {meme["num_comments"]} :speech_balloon: ',value = meme["title"],inline=False)
            embed.set_image(url = meme['url'])

            if not msg :
                msg = await ctx.send(embed = embed)
            else : 
                await msg.edit(embed = embed)

            await msg.add_reaction("⬅️")
            await msg.add_reaction("➡️")
            await msg.add_reaction("❤️")
            await msg.add_reaction("👎")
            await msg.add_reaction("❌")


            try :
                approve = await self.client.wait_for('reaction_add',timeout = 60.0, check=lambda reaction , user :check_reaction(reaction,user))
            except : 
                await ctx.send("BYE")
                await msg.clear_reactions()
                break
            if approve[0].emoji == "⬅️" :
                index -= 1 
            if approve[0].emoji == "➡️" :
                index += 1 

            index %= len(data)

            if approve[0].emoji == "❤️" :
                me = self.client.get_user(owner_id)
                if meme["url"][-3:] != "gif" :
                    post_info = graph.put_photo(image=await fetch_image(meme["url"]),message = meme["title"])
                else : 
                    post_info = graph.put_object(parent_object='me', connection_name='feed',message=meme["title"],link = meme["url"])

                embed = discord.Embed(title = f"from {meme['subreddit']}" ,colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
                embed.add_field(name = "Check our Facebook MEMES Page" , value= "[here](https://www.facebook.com/ArthurMemes-100739768442266)",inline=False)
                embed.add_field(name = f'{meme["score"]} :thumbsup: | {meme["num_comments"]} :speech_balloon: ',value = meme["title"],inline=False)
                embed.set_footer(text = f"post id : {post_info['post_id'].split('_')[-1]}")

                embed.set_image(url = meme['url'])
                await me.send(embed= embed)
                removeFromApprovedMemes(meme)
                block_meme(meme=meme)
                data.remove(meme)

            if approve[0].emoji == "👎" :
                removeFromApprovedMemes(meme)
                data.remove(meme)
                
            if approve[0].emoji == "❌" :
                close = True

            await msg.clear_reactions()


    @commands.command()
    @commands.is_owner()
    async def block_repetable_post(self,ctx,*,meme_title) :
        if meme_title:
            block_meme("by_me",meme=meme_title)
            await ctx.send("blocked")


    @commands.command(aliases = ["pm"],description = "[image Link] [post description] both r optional" ,brief ="post memes in the facebook page only the owner is able to use this command so don't try and waste my time")
    @commands.is_owner()
    async def post_meme(self, ctx,link= None ,message= None ) -> None:

        if link : 

            meme = {'title' : message or " " ,  "url": link}

        else :
            data = update_memes(reddit)
            highest = 0 
            highest_index = 0
            for index ,meme in enumerate(data) :
                if meme["score"] > highest and meme["url"][-3:] != "gif" :
                    highest_index = index
                    highest = meme["score"]
            meme = data[highest_index]

        try :
            if meme["url"][-3:] != "gif" :
                post_info = graph.put_photo(image=await fetch_image(meme["url"]),message = meme["title"])
            else : 
                post_info = graph.put_object(parent_object='me', connection_name='feed',message=meme["title"],link = meme["url"])

            embed = discord.Embed(title = f"from {meme['subreddit']}" ,colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
            embed.add_field(name = "Check our Facebook MEMES Page" , value= "[here](https://www.facebook.com/ArthurMemes-100739768442266)",inline=False)
            embed.add_field(name = f'{meme["score"]} :thumbsup: | {meme["num_comments"]} :speech_balloon: ',value = meme["title"],inline=False)
            embed.set_footer(text = f"post id : {post_info['post_id'].split('_')[-1]}")
            embed.set_image(url = meme['url'])
    
            if not link :
                delete_meme(meme)
                block_meme(meme = meme)

            await ctx.send(embed= embed)

        except Exception as e :
            print(e) 
            await ctx.send("oops error ! XDD ")


    @commands.command(aliases = ["delpost","delp"],description = "[post id]" ,brief ="delete memes from the facebook page only the owner is able to use this command so don't try and waste my time")
    @commands.is_owner()
    async def delete_post(self,ctx,post_id) :
        if len(post_id) == 15 :
            graph.delete_object(post_id)
            await ctx.send("deleted !")
        else :
            await ctx.send("Wrong ID")


    @tasks.loop(hours=1.5)
    async def regularPost(self):
        me = None
        try :
            me  = self.client.get_user(owner_id)
            await me.send("hi i am posting on facebook")
            approvedMemes = getApprovedMemes()
            data = []

            if approvedMemes :
                meme = choice(approvedMemes)
            else:
                data = update_memes(reddit)
                highest = 0 
                highest_index = 0
                for index ,meme in enumerate(data) :
                    if meme["score"] > highest and meme["url"][-3:] != "gif" :
                        highest_index = index
                        highest = meme["score"]

                meme = data[highest_index]

            if meme["url"][-3:] != "gif" :
                post_info = graph.put_photo(image=await fetch_image(meme["url"]),message = meme["title"])
            else : 
                post_info = graph.put_object(parent_object='me', connection_name='feed',message=meme["title"],link = meme["url"])

            embed = discord.Embed(title = f"from {meme['subreddit']}" ,colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
            embed.add_field(name = "Check our Facebook MEMES Page" , value= "[here](https://www.facebook.com/ArthurMemes-100739768442266)",inline=False)
            embed.add_field(name = f'{meme["score"]} :thumbsup: | {meme["num_comments"]} :speech_balloon: ',value = meme["title"],inline=False)
            embed.set_footer(text = f"post id : {post_info['post_id'].split('_')[-1]}")

            embed.set_image(url = meme['url'])
            await me.send(embed= embed)
            if meme in approvedMemes :
                removeFromApprovedMemes(meme)
            elif data : 
                if meme in data :
                    delete_meme(meme)
            block_meme(meme=meme)


        except :
            if me :
                await me.send("error while sharing on facebook")

def setup(client):
    client.add_cog(FBPage(client))
