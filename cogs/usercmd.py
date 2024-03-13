import discord
import random
import io
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from colorama import Fore

# List of 8-ball responses
responses = ["It is certain.","It is decidedly so.","Without a doubt.","Yes - definitely.","You may rely on it.","As I see it, yes.","Most likely.","Outlook good.","Yes.","Signs point to yes.","Reply hazy, try again.","Ask again later.","Better not tell you now.","Cannot predict now.","Concentrate and ask again.","Don't count on it.","My reply is no.","My sources say no.","Outlook not so good.","Very doubtful."]

class userCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        current = datetime.now()
        TimeStamp = current.strftime('%H:%M:%S')
        print(f"{TimeStamp} - {Fore.GREEN}[ OK ]{Fore.RESET} Loaded usercmd.py!")

    @app_commands.command(name="8ball", description="Ask a question.")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        response = random.choice(responses)
        
        # Create an embed for the response
        embed = discord.Embed(
            title="🎱 8-Ball",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Question:", value=question, inline=False)
        embed.add_field(name="Answer:", value=response, inline=False)
        
        # Add an emoji to the embed
        emoji = '🎱'
        embed.set_footer(text=f"Asked by {interaction.user.display_name} {emoji}")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ship", description="Ship two members together.")
    async def ship_cmd(self, interaction: discord.Interaction, person1: discord.Member, person2: discord.Member):
        try:
            # Generate a ship name by combining the names
            ship_name = person1.name[:len(person1.name) // 2] + person2.name[len(person2.name) // 2:]

            # Generate a random percentage (0% to 100%)
            random_percentage = random.randint(0, 100)

            # Determine the emoji based on the random percentage
            if random_percentage <= 30:
                emoji = "💔"  # Less than or equal to 30%, use 💔
            elif random_percentage <= 70:
                emoji = "❤️‍🔥"  # Between 31% and 70%, use ❤️‍🔥
            else:
                emoji = "❤️"  # Greater than 70%, use ❤️

            # Create a text-based progress bar that fills to the random percentage
            filled_blocks = int(random_percentage / 10)
            progress = "█" * filled_blocks + "▒" * (10 - filled_blocks) + f" {random_percentage}%"

            # Create an embed
            embed = discord.Embed(
                title='🚢 Ship Generator',
                description=f'Ship name: {ship_name}',
                color=discord.Color.blue()
            )

            # Add the progress bar to the description field of the embed
            embed.description += f"\n**Compatibility:**\n```ansi\n{progress}\n```\n{emoji}"
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            # Log the error
            print(f"An error occurred: {e}")
            
            # Send an error message to Discord
            await interaction.response.send_message(f"**Error:** `{e}`")


    @app_commands.command(name="whois", description="Displays user infomation.")
    async def whois(self,interaction: discord.Interaction, member: discord.Member):
        if member:
            info_user = member
        elif member == None:
            info_user = interaction.author
        info_embed = discord.Embed(color=0xFD7720)
        info_embed.set_thumbnail(url=f"{info_user.avatar.url}")
        info_embed.add_field(name="🔴Member:",value=f"{info_user.mention}",inline=False)
        info_embed.add_field(name="⭐Member name:",value=f"{info_user}",inline=False)
        info_embed.add_field(name="💬Nickname:",value=f"{info_user.nick}",inline=False)
        info_embed.add_field(name="📆Joined on:",value=info_user.joined_at.strftime("%b %d %Y"))
        info_embed.add_field(name='📆Created on:',value=info_user.created_at.strftime("%b %d %Y"),inline=False)
        info_embed.add_field(name="🆔Member ID:",value=f"{info_user.id}",inline=False)
        await interaction.response.send_message(embed=info_embed, ephemeral=False, delete_after = 30)

    @app_commands.command(name="server", description="Displays server infomation.")
    async def server(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"{interaction.guild.name} Info",description="Information of this Server", color=0xFD7720)
        embed.add_field(name='🆔Server ID', value=f"{interaction.guild.id}", inline=False)
        embed.add_field(name='📆Created on',value=interaction.guild.created_at.strftime("%b %d %Y"),inline=False)
        embed.add_field(name='👑Owner',value=f"{interaction.guild.owner.mention}",inline=False)
        embed.add_field(name='👥Members',value=f'{interaction.guild.member_count} Members',inline=False)
        embed.add_field(name='💬Channels',value=f'{len(interaction.guild.text_channels)} Text | {len(interaction.guild.voice_channels)} Voice',inline=False)
        embed.set_thumbnail(url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed, ephemeral=False, delete_after = 30)

async def setup(bot):
    await bot.add_cog(userCmds(bot))