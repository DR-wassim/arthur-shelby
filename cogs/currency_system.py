from discord.ext import commands
import discord
import json
import datetime
from random import randint
import time
import asyncio


def get_bank_info(info_name : str) :
    with open("./data_base/bank_info.json","r") as data :
        bank_info = json.load(data)
    return bank_info[info_name]

def change_bank_info(info_name : str,new_name : str) :
    with open("./data_base/bank_info.json",'r') as data :
        bank_info = json.load(data)
    bank_info[info_name] = new_name
    with open("./data_base/bank_info.json",'w') as data :
        json.dump(bank_info,data,indent = 4)

class Account:
    def __init__(self, name: str, user_id : int, balance: int, wallet: int):
        self.name = name
        self.user_id = user_id
        self.balance = balance
        self.wallet = wallet



def _invalid_amount(amount: int):
    return bool(amount > 0)

def get_inventory(member :discord.Member):
    with open("./data_base/users_data.json" , "r") as users_data :
        data = json.load(users_data)

    if 'inventory' not in data[str(member.id)]:
        data[str(member.id)]["inventory"] = {}
        with open("./data_base/users_data.json" , "w") as users_data :
            json.dump(data , users_data ,indent = 4)
        with open("./data_base/users_data.json" , "r") as users_data :
            data = json.load(users_data)

    return data[str(member.id)]["inventory"]

def add_to_inventory(member : discord.Member,item : str,item_description =None,times :int = 1):
    with open("./data_base/users_data.json","r") as items_data:
        data = json.load(items_data)

    if 'inventory' not in data[str(member.id)]:
        data[str(member.id)]['inventory'] = {}
        
    if item not in data[str(member.id)]["inventory"]:
        data[str(member.id)]["inventory"][item] = {"description" : item_description,"qantity" : times}
    elif item in data[str(member.id)]["inventory"] :
        data[str(member.id)]["inventory"][item]["qantity"] += times

    with open("./data_base/users_data.json","w") as items_data:
        json.dump(data,items_data,indent=4)

def remove_from_inventory(member : discord.Member,item : str):
    with open("./data_base/users_data.json","r") as items_data:
        data = json.load(items_data)
        
    if item not in data[str(member.id)]["inventory"]:
        # data[str(member.id)]["inventory"][item] = {"description" : item_description,"qantity" : 1}
        return False
    elif item in data[str(member.id)]["inventory"] :
        if data[str(member.id)]["inventory"][item]["qantity"] == 1:
            del(data[str(member.id)]["inventory"][item])
        elif data[str(member.id)]["inventory"][item]["qantity"] > 1:
            data[str(member.id)]["inventory"][item]["qantity"] -= 1

    with open("./data_base/users_data.json","w") as items_data:
        json.dump(data,items_data,indent=4)


def get_items():
    with open("./data_base/shop_items.json","r") as items_data:
        items = json.load(items_data)
    return items

def can_spend_from_wallet(member : discord.Member ,amount :int ) :
    return get_account(member).wallet >= amount

def can_spend_from_balance(member : discord.Member ,amount :int ) :
    return get_account(member).balance >= amount

def minus_wallet(member : discord.Member, amount : int) :
    if _invalid_amount(amount) :
        with open('./data_base/users_data.json',"r") as users_data :
            data = json.load(users_data)
        if "C.S" not in data[str(member.id)]:
            get_account(member)
        if "C.S" in data[str(member.id)]:
            data[str(member.id)]["C.S"]["wallet"] -= amount
            with open('./data_base/users_data.json',"w") as users_data :
                json.dump(data,users_data,indent=4)

def plus_wallet(member : discord.Member , amount : int) :
    if _invalid_amount(amount) :
        with open('./data_base/users_data.json',"r") as users_data :
            data = json.load(users_data)
        if "C.S" not in data[str(member.id)]:
            get_account(member)
        if "C.S" in data[str(member.id)]:
            data[str(member.id)]["C.S"]["wallet"] += amount
            with open('./data_base/users_data.json',"w") as users_data :
                json.dump(data,users_data,indent=4)

def plus_balance(member : str, amount : int) :
    if _invalid_amount(amount) :
        with open('./data_base/users_data.json',"r") as users_data :
            data = json.load(users_data)
        if "C.S" not in data[str(member.id)]:
            get_account(member)
        if "C.S" in data[str(member.id)]:
            data[str(member.id)]["C.S"]["bank"] += amount
            with open('./data_base/users_data.json',"w") as users_data :
                json.dump(data,users_data,indent=4)

