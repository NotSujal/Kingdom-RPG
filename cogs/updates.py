import discord
import assist, os, json
from discord.ext import commands

class User(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['changelogs','cl','changes','logs'])
    async def changelog(self,ctx,id:int=None):
        """Get all the past updates of the bot"""
        with open("data/changelog.json")as f:
            logs = json.load(f)

        if id == None:
            e = discord.Embed(title=str(self.client.user) + " Changlogs")
            i = 0
            for log in logs:
                i +=1
                e.add_field(name=f"{i}. {logs[log]['title']}",value=log,inline=False)

            await ctx.send(embed=e)
        else:
            id -=1
            try:
                #get correct log
                logs = logs[list(logs.keys())[id]]
                e = discord.Embed(title=logs['title'],description=logs['desc'])

                for name in logs['fields']:
                    e.add_field(name=name,value=logs['fields'][name])
                
                await ctx.send(embed=e)
            except IndexError:
                await ctx.send(
                    embed=discord.Embed(
                        title="Out of Logs",
                        description="I searched long and hard, but the point is, my developers are lazy so there are not many changelogs"
                    )
                )
        

def setup(client):
    client.add_cog(User(client))