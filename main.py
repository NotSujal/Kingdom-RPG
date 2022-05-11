import discord, os
from keep_alive import keep_alive
from discord.ext import commands
import  asyncio, json


prefix = os.environ.get("PREFIX") 

client = commands.Bot(
	command_prefix=prefix,
	case_insensitive=True,
    help_command = None
)


#me
client.author_id = os.environ.get("ME") 

with open('data/players.json','r') as f:
    count = len(json.load(f).keys())

async def status_task():
    while True:
        await client.change_presence(
            activity=discord.Game(name=f"with {str(count)} players!", type=1)
            )
        await asyncio.sleep(30)
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=f" {str(len(client.guilds))} servers!")
            )
        await asyncio.sleep(30)
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.listening, name=f" {prefix}help")
            )
        await asyncio.sleep(30)
        await client.change_presence(
            activity=discord.Streaming(name="live!", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            )
        await asyncio.sleep(30)

@client.event 
async def on_ready():
    print(f"Logging in as {client.user}")
    client.loop.create_task(status_task())



#Better Help Command
class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.green(), description='')
        for page in self.paginator.pages:
            e.description += page
        e.set_footer(text=f" KingdomRPG| v_0.5")
        await destination.send(embed=e)
client.help_command = MyHelpCommand()


# @client.command()
# @commands.cooldown(1, 30)
async def enable(ctx, extention):
    """
    Activates the given module for use of it
    """
    if str(ctx.message.author.id) == str(client.author_id):

        client.load_extension(f"cogs.{extention}")
        await ctx.send(
            f"```cogs.{extention} is loaded and is ready to be used```")
    else:
        await ctx.send(
            "```You are not the owner of the bot!, Sorry I can't perform the task without owners permission```"
        )


# @client.command()
# @commands.cooldown(1, 30)
async def disable(ctx, extention):
    """
    Commands of the disabled module can't be used
    """
    if str(ctx.message.author.id)  == str(client.author_id):

        client.unload_extension(f"cogs.{extention}")
        await ctx.send(
            f"```cogs.{extention} is unloaded. If you want to use it load it in.```"
        )
    else:
        await ctx.send(
            "```You are not the owner of the bot!, Sorry I can't perform the task without owners permission```"
        )


# @client.command(aliases=["rl"])
# @commands.cooldown(1, 30)
async def reload(ctx, extention):
    """
    Reloading a module will update the module to the recent version
    """
    if "All" in extention:
        for filename in os.listdir('./cogs'):
            if filename.endswith(".py"):
                client.unload_extension(f"cogs.{filename[:-3]}")
                client.load_extension(f"cogs.{filename[:-3]}")
                await ctx.send(f"```cogs.{filename[:-3]} is reloaded.```")
        await ctx.send("```Reloading Completed!```")
        return

    client.unload_extension(f"cogs.{extention}")
    client.load_extension(f"cogs.{extention}")
    await ctx.send(f"```cogs.{extention} is reloaded.```")


for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


# @client.event
async def on_command_error(ctx, error):
    await ctx.send(f"{str(error)}")

keep_alive()
token = os.environ.get("TOKEN") 
client.run(token)