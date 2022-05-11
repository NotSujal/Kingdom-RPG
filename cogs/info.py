import discord
import  json, os
from discord.ext import commands

prefix = os.environ.get("PREFIX")
# xp required = x^2 / 100

class Info(commands.Cog):
    """Informations about Game systems, Items, Progression,etc."""
    def __init__(self, client):
        self.client = client


    # Wall of Texts
    @commands.group(invoke_without_command = True) # for this main command (.help)
    async def info(self,ctx):
        with open('data/desc.txt') as f:
            desc = f.read()
        e = discord.Embed(
            title="Guide",
            description=desc.format(prefix))
        e.set_footer(text="https://discord.com/api/oauth2/authorize?client_id=933351798243229726&permissions=412518706272&scope=bot")

        e.add_field(name=f"Use `{prefix}help info`",value="to get a list all subcommands")

        await ctx.send(embed=e)

    @info.command()
    async def skills(self,ctx):
        """Know in detail about skills"""
        e = discord.Embed(title="Skills",description="You can use a skill point to enhance your ability, each upgrade in skills cost 1 skill point, which you can collect by levelling up")
        with open("data/skills.json",'r') as f:
            data = json.load(f)
        for skill in data:
            e.add_field(name=skill.title(),value=data[skill]["desc"])

        e.set_footer(text=f"Use `{prefix}skills` command to see your skills")
        await ctx.send(embed=e)

    @info.command()
    async def world(self,ctx):
        """Know in detail about travelling and map"""
        e = discord.Embed(title="World",description="You can travel across the Islands, Fight monsters, get resources, craft items. Some locations allow you to trade your findings to other players, set up a shop, buy from other players, get good deals,etc. Depending on the locations, travelling may cost money")
        e.set_footer(text=f"Use `{prefix}map` command to know more about available locations")

        await ctx.send(embed=e)

    @info.command()
    async def levels(self,ctx): 
        """Know in detail about levels and xp"""
        e = discord.Embed(title="Levels",description="When you do any activity, battles, resource collections,etc., You earn XP(exprience). With enough exprience you can level up. \nLevelling up will buff your stats, unlock new areas, new items. With each level you are offered with a skill point which you can use to boost one of your skill permanently\nThe required xp is calculated by, `req_xp =  420/69 * curr_lvl + 100`")
        e.set_footer(text=f"Use `{prefix}help skill` command to know more about skills")
        await ctx.send(embed=e)
    
    @info.command()
    async def items(self,ctx): 
        """Know in detail about Items in game"""
        e = discord.Embed(title="Levels",description=f"We have a huge collection of items, you can access them through {prefix}items < item_name| page no>.")

        e.add_field(name="Lumber",value=f"This type of items can only be gathered by `choping` down trees `{prefix}chop`.")
        
        e.add_field(name="Ore",value=f"This type of items can only be gathered by `mining` ores `{prefix}mine`.")

        e.add_field(name="Alloy",value=f"You can `craft` these types of items. These are combination of multiple metals. `{prefix}craft`")

        e.add_field(name="Food",value="These are the items which you can `consume` and gain health points.")

        e.set_footer(text=f"Use {prefix}items command to know more about items")

        await ctx.send(embed=e)

        

def setup(client):
    client.add_cog(Info(client))