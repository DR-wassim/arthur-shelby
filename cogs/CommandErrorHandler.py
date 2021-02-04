import traceback
import sys
from discord.ext import commands
import discord
import asyncio
import aiohttp
import platform
import logging

from discord.ext.commands.errors import PrivateMessageOnly 


from config import owner_id

class CommandErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.name = "CommandErrorHandler"
        self.emoji = "None"
        self.call_name = "None"
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        repport_me = True

        error = getattr(error, 'original', error)


        # if isinstance(error , discord.ext.commands.errors.CommandError) :
        #     repport_me = True
        #     return

        

        if isinstance(error,commands.errors.CommandNotFound):
            repport_me = False
            return await ctx.send(f'there is no command named ***{ctx.message.content}*** \n what are talkin about ?!')

        elif isinstance(error, commands.errors.CommandInvokeError) :
            return await ctx.send("error")

        elif isinstance(error, commands.DisabledCommand) :
            return await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error,commands.errors.CommandOnCooldown):
            return await ctx.send(f"ho ho cooldown you have to wait {str(error)[-6:]} before you can use this command again")

        elif isinstance(error, discord.errors.Forbidden):
            return await ctx.send("Forbidden")

        elif isinstance(error, discord.errors.NotFound):
            return await ctx.send("Not Found")

        # elif isinstance(error, discord.errors.HTTPException):
        #     repport_me = True
        #     return await ctx.send('connection error :\ sorry')


        # elif isinstance(error,AttributeError):
            # return await ctx.send("not possible")


        elif isinstance(error, UnboundLocalError):
            pass

        elif isinstance(error, UserWarning):
            pass

        elif isinstance(error, AttributeError):
            pass

        elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            pass

        elif isinstance(error, aiohttp.client_exceptions.ServerDisconnectedError):
            pass

        elif isinstance(error, TimeoutError):
            pass


        elif isinstance(error,PrivateMessageOnly):
            return await ctx.send("{ctx.command} can be used only in DMs")

        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')

        elif isinstance(error, commands.BadArgument):
            return await ctx.send('please cheack the help command bcz your arguments sucks')

        elif isinstance(error , commands.MissingRequiredArgument) :
            return await ctx.send('missing required argument \n please use help command to find out how to use this command')

        elif isinstance(error , commands.TooManyArguments) :
            return await ctx.send('what is all this you provided more than necessary arguments')

        elif isinstance(error , commands.BotMissingPermissions) :
            return await ctx.send('i don\'t have the necessary  permissions please talk to admins to provide them')
        
        elif isinstance(error , commands.MissingPermissions) :
            return await ctx.send('Missing Permissions')

        elif isinstance(error , commands.ExtensionError) :
            return await ctx.send('system failed an error in a lot of places XDD')


        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        if repport_me :

            try :
                me  = self.client.get_user(owner_id)
                system ="`" + platform.uname()[0] + " " + platform.uname()[3] + " " + platform.uname()[1] + "`"
                await me.send(f'{system} : `Ignoring exception in message ***{ctx.message.content}***  {error} {error.__traceback__}`')
            except :
                logging.basicConfig(filename='sys.log', encoding='utf-8', level=logging.DEBUG)
                logging.error(f'Ignoring exception in message ***{ctx.message.content}***  {error} {error.__traceback__}')




def setup(client):
    client.add_cog(CommandErrorHandler(client))