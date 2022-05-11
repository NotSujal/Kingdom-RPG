import discord
import assist, os
from discord.ext import commands

class Test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def addcoins(self,ctx,amt:int):
        user = ctx.message.author.id
        if not str(user) == str(os.environ.get("ME")):
            await ctx.send("Sorry this is Developer only command")
            
            return
        money = assist.addcoins(user, amt)

        await ctx.send(str(money))

    @commands.command()
    async def savedata(self,ctx,key,value):
        user = ctx.message.author.id
        if not str(user) == str(os.environ.get("ME")):
            await ctx.send("Sorry this is Developer only command")
            
            return
        thing = assist.savedata(user, key, value)

        await ctx.send(str(thing))

    @commands.command()
    async def getdata(self,ctx,key):
        user = ctx.message.author.id
        if not str(user) == str(os.environ.get("ME")):
            await ctx.send("Sorry this is Developer only command")
            
            return
        thing = assist.getdata(user, key,"0")

        await ctx.send(str(thing))

    @commands.command()
    async def addinventory(self,ctx,item,amount):
        user = ctx.message.author.id
        if not str(user) == str(os.environ.get("ME")):
            await ctx.send("Sorry this is Developer only command")
            
            return
        thing = assist.addinventory(user, item, amount)
        await ctx.send(str(thing))

    @commands.command()
    async def player(self,ctx):
        user = ctx.message.author.id
        if not str(user) == str(os.environ.get("ME")):
            await ctx.send("Sorry this is Developer only command")
            
            return
        thing = assist.player_debug(user)
        await ctx.send(str(thing))

    @commands.command()
    async def clrscr(self,ctx):
        user = ctx.message.author.id
        if not str(user) == str(os.environ.get("ME")):
            await ctx.send("Sorry this is Developer only command")
            
            return
        await ctx.send("Clearing Replit database")
        assist.clrscr()
        

def setup(client):
    # client.add_cog(Test(client))
    pass