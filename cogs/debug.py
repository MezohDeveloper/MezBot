import discord
from discord.ext import commands
from discord import app_commands, Interaction 
from colorama import Fore
from datetime import datetime

# TODO: Add some debug commands to test speed and data loud time.
# TODO: Add more comments to code.

class DEBUG(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.add_listener(self.on_guild_join, name="on_guild_join")
        self.client.add_listener(self.on_guild_remove, name="on_guild_remove")
        client.tree.on_error = self.global_app_command_error

    @commands.Cog.listener()
    async def on_ready(self):
        current = datetime.now()
        TimeStamp = current.strftime('%H:%M:%S')
        print(f"{TimeStamp} - {Fore.GREEN}[ OK ]{Fore.RESET} Loaded debug.py!")

        
    async def global_app_command_error(
        self,
        interaction: Interaction,
        error: app_commands.AppCommandError
    ):
        current = datetime.now()
        TimeStamp = current.strftime('%H:%M:%S')
        # disclaimer: this is an example implementation.
        print(f"{TimeStamp} {Fore.RED}[ FAILED ]{Fore.RESET} error:", str(error))


    async def on_guild_join(self, guild):
        # Log when the bot joins a server
        print(f"{Fore.GREEN}[ OK ]{Fore.RESET} Joined server: {guild.name} ({guild.id})")

    async def on_guild_remove(self, guild):
        # Log when the bot leaves a server
        print(f"{Fore.GREEN}[ OK ]{Fore.RESET} Left server: {guild.name} ({guild.id})")

async def setup(client):
    await client.add_cog(DEBUG(client))