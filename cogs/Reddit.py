import praw
import discord
from discord.ext import commands , tasks
import json


from random import choice, randint
from time import time

from prawcore.exceptions import Redirect , NotFound

from config import client_id,client_secret,user_agent,facebookPageAdmins
from core import update_memes , delete_meme


reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,user_agent=user_agent)


def addToApprovedMemes(meme):
    with open("./data_base/approved_memes.json","r") as file:
        memes = json.load(file)
    if meme not in memes["memes"] :
        memes["memes"].append(meme)
        with open("./data_base/approved_memes.json","w") as file:
            json.dump(memes,file,indent=4)

class Reddit(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.name = "reddit"
        self.emoji = ":joy:"
        self.call_name = "reddit"

    @commands.command(aliases = ["surf","reddit"], description = "[subreddit]",brief = "surf reddit from discord")
    async def surfreddit(self,ctx,subreddit_name="all"):

        subreddit = reddit.subreddit(subreddit_name)

        try:
            if subreddit.over18 :
                if not ctx.message.channel.is_nsfw() :
                    await ctx.send("the channel is not nsfw")
                    return
        except Redirect:
            await ctx.send(f"there is no sureddit named {subreddit_name}")
        except NotFound:
            await ctx.send(f"there is no sureddit named {subreddit_name}")

        def check_reaction(reaction,user):
            if user == ctx.message.author:
                if reaction.emoji == "⬅️":
                    return "backward"
                if reaction.emoji == "➡️":
                    return 'forward'
            return False

        index = 0
        t_end = time() + 30        
        
        Rdata = list(subreddit.hot(limit=100))

        data = Rdata[index]

        while not data.url.endswith(("gif","jpg","png")):
            index += 1
            try :
                data = Rdata[index]
            except IndexError :
                await ctx.send("only text here no images")
        embed = discord.Embed(title = f"{subreddit}" ,colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
        embed.add_field(name = "Check our Facebook MEMES Page" , value= "[here](https://www.facebook.com/ArthurMemes-100739768442266)",inline=False)
        embed.add_field(name = f'{data.score} :thumbsup: | {data.num_comments} :speech_balloon: ',value = data.title,inline=False)
        embed.set_image(url = data.url)
        embed.set_footer(text = "sometimes it doesn't display anything beacause it's just a text ")
        msg = await ctx.send(embed= embed)
        await msg.add_reaction("➡️")

        while t_end > time():

            try :
                approve = await self.client.wait_for('reaction_add',timeout = 30.0, check=lambda reaction , user :check_reaction(reaction,user))
                # t_end += 30
            except :
                await msg.clear_reactions()
                break

            await msg.clear_reactions()

            if approve[0].emoji == "⬅️" : #backward
                index -= 1
                t_end = time() + 30

                if index == 0:
                    await msg.add_reaction("➡️") 

                if index > 0 :
                    await msg.add_reaction("⬅️")
                    await msg.add_reaction("➡️") 

            if approve[0].emoji == "➡️" : #forward
                index += 1
                t_end = time() + 30
                if index < len(Rdata) :
                    await msg.add_reaction("⬅️")
                    await msg.add_reaction("➡️")
                elif index > len(Rdata):
                    index == -1
                    await msg.add_reaction("⬅️")

            data = Rdata[index]
            
            embed = discord.Embed(title = f"{subreddit}" ,colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
            embed.add_field(name = f'{data.score} :thumbsup: | {data.num_comments} :speech_balloon: ',value = data.title)
            embed.set_image(url = data.url)
            # embed.set_footer(text = "sometimes it doesn't display anything beacause it's just a text ")


            await msg.edit(embed = embed)

        await msg.clear_reactions()
        await ctx.send('the reddit viewer is no longer fonctionnelle')


    @commands.command(description = "[nothing]",brief = "fresh memes from REDDIT")
    async def meme(self,ctx):
        data = update_memes(reddit)

        memeinfo = choice(data)

        while int(memeinfo["score"]) < 30000 :
            delete_meme(memeinfo)
            data = update_memes(reddit)

            memeinfo = choice(data)

        embed = discord.Embed(title = f"from {memeinfo['subreddit']}" ,colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
        embed.add_field(name = "Check our Facebook MEMES Page" , value= "[here](https://www.facebook.com/ArthurMemes-100739768442266)",inline=False)
        embed.add_field(name = f'{memeinfo["score"]} :thumbsup: | {memeinfo["num_comments"]} :speech_balloon: ',value = memeinfo["title"])
        embed.set_image(url = memeinfo['url'])
        embed.set_footer(text= "give it a thumbs up to post it in our facebook page")
        msg = await ctx.send(embed= embed)

        await msg.add_reaction("👍")

        def check_reaction(reaction,user):
            if user.id in facebookPageAdmins:
                if reaction.emoji == "👍":
                    return "Approved"
            return False

        delete_meme(memeinfo)

        try :
            approve = await self.client.wait_for('reaction_add',timeout = 30.0, check=lambda reaction , user :check_reaction(reaction,user))
            if approve[0].emoji == "👍" : # confirm approve 
                posted_meme = approve[0].message.embeds[0].to_dict()
                if posted_meme["image"]["url"] == memeinfo["url"] or posted_meme["fields"][0]["value"] == memeinfo["title"] :
                    addToApprovedMemes(memeinfo)
        except :
            await msg.clear_reactions()


    
    @commands.command(name="update_memes",aliases = ["new_memes","upmeme"], description = "[nothing]",brief = "update memes stock")
    @commands.cooldown(1, 86400, commands.BucketType.guild)
    async def _update_memes(self,ctx):
        update_memes(reddit,ALL=True)
        await ctx.send("up to date mate !")
        
def setup(client):
    client.add_cog(Reddit(client))
