import discord
from datetime import datetime
from colorama import Fore
from discord.ext import commands

# TODO: Make json file to keep autobanned users that have yet to join the server. 
# TODO: Add slash commands like add, remove, and view.
# TODO: Make little jokes in in comments >^> 

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banned_users = [
            1176634937693196300,
            1213729778725822474,
            1067773806090924112,
            1047148713191157790,
            1029111707924168715,
            1010619449885335666,
            1010619449885335666,
            1001920601377738882,
            824378839068835850,
            840293601011302410
        ]
    
    @commands.Cog.listener()
    async def on_ready(self):
        current = datetime.now()
        TimeStamp = current.strftime('%H:%M:%S')
        print(f"{TimeStamp} - {Fore.GREEN}[ OK ]{Fore.RESET} Loaded bancog.py!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.id in self.banned_users:
            try:
                await member.send("You have been banned from this server by SootBot.\nThis may because you were reported for raiding Wilbur support servers or Shubble support servers.\nIf you think this ban was false please message [@WaterMeloDev](https://x.com/WaterMeloDev) on Twitter to get your user ID removed from BanCog.")
                await member.ban(reason="Banned by SootBot upon joining.")
            except discord.Forbidden:
                await member.ban(reason="Banned by SootBot upon joining.")

async def setup(client):
    try:
        await client.add_cog(BanCog(client))
    except Exception as e:
        print(f"{Fore.RED}Error adding Logs Cog: {e}{Fore.RESET}")
