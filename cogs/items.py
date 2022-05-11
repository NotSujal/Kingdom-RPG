import discord
import assist, json,os, random
from discord.ext import commands

prefix = os.environ.get("PREFIX")
class Items(commands.Cog):
    """Commands related to Items"""
    def __init__(self, client):
        self.client = client
        
    @commands.command(pass_context=True,aliases=["inv","e"])
    async def inventory(self,ctx,page:int=1):
        """Open Your Inventory"""

        user = str(ctx.message.author.id)
        inv = assist.getdata(user,"inv",{})
        try: inv = json.loads(inv)
        except: pass
        print(type(inv))
        e = discord.Embed(title=f"{ctx.message.author.name}'s Inventory Page: {page}")

        starting_no = (int(page) -1) * 10
        string = ""
        i = 1
        for keys in inv:
            if i >= starting_no and i <= starting_no + 10:
                string += f"{i}. {keys} *({inv[keys]})* \n"
            else:
                i +=1
                continue
            i +=1
        if string == "":
            string = "Not enough items for this page"
        e.add_field(name="Amount (Item)",value = string)

        await ctx.send(embed = e)


    @commands.command(pass_context=True,aliases=["item"])
    async def items(self,ctx,*,filter:str=None):

        #get page and filter
        try:
            page = int(filter)
            name = None
        except:
            name = filter
            page = 1

        with open("data/items.json",'r') as f:
            items = json.load(f)

        # show all items
        if name == None:
            e = discord.Embed(title="Provide a name to get details",description=f"Page: {page}")
            string = ""
            starting_no = (page -1) * 20
            i = 1
            for word in items.keys():
                
                if i >= starting_no and i <= starting_no + 20:
                    string += f"{i}. {word} \n"
                else:
                    i +=1
                    continue
                i +=1
            if string == "":
                string = "Not enough items for this page"
            e.add_field(name="Available Items:",value = string)
            
            await ctx.send(embed=e)
            return

        # auto_complete filter
        name = assist.auto_complete(name,"items")
        if not name:
            await ctx.send(f"Aoy! It seems u messed up, do `{prefix}info items`")

        #create Embed
        e = discord.Embed(title="Location Details:")
        temp = items[name]
        e.add_field(name="Name:", value=name)
        e.add_field(name="Description:", value=temp['desc'],inline=False)
        _recipe_value = ""
        _recipe = temp["recipe"]
        if len(_recipe.keys()) == 0:
            _recipe_value = "Cannot Be Crafted!"
        for _item in _recipe:
            _recipe_value += f"> {_item}  *({_recipe[_item]})*\n" 
        e.add_field(name="Recipe:", value=_recipe_value,inline=False)
        e.add_field(name="Type:", value=temp['meta']['type'],inline=False)

        await ctx.send(embed=e)
        
    @commands.cooldown(1, 300)
    @commands.command(pass_context=True)
    async def mine(self,ctx):
        """Mine for ores in your current location"""
        #get required data
        user = str(ctx.message.author.id)
        user_loc = assist.getdata(user,'loc',"House")
        with open('data/locations.json')as f:
            ores = json.load(f)[user_loc]['ore']
        if len(ores) >0:
            the_chosen_one = random.choice(ores)
        else:
            the_chosen_one = "None"
        the_chosen_amount = random.randint(1,3)

        with open('data/items.json') as f:
            items = json.load(f)

        #get users pick stats
        users_pick = assist.getdata(user,'pickaxe',"None")
        if users_pick == "None":
            await ctx.send(
                embed=discord.Embed(
                    title="You need Pickaxe",
                    description="Your fists are not that strong to punch rocks. Go get a Pickaxe, either craft it or buy it."
                )
            )
            return

        #consider multipliers
        ehnance_factor  = items[assist.getdata(user,'pickaxe',"None")]['meta']['qfac']
        skill_factor = int(assist.getdata(user,'mining',"0"))
        the_chosen_amount += int(random.randint(0,3) * int(ehnance_factor) * (1 + int(skill_factor)/2))

        #construct embeds
        if the_chosen_one != "None":
            assist.addinventory(user,the_chosen_one,the_chosen_amount)
            
            e = discord.Embed(
                title=f"{ctx.message.author.name} went mining",
                description=f"{ctx.message.author.name} found **{the_chosen_amount} {the_chosen_one}**. It was added to inventory",
            )
        else:
            e = discord.Embed(
                title=f"{ctx.message.author.name} went mining",
                description=f"{ctx.message.author.name} you __cannot__ mine here! There are no ores here. Do `{prefix}loc`",
            )
        await ctx.send(embed=e)



    @commands.cooldown(1, 200)
    @commands.command(pass_context=True)
    async def chop(self,ctx):
        """Chop for lumber in your current location"""
        #get required data
        user = str(ctx.message.author.id)
        user_loc = assist.getdata(user,'loc',"House")
        with open('data/locations.json')as f:
            ores = json.load(f)[user_loc]['lumber']
        if len(ores) >0:
            the_chosen_one = random.choice(ores)
        else:
            the_chosen_one = "None"
        the_chosen_amount = random.randint(1,3)
        with open('data/items.json') as f:
            items = json.load(f)
        
        #get users axe stats
        users_axe = assist.getdata(user,'axe',"None")
        if users_axe == "None":
            await ctx.send(
                embed=discord.Embed(
                    title="You need Axe",
                    description="Your fists are made for punching enemies not logs. Go get a axe, either craft it or buy it."
                )
            )
            return

        #consider multipliers
        ehnance_factor  = items[users_axe]['meta']['qfac']
        skill_factor = int(assist.getdata(user,'lumberjack',"0"))
        the_chosen_amount += int(random.randint(0,3) * int(ehnance_factor) * (1+ int(skill_factor)/2))

        #construct embeds
        if the_chosen_one != "None":
            assist.addinventory(user,the_chosen_one,the_chosen_amount)
            
            e = discord.Embed(
                title=f"{ctx.message.author.name} went chopping",
                description=f"{ctx.message.author.name} found **{the_chosen_amount} {the_chosen_one}**. It was added to inventory",
            )
        else:
            e = discord.Embed(
                title=f"{ctx.message.author.name} went chopping",
                description=f"{ctx.message.author.name} you __cannot__ chop here! There are no trees here. Do `{prefix}loc`",
            )
            
        await ctx.send(embed=e)

            
    @commands.cooldown(1, 300)
    @commands.command(pass_context=True)
    async def forage(self,ctx):
        """Search trees and grass to find edibles"""
        user = str(ctx.message.author.id)

        with open('data/items.json') as f:
            items = json.load(f)

        #get all edibles
        edibles = []
        for item in items:
            if items[item]['meta']['type'] == 'food':
                edibles.append(str(item))

        #modifiers, amounts, and items
        skill_factor = int(assist.getdata(user,'reaper',"0"))
        the_chosen_one = random.choice(edibles)
        the_chosen_amount = int(random.randint(1,5) * (1+ skill_factor/3))
        assist.addinventory(user,the_chosen_one,the_chosen_amount)
            
        #construct embeds
        await ctx.send(
            embed=discord.Embed(
                title=f"{ctx.message.author.name} went foraging",
                description=f"{ctx.message.author.name} found **{the_chosen_amount} {the_chosen_one}**. It was added to inventory",
            )
        )


def setup(client):
    client.add_cog(Items(client))