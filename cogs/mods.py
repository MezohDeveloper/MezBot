import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
from datetime import timedelta
import asyncio
from datetime import datetime

locked_channels = []

class modCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        current = datetime.now()
        TimeStamp = current.strftime('%H:%M:%S')
        print(f"{TimeStamp} - {Fore.GREEN}[ OK ]{Fore.RESET} Loaded mods.py!")

    @app_commands.command(name="lock", description="locks a mention channel")
    @app_commands.checks.has_permissions(ban_members=True)
    async def lock(self,interaction: discord.Interaction, channel: discord.TextChannel = None):
        if not channel:
            channel = interaction.channel

        if channel.id in locked_channels:
            await interaction.response.send_message("This channel is already locked.", delete_after = 3)
        else:
            await interaction.response.send_message("This channel is now locked.")
            locked_channels.append(channel.id)

    @app_commands.command(name="unlock", description="unlocks a mention channel")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unlock(self,interaction: discord.Interaction, channel: discord.TextChannel = None):
        if not channel:
            channel = interaction.channel

        if channel.id in locked_channels:
            locked_channels.remove(channel.id)
            await interaction.response.send_message("This channel is now unlocked.")
        else:
            await interaction.response.send_message("This channel was not locked.", delete_after = 3)

    @app_commands.command(name='timeout', description='times out a member')
    @app_commands.checks.has_permissions(kick_members=True)
    async def timeout(self,interaction: discord.Interaction, user: discord.User, *, reason: str, minutes: int):
        embed = discord.Embed(title="Success!", description=f"{user} was timed out!", color=0xFD7720) 
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after = 3)
        await user.timeout(timedelta(minutes = minutes), reason = reason)

    @app_commands.command(name='unban', description="Unbans the user's ID") # unban slash command
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self,interaction: discord.Interaction, userid: discord.User):
        if userid == None:
            await interaction.response.send_message("Please specify a member\nEx: `949097449740435586`", ephemeral=True, delete_after = 3)
        else:
            guild = interaction.guild
            await guild.unban(user=userid)
            embed = discord.Embed(title="Success!", description=f"{userid} was unbanned!", color=0xFD7720) 
            await interaction.response.send_message(embed=embed, ephemeral=True, delete_after = 3)

    @app_commands.command(name='softban', description='Bans the selected user') # softban slash command
    @app_commands.checks.has_permissions(ban_members=True)
    async def softban(self,interaction: discord.Interaction, userid: discord.User, reason:str):
        guild = interaction.guild
        embed = discord.Embed(title=f"{userid} was softbanned for {reason}", color=0xFD7720)
        await userid.ban(reason=reason)
        await guild.unban(user=userid)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after = 3)

    @app_commands.command(name='ban', description='Bans the selected user') # ban slash command
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self,interaction: discord.Interaction, member: discord.User, reason:str):
        embed = discord.Embed(title=f"{member} was banned for {reason}", color=0xFD7720)
        await member.ban(reason=reason)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after = 3)

    @app_commands.command(name='kick', description='Kicks the selected user') # kick slash command
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self,interaction: discord.Interaction, member: discord.User, reason:str):
        embed = discord.Embed(title=f"{member} was kicked for {reason}", color=0xFD7720)
        await member.kick(reason=reason)
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after = 3)

    @app_commands.command(name='clear', description='Clears messages') # clear slash command
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self,interaction: discord.Interaction, amount: int):
        embed = discord.Embed(title=f"Purged {amount} messages", color=0xFD7720)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await interaction.channel.purge(limit=amount + 1)

    @app_commands.command(name='nuke', description='Nukes a selected channel') # nuke slash command
    @app_commands.checks.has_permissions(ban_members=True)
    async def nuke(self,interaction: discord.Interaction, channel: discord.TextChannel = None):
            await interaction.response.send_message(f'Nuking {channel}', ephemeral=True)
            channel = discord.utils.get(interaction.guild.channels, name=channel.name)
            if channel is not None:
                message = await channel.send("THIS CHANNEL IS BEING NUKED IN 5")
                await asyncio.sleep(1)
                await message.edit(content='THIS CHANNEL IS BEING NUKED IN 4')
                await asyncio.sleep(1)
                await message.edit(content='THIS CHANNEL IS BEING NUKED IN 3')
                await asyncio.sleep(1)
                await message.edit(content='THIS CHANNEL IS BEING NUKED IN 2')
                await asyncio.sleep(1)
                await message.edit(content='THIS CHANNEL IS BEING NUKED IN 1')
                await asyncio.sleep(1)
                await message.edit(content='THIS CHANNEL IS BEING NUKED IN 0')
                new_channel = await channel.clone(reason="Has been Nuked!")
                await channel.delete()
                await new_channel.send("Nuked the Channel sucessfully!", delete_after = 3)

            else:
                await interaction.response.send_message(f"No channel named {channel.name} was found!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(modCmds(bot))