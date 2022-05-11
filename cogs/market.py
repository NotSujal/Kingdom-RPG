import discord
import assist, os, json
from discord.ext import commands

prefix = os.environ.get("PREFIX")

class Market(commands.Cog):
    """A place to sell your stuff and buy more stuff"""
    def __init__(self, client):
        with open('data/market/shop.json')as f:
            shop = json.load(f)
        with open('data/items.json')as f:
            items = json.load(f)

        for item in items:
            if items[item]['meta']['type'] == 'food':
                shop[item] = 100 + int(items[item]['meta']['heal']) * 33
            elif items[item]['meta']['type'] == 'axe':
                shop[item] = 100 * int(items[item]['meta']['qfac']) * int(items[item]['meta']['strenght'])
            elif items[item]['meta']['type'] == 'pickaxe':
                shop[item] = 100 * int(items[item]['meta']['qfac']) * int(items[item]['meta']['strenght'])
            elif items[item]['meta']['type'] == 'axe':
                shop[item] = 100 * int(items[item]['meta']['qfac']) * int(items[item]['meta']['strenght'])

            elif items[item]['meta']['type'] == 'ore':
                shop[item] = 113 * int(items[item]['meta']['rare'])
            

        with open('data/market/shop.json','w')as f:
            json.dump(shop,f,indent=4)
        self.client = client

    @commands.command()
    async def shop(self,ctx,page:int=1):
        """This is a trusty shop. Made by developer for for you. Buy and Sell Stuff here!"""
        e = discord.Embed(title="Provide a location to get details")
        string = ""
        starting_no = (page -1) * 10
        i = 1
        with open('data/market/shop.json') as f:
            items = json.load(f)
        for word in items.keys():
            
            if i >= starting_no and i <= starting_no + 10:
                string += f"{i}. {word} `${items[word]}`\n"
            else:
                i +=1
                continue
            i +=1
        if string == "":
            string = "Not enough items for this page"
        e.add_field(name=f"General Market: page{page}",value = string)
        e.set_footer(text=f"{prefix}buy command to buy an item from this shop")
        await ctx.send(embed=e)
    
    @commands.command()
    async def buy(self,ctx,_item:str,amount:int=1):
        """Buy items from the General Shop"""

        user = str(ctx.message.author.id)
        user_money = int(assist.getdata(user,'coins','0'))

        item = assist.auto_complete(_item,'market/shop')
        if not item:
            await ctx.send(
                embed=discord.Embed(
                    title=f"Could not find {item} item",
                    description=f"Either {_item} is spelled wrong or we are not selling them in the general shop. do `{prefix}shop` or `{prefix}market`"
                )
            )
            return
        
        with open('data/market/shop.json')as f:
            price = json.load(f)[item]
        
        if user_money < price * amount:
            await ctx.send(
                embed = discord.Embed(
                    title="Not enough Money",
                    description = f"You are short by {price * amount - user_money}, try selling items."
                )
            )
            return

        assist.addcoins(user,-(price*amount))
        assist.addinventory(user,item,amount)

        e = discord.Embed(
            title="Invoice",
            description="Invoice of your purchases"
        )
        e.add_field(name="Item",value=item.title())
        e.add_field(name="Amount",value=amount)
        e.add_field(name="Coins per piece",value=price)
        e.add_field(name="Total",value= -(price*amount))
        
        await ctx.send(embed=e)

    @commands.command()
    async def sell(self,ctx,_item:str,amount):
        """Sell items to get money"""
        user = str(ctx.message.author.id)
        with open('data/players.json') as f:
            inv = json.load(f)[user]['inv']

        item = assist.auto_complete(_item,"items")
        print(item,inv)
        if item in inv:
            avail_item = int(inv[item])
            if amount == "all":
                amount = avail_item

            amount = int(amount)

            if amount > avail_item:
                await ctx.send(
                    embed=discord.Embed(
                        title="Not enough items",
                        description="You dont have that many items to sell"
                    )
                )
                return
            else:
                with open('data/market/shop.json') as f:
                    shop = json.load(f)
                if item not in shop:
                    await ctx.send(
                    embed=discord.Embed(
                        title="We dont buy this item",
                        description=f"No vendor buys {item} here check the player shop `{prefix}market`"
                        )
                    )
                    return

                price = int(0.3 * int(shop[item]))

                assist.addinventory(user,item,-amount)
                assist.addcoins(user,price*amount)

                e =discord.Embed(
                    title = "Invoice",
                    description="You sold items!"
                )
                e.add_field(name="Item",value=item)
                e.add_field(name="Amount",value=amount)
                e.add_field(name="Price per piece",value=price)
                e.add_field(name="Total",value=price * amount)
                await ctx.send(embed=e)
        else:
            await ctx.send(
                embed=discord.Embed(
                        title="Couldn't find",
                        description=f"We couldn't find the {_item} in your inventory"
                    )
                )


def setup(client):
    client.add_cog(Market(client))