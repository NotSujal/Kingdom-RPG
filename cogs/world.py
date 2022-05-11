import discord
import assist, json, os
from discord.ext import commands

prefix = os.environ.get("PREFIX")

class World(commands.Cog):
    """Commands related to Map and Travelling"""
    def __init__(self, client):
        self.client = client
        
    # main commands
    @commands.command(pass_context=True)
    async def travel(self,ctx,*,location:str=None):
        """Travel to locations to get different types of wood"""


        #load required data
        with open("data/locations.json",'r') as f:
            places = json.load(f)

        user = ctx.message.author.id

        # if location is not provided, display all locations
        if location is None:
            await ctx.send("Need to provide a location to travel")
            return
        
        # get the location and check the location
        location = assist.auto_complete(str(location))

        if not location:
            await ctx.send(f"Aoy! It seems u messed up, do `{prefix}map`")

        #calculate the cost of the travel
        curr_loc = assist.getdata(user, "loc","Village Holz")
        cost = abs(int(places[location]["cost"]) - int(places[curr_loc]["cost"]))

        #create Embed
        e = discord.Embed(title="Travel")
        e.add_field(name="From:", value=curr_loc)
        e.add_field(name="To:", value=location)
        e.add_field(name="Cost:", value=cost)

        # compare level of player 
        player_lvl = assist.getdata(user, "lvl", "0")
        if int(player_lvl) < int(places[location]['req_lvl']):
            e.add_field(name="Cannot able to Travel:", value="Not Enough Levels")
            await ctx.send(embed=e)
            return

        #deduce cost
        curr_money = assist.getdata(user,"coins","0")
        curr_money = int(curr_money)
        if curr_money >= cost:
            curr_money -= cost
            assist.savedata(user, 'loc',location)
            assist.savedata(user, 'coins',curr_money)
        else:
             e.add_field(name="Cannot able to Travel:", value="Not Enough Money")

        await ctx.send(embed=e)

    @commands.command(pass_context=True)
    async def map(self,ctx,*,filter=None):
        """Get details of Any Location"""

        user= str(ctx.message.author.id)
        try:
            page = int(filter)
            location = None
        except:
            location = filter
            page = 1

        
        #load required data
        with open("data/locations.json",'r') as f:
            places = json.load(f)
        with open("data/players.json",'r') as f:
            player = json.load(f)[user]

        # if location is not provided, display all locations
        if location is None:
            e = discord.Embed(title="Provide a location to get details")
            string = ""
            starting_no = (page -1) * 10
            i = 1
            for word in places.keys():
                
                if i >= starting_no and i <= starting_no + 10:
                    string += f"{i}. {word} \n"
                else:
                    i +=1
                    continue
                i +=1
            if string == "":
                string = "Not enough items for this page"
            e.add_field(name=f"Available Locations: page{page}",value = string)
            e.set_footer(text="use map command to get details of a region")
            
            file = discord.File("images/world_map.jpg", filename="image.png")
            e.set_image(url="attachment://image.png")

            await ctx.send(file=file,embed=e)
            return
        
        # get the location and check the location
        location = assist.auto_complete(str(location))
            
        if not location:
            await ctx.send(f"Aoy! It seems u messed up, do `{prefix}map`")

        #create Embed
        e = discord.Embed(title="Location Details:")
        temp = places[location]
        e.add_field(name="Name:", value=location)
        e.add_field(name="Description:", value=temp['desc'],inline=False)
        e.add_field(name="Enemies :", value=temp['enemy'],inline=False)
        e.add_field(name="Lumber :", value=temp['lumber'],inline=False)
        e.add_field(name="Ores :", value=temp['ore'],inline=False)

        _my_loc_cost = places[player['loc']]['cost']
        _that_loc_cost = temp['cost']
        _cost = abs(int(_my_loc_cost) - int(_that_loc_cost))

        e.add_field(name="Travel Cost:", value=_cost,inline=False)
        e.add_field(name="Required Level:", value=temp['req_lvl'],inline=False)

        file = discord.File(temp['img'], filename="image.png")
        e.set_image(url="attachment://image.png")
        await ctx.send(file=file,embed=e)

    @commands.command(pass_context=True,aliases=["loc"])
    async def location(self,ctx,mention:discord.User=None):
        """Get Current location of a Player"""
        if mention == None:
            user = str(ctx.message.author.id)
            mention = ctx.message.author
        else:
            user = str(mention.id)

        loc = assist.getdata(user,"loc","House")
        with open("data/locations.json",'r') as f:
            places = json.load(f)
        with open("data/players.json",'r') as f:
            player = json.load(f)[user]

        e = discord.Embed(title=f"{mention.name}'s Location'",description="Information is as follows;")
        temp = places[loc]
        e.add_field(name="Name:", value=loc)
        e.add_field(name="Description:", value=temp['desc'],inline=False)
        e.add_field(name="Enemies :", value=temp['enemy'],inline=False)
        e.add_field(name="Lumber :", value=temp['lumber'],inline=False)
        e.add_field(name="Ores :", value=temp['ore'],inline=False)

        _my_loc_cost = places[player['loc']]['cost']
        _that_loc_cost = temp['cost']
        _cost = abs(int(_my_loc_cost) - int(_that_loc_cost))

        e.add_field(name="Travel Cost:", value=_cost,inline=False)
        e.add_field(name="Required Level:", value=temp['req_lvl'],inline=False)

        file = discord.File(temp['img'], filename="image.png")
        e.set_image(url="attachment://image.png")

        await ctx.send(file=file,embed=e)


     

def setup(client):
    client.add_cog(World(client))