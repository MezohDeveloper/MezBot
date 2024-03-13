import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from colorama import Fore
import json
from datetime import datetime

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        current = datetime.now()
        TimeStamp = current.strftime('%H:%M:%S')
        print(f"{TimeStamp} - {Fore.GREEN}[ OK ]{Fore.RESET} Loaded setup.py!")

    # setup command
    @app_commands.command(name="setup", description="setup logs")
    @app_commands.checks.has_permissions(ban_members=True)
    async def setup(self, interaction: discord.Interaction, user_logs: discord.TextChannel, mod_logs: discord.TextChannel, bot_update_logs: discord.TextChannel):
        guild_id = interaction.guild.id
        config = {}

        # Load existing config
        try:
            with open("src/data/config.json", "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            pass  # If the file doesn't exist yet, an empty config will be created

        if guild_id not in config:
            config[guild_id] = {}

        guild_config = config[guild_id]

        # Store the channels in the config
        guild_config["user_logs_channel"] = user_logs.id
        guild_config["mod_logs_channel"] = mod_logs.id
        guild_config["bot_update_channel"] = bot_update_logs.id

        # Save the configuration to config.json
        with open("src/data/config.json", "w") as f:
            json.dump(config, f)

        embed = discord.Embed(title="Setup Complete", description="Channels for logging configured successfully!", color=0x5865F2)
        embed.add_field(name="User Logs Channel", value=user_logs.mention, inline=False)
        embed.add_field(name="Mod Logs Channel", value=mod_logs.mention, inline=False)
        embed.add_field(name="Bot Update Logs Channel", value=bot_update_logs.mention, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=False)
        
    

async def setup(bot):
    await bot.add_cog(Config(bot))
