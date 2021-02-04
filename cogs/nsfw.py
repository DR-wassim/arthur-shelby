import discord 
from discord.ext import commands
import praw
import json
from random import choice, randint
from time import time 

from config import client_id , client_secret , user_agent

reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,user_agent=user_agent)

def update_content(subname):
    with open("./data_base/nsfw.json","r") as f:
        data = json.load(f)

    last_update = float(data["last_update"])

    if last_update <= float(time() - 3600) or not data["posts"][subname]:
        last_update = time() + 3600

        data["last_update"] = last_update

        data["posts"][subname] = []
        for post in list(reddit.subreddit(subname).hot(limit=100)):
            if post.url[-3:] in ["jpg","png","gif"]:
                data["posts"][subname].append({'title' : post.title , "num_comments" : post.num_comments  , "score":post.score, "url": post.url})

        with open("./data_base/nsfw.json","w") as f:
            json.dump(data,f,indent = 4)

    return data["posts"][subname]

def delete(post,subreddit):
    with open("./data_base/nsfw.json","r") as f:
        data = json.load(f)
    data["posts"][subreddit].remove(post)
    with open("./data_base/nsfw.json","w") as f:
        json.dump(data,f,indent=4)

def prepare_embed(subreddit):
    data = update_content(subreddit)
    postcontnt = choice(data)
    embed = discord.Embed(title = f"from r\\{subreddit}" ,colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
    embed.add_field(name = f'{postcontnt["score"]} :thumbsup: | {postcontnt["num_comments"]} :speech_balloon: ',value = postcontnt["title"])
    embed.set_image(url = postcontnt['url'])
    embed.set_footer(text ="this shit ain't good for you, go find a gf for God's sake")
    delete(postcontnt,subreddit)
    return embed

class nsfw(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.name = "NSFW"
        self.emoji = ":kiss:"
        self.call_name = "nsfw"        

    @commands.command(aliases = ["sex","34","rule","rule34","hentai","boobs","boob","tites","tite","ass","pussy"],description = '[no parametres]' ,brief = "best porn pics in the world")
    async def porn(self,ctx):
        if ctx.message.channel.type == discord.ChannelType.private or ctx.message.channel.is_nsfw():
            type = ctx.message.content.replace(ctx.prefix,"").split(" ")[0]
            if type in ["sex"] :
                type = "porn"
            elif type in ["34","rule"] :
                type = "rule34"
            elif type in ["boob","tites","tite"] :
                type = "boobs"
            elif type in ["pussy"] :
                type = "ass"

            embed = prepare_embed(type)
            await ctx.send(embed= embed)
        else :
            await ctx.send('this commands works only in a nsfw channel')

def setup(client):
    client.add_cog(nsfw(client))