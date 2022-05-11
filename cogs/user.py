import discord
import assist, os, random, json, asyncio
from discord.ext import commands

prefix = os.environ.get("PREFIX") 

class User(commands.Cog):
    """Commands related to Players and Stuff"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot:
            return

        if message.content.startswith('say'):
            msg = message.content.replace('say','')
            user = str(message.author.id)
            name = assist.getdata(user,'name',message.author.name)
            try: img_url =assist.getdata(user,'img',str(message.author.avatar_url))
            except: pass
            one_liner = assist.getdata(user,'footer',f"You can customize it with {prefix}profile")

            

            e = discord.Embed(title=f"{name} says",description=msg)
            e.set_thumbnail(url=img_url)
            e.set_footer(text=one_liner)
            attachments = message.attachments
            for atc in attachments:
                e.add_field(name ="Attachment:",value = str(atc.proxy_url))
            await message.channel.send(embed=e)


            try: await message.delete()
            except  discord.errors.Forbidden:
                await asyncio.sleep(10)
                await  message.channel.send("It would be nice if you give me `Permission to delete messages`, so I can delete the root message😉")
            


        user = str(message.author.id)
        curr_lvl = int(assist.getdata(user,"lvl","0"))
        curr_xp = int(assist.getdata(user,"xp","0"))
        curr_sp = int(assist.getdata(user,"skillpoints","0"))

        curr_xp += random.randint(0,10)

        req_xp,_has_lvl_up = assist.check_lvlup(curr_lvl,curr_xp)
        if _has_lvl_up:
            curr_lvl +=1
            curr_sp += 1
            curr_xp = 0 +random.randint(0,10)
            req_xp,_ = assist.check_lvlup(curr_lvl,curr_xp)
            e = discord.Embed(title="Level Up!",description="You just leveled up!")
            e.add_field(name="Current Level"  , value=f"{curr_lvl}" )
            e.add_field(name="Xp for Next Level" , value=f"{req_xp}")
            e.set_footer(text=f"You gained 1 skill point ({prefix}skills)")
            await message.channel.send(embed=e)
        
        assist.savedata(user,"lvl",curr_lvl)
        assist.savedata(user,"xp",curr_xp)
        assist.savedata(user,"skillpoints",curr_sp)
        
    @commands.command(pass_context=True,aliases=["stats"])
    async def statistics(self,ctx,mention:discord.User=None):
        """Get details of Any Player"""
        if mention == None:
            user = str(ctx.message.author.id)
            mention = ctx.message.author
        else:
            user = str(mention.id)

        #load data to temp variables
        _lvl = assist.getdata(user, "lvl", "0")
        _coins = assist.getdata(user, "coins", "0")
        _loc = assist.getdata(user, "loc", "House")
        _xp = assist.getdata(user, "xp", "0")
        _skillpoints = assist.getdata(user, "skillpoints", "0")
        _helmet = assist.getdata(user, "helmet", "None")
        _chestplate = assist.getdata(user, "chestplate", "None")
        _boots = assist.getdata(user, "boots", "None")
        _axe = assist.getdata(user, "axe", "None")
        _pick = assist.getdata(user, "pickaxe", "None")

        #create and display embed
        e = discord.Embed(title=f"{mention.name}'s Stats'")
        e.add_field(name="Level", value=_lvl)
        e.add_field(name="Coins", value=_coins)
        e.add_field(name="Location", value=_loc)
        e.add_field(name="XP", value =_xp)
        e.add_field(name="Skill Points", value =_skillpoints)
        e.add_field(name="Helmet", value =_helmet)
        e.add_field(name="Chestplate", value =_chestplate)
        e.add_field(name="Boots", value =_boots)
        e.add_field(name="Axe", value =_axe)
        e.add_field(name="Pickaxe", value =_pick)

        await ctx.send(embed = e)


    @commands.command(pass_context=True,aliases=["skill"])
    async def skills(self,ctx,mention:discord.User=None):
        """Get Skills of Any Player"""
        if mention == None:
            user = str(ctx.message.author.id)
            mention = ctx.message.author
        else:
            user = str(mention.id)

        #load data to temp variables
        _skillpoints = assist.getdata(user, "skillpoints", "0")

        with open("data/skills.json",'r') as f:
            data = json.load(f)
        skills = {}
        for skill in data:
            skills[skill] = assist.getdata(user, skill, "0")


        #create and display embed
        e = discord.Embed(title=f"{mention.name}'s Skills'")
        e.add_field(name="Unused Skill Points", value=_skillpoints)
        for skill in skills:
            e.add_field(name=skill.title(), value=skills[skill])

        e.set_footer(text="use *assign* command to assign unused points ")
        await ctx.send(embed = e)

    @commands.command(pass_context=True)
    async def assign(self,ctx,*,skill):
        """Assign Your unspent skill points, Assign one at a time"""
        user = str(ctx.message.author.id)

        #autocomplete skill
        skill = assist.auto_complete(skill,"skills")
        if not skill:
            await ctx.send(f"Aoy! It seems u messed up, do `{prefix}help assign`")
            return

        user_skills = int(assist.getdata(user,'skillpoints',"0"))

        if user_skills <= 0:
            await ctx.send("You do not have enough skill points")
        else:
            user_skills -= 1
            if user_skills < 0:
                user_skills ==0
            assist.savedata(user,'skillpoints',user_skills)

            skill_points_of_req_skill = int(assist.getdata(user,skill,'0'))

            skill_points_of_req_skill +=1
            assist.savedata(user,skill,skill_points_of_req_skill)

            curr_skill_points = assist.getdata(user,"skillpoints","0")
            e = discord.Embed(title="Skill Point assigned")
            e.add_field(name="Enhanced Skill",value=skill)
            e.add_field(name="Remaining Skill Point",value=curr_skill_points)
            e.set_footer(text=f"{skill} enhanced by one")
            await ctx.send(embed=e)

    @commands.command(pass_context=True)
    async def equip(self,ctx,*,item):
        """Using this command you can equip a new tool, or a peice of armour, old item returns to your inventory"""
        user = str(ctx.message.author.id)
        item = assist.auto_complete(item,'items')
        inv = str(assist.getdata(user,'inv',{}))

        e = discord.Embed(title="Equip",description="Equip Gear and Tools")
        if item in inv:
            with open('data/items.json','r') as f:
                _item = json.load(f)[item]
            with open('data/players.json','r') as f:
                _player = json.load(f)[user]

            if _item['meta']['type']in ['axe','pickaxe',"helmet","chestplate","boots"]:
                _tool = _item['meta']['type']
                e.add_field(name='Type:',value=_tool)

            if int(_player['strenght']) < int(_item['meta']['strenght']):
                await ctx.send(embed=discord.Embed(
                    title="Cannot Equip Item",
                    description=f"You are not sufficiently strong to hold the item `{prefix}skills`"
                ))
            
            e.add_field(name="Previous Item:",value=_player[_tool])
            if _player[_tool] != "None":
                assist.addinventory(user,_player[_tool],1)
            
            assist.savedata(user,_tool,item)
            assist.addinventory(user,item,-1)
            e.add_field(name="Current Item:",value=item)

            e.set_footer(text="The Previous item has been transfered into your inventory")

            await ctx.send(embed=e)
        else:
            await ctx.send(
                embed=discord.Emned(
                    title=f"Couldn't find item",
                    description=f"Please check if you have that item."
                )
            )

    @commands.command(pass_context=True)
    async def profile(self,ctx,name,img_url,one_liner):
        user = str(ctx.message.author.id)
        assist.savedata(user,'name',name)
        if img_url.lower() == "none":
            img_url = ctx.message.author.avatar_url
        assist.savedata(user,'img',str(img_url))
        assist.savedata(user,'footer',one_liner)

        e = discord.Embed(title=f"{name} said",description="write `say Hello World!` it will be modified to a embed.")
        e.set_thumbnail(url=img_url)
        e.set_footer(text=one_liner)

        await ctx.send(embed=e)


    

    

def setup(client):
    client.add_cog(User(client))