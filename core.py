from io import BytesIO
import os
import json
import discord
from PIL import Image



def listToString(listt : list , seprate = "-" , PrefixAndSufix = "") -> str :
    result = ""  
    for x in listt :
        result += PrefixAndSufix + str(x) + PrefixAndSufix + f' {seprate} '

    result = result[:-3]
    return result

def cogsList() -> list:
    cogs_list = []
    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            cogs_list.append(filename[:-3])
    return cogs_list


def check_if_blocked(meme_title):
    with open("./data_base/blocked_memes.json","r") as f :
        blocked = json.load(f)
    return meme_title not in blocked["by_me"] or meme_title not in blocked["already_posted"]

def block_meme(type_of_block = "already_posted",*,meme = None):
    if meme:
        with open("./data_base/blocked_memes.json","r") as f:
            blocked = json.load(f)
        if isinstance(meme,dict) :
            blocked[type_of_block].append(meme["title"])
        elif isinstance(meme,str) :
            blocked[type_of_block].append(meme)
        with open("./data_base/blocked_memes.json","w") as f:
            json.dump(blocked,f,indent=4)


def delete_meme(meme):
    with open("./data_base/memes.json","r") as f:
        data = json.load(f)
    data["memes"].remove(meme)
    with open("./data_base/memes.json","w") as f:
        json.dump(data,f,indent=4)


def update_memes(reddit ,ALL : bool = False) -> list:
    with open("./data_base/memes.json","r") as f:
        data = json.load(f)

    titles = []

    if data["memes"] == [] or ALL:
        for subname in ["dankmemes","memes"]:
            for post in list(reddit.subreddit(subname).hot(limit=100)):
                if check_if_blocked(post.title):
                    if post.url[-3:] in ["gif","jpg","png"]:
                        if post.score > 30000 :
                            if post.title not in titles :
                                data["memes"].append({'title' : post.title , "num_comments" : post.num_comments  , "score":post.score, "url": post.url,"subreddit" : subname})
                                titles.append(post.title)

        with open("./data_base/memes.json","w") as f:
            json.dump(data,f,indent = 4)

    return data["memes"]

def collect_data(guild):
    with open ('./data_base/users_data.json','r') as users_data :
        data = json.load(users_data)
    try:
        members = guild.members
    except AttributeError :
        members = guild
    for member in members :
        if member.bot == False :
            if str(member.id) not in data :
                data[str(member.id)] = {"name" : member.name}
                with open ('./data_base/users_data.json','w') as users_data :
                    json.dump(data,users_data,indent=4)


def collect_personal_data(member : discord.Member):
    with open ('./data_base/users_data.json','r') as users_data :
        data = json.load(users_data)

    if member :
        if not member.bot :
            if str(member.id) not in data :
                data[str(member.id)] == {"name" : member.name}

                with open ('./data_base/users_data.json','w') as users_data :
                    json.dump(data,users_data,indent=4)

def image_to_byte_array(image:Image):
    arr = BytesIO()
    image.save(arr, format=image.format)
    arr.seek(0)
    return arr