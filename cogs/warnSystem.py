import discord
from discord.ext import commands
import sqlite3
from discord import app_commands
from colorama import Fore
from datetime import datetime

class warnSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        current = datetime.now()
        TimeStamp = current.strftime('%H:%M:%S')
        print(f"{TimeStamp} - {Fore.GREEN}[ OK ]{Fore.RESET} Loaded warnSystem.py!")
    
    @app_commands.command(name="warn", description="Warn a user")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        # Create a database connection specific to the guild
        conn = sqlite3.connect(f'src/data/warnings/warnings_{interaction.guild.id}.db')
        c = conn.cursor()

        # Check if the user has the necessary permissions to warn
        if interaction.user.guild_permissions.kick_members:
            # Create a table for warnings if it doesn't exist
            c.execute('''CREATE TABLE IF NOT EXISTS warnings (
                            user_id INTEGER,
                            moderator_id INTEGER,
                            reason TEXT
                         )''')
            
            # Insert the warning into the database
            c.execute("INSERT INTO warnings (user_id, moderator_id, reason) VALUES (?, ?, ?)",
                      (user.id, interaction.user.id, reason))
            conn.commit()
            await interaction.response.send_message(f"{user.mention} has been warned for: {reason}")
        else:
            await interaction.response.send_message("You do not have permission to warn users.")

    @app_commands.command(name="delwarn", description="Deletes a warning")
    @app_commands.checks.has_permissions(ban_members=True)
    async def delwarn(self, interaction: discord.Interaction, user: discord.Member, warning_id: int):
        # Create a database connection specific to the guild
        conn = sqlite3.connect(f'src/data/warnings/warnings_{interaction.guild.id}.db')
        c = conn.cursor()

        # Check if the user has the necessary permissions to delete warnings
        if interaction.user.guild_permissions.kick_members:
            # Delete the specified warning from the database
            c.execute("DELETE FROM warnings WHERE user_id = ? AND rowid = ?", (user.id, warning_id))
            conn.commit()
            await interaction.response.send_message(f"Warning {warning_id} for {user.mention} has been deleted.")
        else:
            await interaction.response.send_message("You do not have permission to delete warnings.")

    @app_commands.command(name="cwarns", description="Clear warnings from a user")
    @app_commands.checks.has_permissions(ban_members=True)
    async def cwarns(self, interaction: discord.Interaction, user: discord.Member):
        # Create a database connection specific to the guild
        conn = sqlite3.connect(f'src/data/warnings/warnings_{interaction.guild.id}.db')
        c = conn.cursor()

        # Check if the user has the necessary permissions to clear warnings
        if interaction.user.guild_permissions.kick_members:
            # Delete all warnings for the specified user from the database
            c.execute("DELETE FROM warnings WHERE user_id = ?", (user.id,))
            conn.commit()
            await interaction.response.send_message(f"All warnings for {user.mention} have been cleared.")
        else:
            await interaction.response.send_message("You do not have permission to clear warnings.")

    
    @app_commands.command(name="warnings", description="List out the warnings for a user.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warnings(self, interaction: discord.Interaction, user: discord.Member):
        # Create a database connection specific to the guild
        conn = sqlite3.connect(f'src/data/warnings/warnings_{interaction.guild.id}.db')
        c = conn.cursor()

        # Retrieve the user's warnings from the database
        c.execute("SELECT rowid, reason FROM warnings WHERE user_id = ?", (user.id,))
        warning_data = c.fetchall()
        if interaction.user.guild_permissions.kick_members:
            if not warning_data:
                await interaction.response.send_message(f"{user.mention} has no warnings.")
            else:
                # Create an embed to display the warnings
                embed = discord.Embed(title=f"⚠️ Warnings for {user}", color=discord.Color.red())
                for row in warning_data:
                    embed.add_field(name=f"Warning {row[0]}", value=row[1], inline=False)
                
                await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("You do not have permission to look at warnings.")


async def setup(bot):
    await bot.add_cog(warnSystem(bot))