def minus_balance(member : discord.Member , amount : int) :
    if _invalid_amount(amount) :
        with open('./data_base/users_data.json',"r") as users_data :
            data = json.load(users_data)
        if "C.S" not in data[str(member.id)]:
            get_account(member)
        if "C.S" in data[str(member.id)]:
            data[str(member.id)]["C.S"]["bank"] -= amount
            with open('./data_base/users_data.json',"w") as users_data :
                json.dump(data,users_data,indent=4)



def get_account(member : discord.member.Member):
    with open('./data_base/users_data.json','r') as users_data :
        data = json.load(users_data)

    if "C.S" not in data[str(member.id)] :
        data[str(member.id)]["C.S"] = {"wallet" : 0 , "bank" : 0}
        with open('./data_base/users_data.json','w') as users_data :
            json.dump(data,users_data,indent=4)
        with open('./data_base/users_data.json','r') as users_data :
            data = json.load(users_data)

    return Account(  [member.name] , member.id,data[str(member.id)]["C.S"]["bank"] , data[str(member.id)]["C.S"]["wallet"] )
            #name: str, user_id : int, balance: int, wallet: str

class currency_system(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.name = "currency system"
        self.emoji = ":money_with_wings:"
        self.call_name = "currency_system"

    @commands.command(aliases = ['bal'],brief = "show your bank account and wallet")
    async def balance(self,ctx , member : discord.Member  = None):
        '''[member] if None I will show yours'''

        if ctx.message.channel.type == discord.message.ChannelType.private or member == None:
            member = ctx.message.author
        elif member not in ctx.guild.members :
            await ctx.send(f'there is no one named {member}')
        try :
            user = get_account(member)
        except KeyError :
            await ctx.send('this user have no account in our bank')
            return
        embed = discord.Embed(title = f"{member.name} 's balance" ,colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
        embed.add_field(name =" bank : " ,value= f"{user.balance} {get_bank_info('currency')}")
        embed.add_field(name =" wallet : " ,value= f"{user.wallet} {get_bank_info('currency')}")

        await ctx.send(embed = embed)

    @commands.command(brief = "hhhhhhhhh begging people, what a shame")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg (self,ctx):
        '''no parametres '''
        amount = randint(15,150)
        plus_wallet(ctx.message.author,amount)
        await ctx.send(f"Thomas gave u {amount} {get_bank_info('currency')}")


    @commands.command(aliases = ["change bank name" , "CHBN" ,"CBN" ,"cbn"],brief= "obviously change bank name ")
    async def change_bank_name(self,ctx,new_name : str) :
        '''[new bank name]'''
        change_bank_info('bank_name',new_name)
        await ctx.send("Done !!")

    @commands.command(aliases = ["change currency name" , "CHCN" ,"CCN" ,"ccn"],brief = "obviously change currecny system")
    async def change_currency_name(self,ctx , name : str ):
        '''[ new name ]'''
        change_bank_info('currency',name)
        await ctx.send("Done !!")

    @commands.command(aliases = ["get bank name" , "GBN"  ,"gbn"],brief = "obviously get bank name")
    async def get_bank_name(self,ctx) :
        '''no parametres'''
        await ctx.send(get_bank_info('bank_name'))

    @commands.command(aliases = ["get currency name" , "GCN"  ,"gcn"], brief = "obviously get currency name")
    async def get_currency_name(self,ctx ):
        '''no parametres'''
        await ctx.send(get_bank_info('currency'))

    @commands.command(aliases = ["transfer" , "TRA"  ,"tra"],brief = f"give other some {get_bank_info('currency')} from your bank account")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def transfer_credits(self,ctx,member : discord.Member , amount : int):
        '''[ mention a member ] [ amount ]'''
        if _invalid_amount(amount):
            if can_spend_from_balance(ctx.message.author,amount) :
                plus_balance(member,amount)
                minus_balance(ctx.message.author , amount)
            else :
                await ctx.send(f"{ctx.message.author} you don't have this amount {amount} in your bank")
        else:
            await ctx.send("invalid amount")

    @commands.command(aliases = ["donate" , "yssa5if_le5ra" , "don"]  , brief = "give other some money from your bank account")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def give(self,ctx,member : discord.Member , amount : int):
        '''[ mention a member ] [ amount ]'''
        if _invalid_amount(amount):
            if can_spend_from_wallet(ctx.message.author,amount) :
                plus_wallet(member,amount)
                minus_wallet(ctx.message.author , amount)
                await ctx.send("done !!")
            else :
                await ctx.send(f"{ctx.message.author} you don't have this amount {amount} in your wallet")
        else:
            await ctx.send("invalid amount")

    @commands.command(aliases = ["inv","home"],brief = "open your inventory")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def inventory(self,ctx): #,member : discord.Member = None
        '''no parametres'''

        def check_reaction(reaction,user):
            if user == ctx.message.author:
                if reaction.emoji == "⬅️":
                    return "backward"
                if reaction.emoji == "➡️":
                    return 'forward'
                if reaction.emoji == "❌" : 
                    return "close"

            return False

        i = 0
        k = 5

        member = ctx.message.author
        embed = discord.Embed(title = f"{member.name.upper()}'s inventory" , colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
        inv = get_inventory(member)
        if inv == {} or inv == None:
            embed.add_field(name = "items : " , value = "empty")
            await ctx.send (embed=embed)
            return

        item_list = []

        for item in inv:
            item_list.append(item)
        itemss = item_list[i:k]

        msgcontent = ""
        for item in itemss :
            msgcontent += f"**{item}** X {str(inv[item]['qantity'])}" + "\n"
        embed.add_field(name = "items : " , value = msgcontent)
        msg = await ctx.send (embed=embed)

        if len(itemss) >= 5 :
            await msg.add_reaction("⬅️")
            await msg.add_reaction("➡️")
            await msg.add_reaction("❌")

            close = False

            while not close:
                try :
                    approve = await self.client.wait_for('reaction_add',timeout = 30.0, check=lambda reaction , user :check_reaction(reaction,user))
                except :
                    await msg.clear_reactions()
                    break

                await msg.clear_reactions()

                if approve[0].emoji == "❌" : 
                    close = True
                    break

                if approve[0].emoji == "⬅️" : #backward
                    i -= 5
                    k -= 5

                if approve[0].emoji == "➡️" : #forward
                    i += 5
                    k += 5

                i%=len(item_list)
                k%=len(item_list)

                if i > k :
                    itemss = item_list[i:] + item_list[:k]
                
                else :
                    itemss = item_list[i:k]

                

                msgcontent = ""

                embed = discord.Embed(title = "SHOP" , colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
                for item in itemss :
                    msgcontent += f"**{item}** X {str(inv[item]['qantity'])}" + "\n"
                embed.add_field(name = "items : " , value = msgcontent)
                await msg.edit(embed = embed)

                await msg.add_reaction("⬅️")
                await msg.add_reaction("➡️")
                await msg.add_reaction("❌")


            await msg.clear_reactions()
            await ctx.send('your inventory is no longer fonctionnelle')




    @commands.command(aliases = ["s"] ,brief= "open the shop")
    @commands.guild_only()
    async def shop(self, ctx) :
        ''' no parametres '''
        items_emojies = ["1️⃣" ,"2️⃣" ,"3️⃣" ,"4️⃣" ,"5️⃣" ]

        def check_reaction(reaction,user):
            if user == ctx.message.author:
                if reaction.emoji == "⬅️":
                    return "backward"
                if reaction.emoji == "➡️":
                    return 'forward'
                if reaction.emoji in items_emojies :
                    return "buying"
                if reaction.emoji == "❌" : 
                    return "close"
            return False

        i = 0
        k = 5

        embed = discord.Embed(title = "SHOP" , colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
        items = get_items()
        item_list = []
        for item in items:
            item_list.append(item)
        itemss = item_list[i:k]
        msgcontent = ""
        for index,item in enumerate(itemss) :
            msgcontent += f"{items_emojies[index]} - **{item}** | {str(items[item]['price'])} | " + str(items[item]['type']) + "\n" + str(items[item]['description']) + "\n \n"
        embed.add_field(name = "items : " , value = msgcontent,inline= False)
        embed.add_field(name = "tips : " ,value= "wait until the shop magazine is fully loaded",inline=False)

        embed.set_footer(text = "react with the item number to buy it")

        msg = await ctx.send(embed = embed)
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")
        await msg.add_reaction("❌")


        for emoji in items_emojies :
            await msg.add_reaction(emoji)

        close = False

        while not close:
            try :
                approve = await self.client.wait_for('reaction_add',timeout = 30.0, check=lambda reaction , user :check_reaction(reaction,user))
            except :
                await msg.clear_reactions()
                break

            await msg.clear_reactions()

            if approve[0].emoji in items_emojies :
                
                item_index = items_emojies.index(approve[0].emoji)
                await ctx.invoke(self.client.get_command("buy"),item = itemss[item_index],times = "1")

            elif approve[0].emoji == "❌" : 
                close = True
                break

            elif approve[0].emoji == "⬅️" :
                i -= 5
                k -= 5

            elif approve[0].emoji == "➡️" :
                i += 5
                k += 5

            i%=len(item_list)
            k%=len(item_list)

            if i > k :
                itemss = item_list[i:] + item_list[:k]
            
            else :
                itemss = item_list[i:k]

            msgcontent = ""

            embed = discord.Embed(title = "SHOP" , colour = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255)))
            for index,item in enumerate(itemss) :
                msgcontent += f"{items_emojies[index]} - **{item}** | {str(items[item]['price'])} | " + str(items[item]['type']) + "\n" + str(items[item]['description']) + "\n \n"
            embed.add_field(name = "items : " , value = msgcontent,inline=False)
            embed.add_field(name = "tips : " ,value= "wait until the shop magazine is fully loaded",inline=False)
            embed.set_footer(text = "react with the item number to buy it")
            await msg.edit(embed = embed)
            
            await msg.add_reaction("⬅️")
            await msg.add_reaction("➡️")
            await msg.add_reaction("❌")

            for index, emoji in enumerate(items_emojies) :
                if int(index+1) > len(itemss) :
                    break
                await msg.add_reaction(emoji)


        await msg.clear_reactions()
        await ctx.send('the shop magazine is no longer fonctionnelle')

    @commands.command(aliases = ["with"] , brief = "get money from your bank account")
    async def withdraw_credits(self,ctx,amount):
        ''' [amount] '''

        if amount == "all":
            amount = int(get_account(ctx.message.author).balance)

        if isinstance(amount,int) or amount.isdigit() :
            if _invalid_amount(int(amount)):
                if can_spend_from_balance(ctx.message.author, int(amount)):
                    minus_balance(ctx.message.author,int(amount))
                    plus_wallet(ctx.message.author,int(amount))
                    await ctx.send("done !!")
                else :
                    await ctx.send(" you don't have this much in your bank account")
            else :
                await ctx.send('invalid amount')
        else : 
            await ctx.send("please provide a valid amount")

    @commands.command(aliases = ["dep"] , brief = "deposit to your bank account")
    async def deposit_credits(self,ctx,amount :str):
        ''' [amount] '''
        if amount == "all":
            amount = int(get_account(ctx.message.author).wallet)

        if isinstance(amount,int) or amount.isdigit() :
            if _invalid_amount(int(amount)):
                if can_spend_from_wallet(ctx.message.author,int(amount)):
                    minus_wallet(ctx.message.author,int(amount))
                    plus_balance(ctx.message.author,int(amount))
                    await ctx.send("done !!")
                else :
                    await ctx.send(" you don't have this much in your wallet")
            else :
                await ctx.send('invalid amount')
        else : 
            await ctx.send("please provide a valid amount")

    @commands.command(description = "[item name] [times defualt 1]",brief = "buy available items from the shop")
    async def buy(self,ctx,times :str = "1" ,*,item : str = None):
        ''' [item name from the shop] '''
        
        if times.isdigit():
            times = int(times)
        else :
            if item :
                item = times + " " + item
            else : 
                item = times
            times = 1
        if item != None :
            items = get_items()

            if item in items.keys():
                if can_spend_from_wallet(ctx.message.author,int(items[item]["price"])*times) :
                    add_to_inventory(ctx.message.author , item,items[item]["description"],times)
                    minus_wallet(ctx.message.author,int(items[item]["price"]))
                    await ctx.send(f"{ctx.message.author.name} bought {item}")
                elif can_spend_from_balance(ctx.message.author,int(items[item]["price"])*times):
                    add_to_inventory(ctx.message.author , item,items[item]["description"],times)
                    minus_balance(ctx.message.author,int(items[item]["price"]))
                    await ctx.send(f"{ctx.message.author.mention} bought {item} with his credit card")
                else :
                    await ctx.send("you don't have enough money")
            else :
                await ctx.send(f'we don\'t have {item} in our shops')
        else :
            await ctx.send("choose an item or visit the shop")

    @commands.group(brief = "use the items from your inventory",description='[item name]')
    async def use(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('there is no item with this name')

    @use.command(name = "m4-16",aliases = ["m4","m416"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def m4_16(self,ctx,target : discord.Member):
        if "m4-16" in get_inventory(ctx.message.author) :
            remove_from_inventory(ctx.message.author , "m4-16")
            await ctx.send(f"{ctx.message.author.mention} shot {target.mention} in the head \n {target.mention} lost his wallet ")
            amount = int(get_account(target).wallet)
            minus_wallet(target,amount)
        else :
            await ctx.send("you don't have m4-16 go buy one from the shop")

    @use.command(name = "magic",aliases = ["spell"])
    @commands.cooldown(1,30,commands.BucketType.user)
    async def magic_book(self,ctx,target:discord.Member):
        if 'Magic Book' in get_inventory(ctx.message.author):
            spell = "Expecto Patronum"
            await ctx.send(spell)
            await ctx.send(f'Gets rid of pesky Dementors like {target.mention} by summoning a badass Patronus to chase them away.')
            remove_from_inventory(ctx.message.author,"Magic Book")
        else:
            await ctx.send("you don't have Magic Book go buy one from the shop")


def setup(client):
    client.add_cog(currency_system(client))

