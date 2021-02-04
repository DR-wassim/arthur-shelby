import discord 
from discord.ext import commands
from random import randint

class magic8ball(commands.Cog)  :
    def __init__(self,client):
        self.client = client
        self.name = "magic 8ball"
        self.emoji = ":8ball:"
        self.call_name = "magic8ball"

    @commands.command(name = '8ball',description = "[your qestion]" ,brief="answer all your questions")
    async def _8ball (self ,ctx,*,question :str = None):
        affirmative  = [" It is certain." , "It is decidedly so." , "Without a doubt." , "Yes – definitely.","You may rely on it.","As I see it, yes.","Most likely.","Outlook good.","Yes.","Signs point to yes."]

        non_committal = ["Reply hazy, try again.","Ask again later.","Better not tell you now.","Cannot predict now.","Concentrate and ask again."]

        negative = ["Don't count on it.","My reply is no." ," My sources say no.","Outlook not so good.","Very doubtful.","sadly no","le voiçi"]

        if question != None :
            if "wassim" in question and "gay" in question :
                answer_type = 2
            else :
                answer_type = randint(0,2)
            
            answer = 'error'
            color = discord.Colour.from_rgb(randint(0,255),randint(0,255),randint(0,255))
            if answer_type == 0 :
                answer = affirmative[randint(0,len(affirmative))]
                color = discord.Colour.dark_green()
            if answer_type == 1 :
                answer = non_committal[randint(0,len(non_committal))]
                color = discord.Colour.dark_gold()
            if answer_type == 2 :
                answer = negative[randint(0,len(negative))]
                color = discord.Colour.dark_red()


            
            embed = discord.Embed(title = "***8ball***" , colour = color)
            embed.add_field(name = "your question : " + str(question) , value= str(answer))
            await ctx.send(embed = embed)
        else : 
            await ctx.send("make sure you write a question next time or don't come back")

def setup(client):
	client.add_cog(magic8ball(client))