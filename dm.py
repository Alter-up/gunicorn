import settings
import discord 
from discord.ext import commands
    
logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True


bot = commands.Bot(command_prefix=prefix, intents=intents)
    
    
@bot.event
async def on_member_join(member):
  embed = discord.Embed(title="Welcome to my server!", description=None, color = discord.Color.magenta())
  embed.add_field(name="To get started:", value="•Invite some friends!\n•Check out some of the channels and get engaged with the community!\n•Have fun!", inline=True)
  await member.send(embed=embed)


    @bot.command()
    async def ping(ctx):
        # await ctx.message.author.send("Hello")
        user = discord.utils.get(bot.guilds[0].members, nick="User2")
        if user:
            await user.send("Hello 2")
        
    bot.run(d4rJ2-ql9Zp92-GbdainnyPRrzdwhr6y, root_logger=True)

if __name__ == "__main__":
    run()
