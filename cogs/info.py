import discord
from discord.ext import commands
from discord import app_commands
from colorama import Fore
from datetime import datetime

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        current = datetime.now()
        TimeStamp = current.strftime('%H:%M:%S')
        print(f"{TimeStamp} - {Fore.GREEN}[ OK ]{Fore.RESET} Loaded info.py!")

    @app_commands.command(name="modhelp", description="Show a list of mod commands.")
    async def modhelp_cmd(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Mod Discord Bot Commands",
            description="Here are some useful commands for mods:",
            color=0x27ae60,
        )

        embed.add_field(name="📜 /modhelp", value="Show this list of commands.", inline=False)
        embed.add_field(name="🚧 /ban", value="Bans a member.", inline=True)
        embed.add_field(name="🚧 /kick", value="Kicks a member.", inline=True)
        embed.add_field(name="🚧 /setup", value="Set up logs.", inline=True)
        embed.add_field(name="🚧 /warn", value="Warn a member.", inline=True)
        embed.add_field(name="🚧 /delwarn", value="Delete a warning.", inline=True)
        embed.add_field(name="🚧 /warnings", value="View a member's warnings.", inline=True)
        embed.add_field(name="🚧 /cwarn", value="Clear all warnings of a member.", inline=True)
        embed.add_field(name="🚧 /timeout", value="Timeout a member.", inline=True)
        embed.add_field(name="🚧 /lock", value="Lock a channel.", inline=True)
        embed.add_field(name="🚧 /unlock", value="Unlock a channel.", inline=True)
        embed.add_field(name="🚧 /nuke", value="Nuke a channel.", inline=True)
        embed.add_field(name="🚧 /unban", value="Unban a member.", inline=True)
        embed.add_field(name="🚧 /tempban", value="Temporarily ban a member.", inline=True)

        # Send the embed as a response
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="help", description="Show a list of user commands")
    async def help_cmd(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="User Discord Bot Commands",
            description="Here are some commands tailored for users:",
            color=0xff5733,
        )

        embed.add_field(name="📜 /help", value="Show this list of commands.", inline=False)
        embed.add_field(name="✅ /ship", value="Ship something.", inline=True)
        embed.add_field(name="🚧 /dev", value="<@1205617300875771984>", inline=True)
        embed.add_field(name="🔍 /whois", value="Get information about a user.", inline=True)
        embed.add_field(name="🖥️ /server", value="Get information about the server.", inline=True)
        embed.add_field(name="🎱 /8ball", value="Ask the magic 8-ball a question.", inline=True)

        # Send the embed as a response
        await interaction.response.send_message(embed=embed)


    """@app_commands.command(name="dev", description="A passionate Discord bot developer")
    async def developer(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Melo's Bot",
            description="A passionate Discord bot developed by WaterMeloDev",
            color=0x00ff00 
        )
        
        embed.add_field(name="Currently working on", value="`No Recent Project Found`", inline=False)
        embed.add_field(name="Ask me about", value="`Python, C#, JavaScript, Discord API, Discord ToS`", inline=False)
        embed.add_field(name="Contact", value="Email: `watermelodev@gmail.com`", inline=False)
        
        embed.add_field(name="Connect with me on Twitter", value="[@WaterMeloDev](https://twitter.com/watermelodev)", inline=False)
        
        languages_and_tools = [
            "Bash", "C#", "CSS3", "Django", "Flask", "HTML5", "JavaScript",
            "Linux", "MySQL", "Node.js", "Python", "Webpack"
        ]
        embed.add_field(name="Languages and Tools", value=", ".join(languages_and_tools), inline=False)
        
        embed.set_thumbnail(url="")
        
        await interaction.response.send_message(embed=embed)"""

async def setup(bot):
    await bot.add_cog(Info(bot))
