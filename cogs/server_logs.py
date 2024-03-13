import discord
import json
import random
import re
from datetime import datetime
from colorama import Fore
from discord.ext import commands



class Logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_time(self):
        return datetime.now().strftime("%H:%M")

    @commands.Cog.listener()
    async def on_ready(self):
        current = datetime.now()
        TimeStamp = current.strftime('%H:%M:%S')
        print(f"{TimeStamp} - {Fore.GREEN}[ OK ]{Fore.RESET} Loaded server_logs.py!")

    async def get_config(self, guild):
        try:
            with open("src/data/config.json", "r") as f:
                config = json.load(f)
                return config.get(str(guild.id), {})
        except FileNotFoundError:
            return {}

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            config = await self.get_config(message.guild)
            User_Logs_ID = config.get("user_logs_channel")
            User_Logs = message.guild.get_channel(User_Logs_ID)

            if message.author.bot:
                return
            else:
                try:
                    embed = discord.Embed(
                        title=f"Message Log | {message.jump_url}",
                        description=f"{self.get_time()} - {message.author.name}: {message.content}",
                        color=0x5865F2
                    )
                    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar.url)
                    embed.add_field(name="Username", value=message.author.name, inline=True)
                    embed.add_field(name="User ID", value=message.author.id, inline=True)
                    embed.add_field(name="Nickname", value=message.author.nick, inline=True)
                    
                    await User_Logs.send(embed=embed)
                except Exception as e:
                    await User_Logs.send(e)
                    print(e)
        except Exception as e:
            print(f"on_message {Fore.RED}[ FAILED ]{Fore.RESET}: {e}")

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        try:
            guild = after.guild
            if guild is None:
                return 

            config = await self.get_config(guild)
            User_Logs_ID = config.get("user_logs_channel")
            User_Logs = guild.get_channel(User_Logs_ID)

            if before.avatar != after.avatar:
                embed = discord.Embed(
                    title="Avatar Update Log",
                    description=f"{self.get_time()} - {after.name}'s avatar has been updated",
                    color=0x9B51E0
                )
                embed.set_thumbnail(url=after.avatar.url)
                await User_Logs.send(embed=embed)
        except Exception as e:
            print(f"on_user_update {Fore.RED}[ FAILED ]{Fore.RESET}: {e}")


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            config = await self.get_config(after.guild)
            User_Logs_ID = config.get("user_logs_channel")
            User_Logs = after.guild.get_channel(User_Logs_ID)

            if after.author.bot:
                return
            else:
                try:
                    embed = discord.Embed(
                        title=f"Message Edit Log | {after.jump_url}",
                        description=f"{self.get_time()} - {after.author.name} edited a message",
                        color=0xF9A825
                    )
                    embed.add_field(name="User", value=after.author.mention, inline=True)
                    embed.add_field(name="Before", value=before.content, inline=False)
                    embed.add_field(name="After", value=after.content, inline=False)
                    await User_Logs.send(embed=embed)
                except Exception as e:
                    await User_Logs.send(e)
                    print(e)
        except Exception as e:
            print(f"on_message_edit {Fore.RED} [ FAILED ]: {e}{Fore.RESET}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            if message.author.bot:
                return

            config = await self.get_config(message.guild)
            User_Logs_ID = config.get("user_logs_channel")
            User_Logs = message.guild.get_channel(User_Logs_ID)

            embed = discord.Embed(
                title="Message Deletion Log",
                description=f"{self.get_time()} - {message.author.name} deleted a message",
                color=0xE53935
            )
            embed.add_field(name="User", value=message.author.mention, inline=True)
            embed.add_field(name="Content", value=message.content, inline=False)
            await User_Logs.send(embed=embed)
        except Exception as e:
            print(f"on_message_delete {Fore.RED} [ FAILED ]: {e}{Fore.RESET}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            config = await self.get_config(member.guild)
            User_Logs_ID = config.get("user_logs_channel")
            User_Logs = member.guild.get_channel(User_Logs_ID)

            embed = discord.Embed(
                title="Member Join Log",
                description=f"{self.get_time()} - {member.name} joined the server",
                color=0x43B581
            )
            await User_Logs.send(embed=embed)
        except Exception as e:
            print(f"on_member_join {Fore.RED} [ FAILED ]: {e}{Fore.RESET}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            config = await self.get_config(member.guild)
            User_Logs_ID = config.get("user_logs_channel")
            User_Logs = member.guild.get_channel(User_Logs_ID)

            embed = discord.Embed(
                title="Member Removal Log",
                description=f"{self.get_time()} - {member.name} left the server",
                color=0xF04747
            )
            await User_Logs.send(embed=embed)
        except Exception as e:
            print(f"on_member_remove {Fore.RED} [ FAILED ]: {e}{Fore.RESET}")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            config = await self.get_config(after.guild)
            User_Logs_ID = config.get("user_logs_channel")
            User_Logs = after.guild.get_channel(User_Logs_ID)

            embed = discord.Embed(
                title="Member Update Log",
                description=f"{self.get_time()} - Member {before.name} updated",
                color=0x9B51E0
            )

            if before.nick != after.nick:
                if after.nick is None:
                    embed.add_field(name="Nickname", value=f"{before.name} removed their nickname", inline=False)
                else:
                    embed.add_field(name="Nickname", value=f"{before.name} changed their nickname to {after.nick}", inline=False)

            elif before.roles != after.roles:
                if len(before.roles) > len(after.roles):
                    for role in before.roles:
                        if role not in after.roles:
                            embed.add_field(name="Role Update", value=f"{before.name} removed the {role} role", inline=False)
                else:
                    for role in after.roles:
                        if role not in before.roles:
                            embed.add_field(name="Role Update", value=f"{before.name} added the {role} role", inline=False)

            elif before.pending != after.pending:
                if after.pending:
                    embed.add_field(name="Member Update", value=f"{before.name} joined the server", inline=False)
                else:
                    embed.add_field(name="Member Update", value=f"{before.name} is now a member of the server", inline=False)

            elif before.premium_since != after.premium_since:
                if after.premium_since is None:
                    embed.add_field(name="Boost Update", value=f"{before.name}'s boost has ended", inline=False)
                else:
                    embed.add_field(name="Boost Update", value=f"{before.name} boosted the server", inline=False)



            await User_Logs.send(embed=embed)
        except Exception as e:
            print(f"on_member_update {Fore.RED} [ FAILED ]: {e}{Fore.RESET}")



    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        try:
            config = await self.get_config(after)
            Mod_Logs_ID = config.get("mod_logs_channel")
            Mod_Logs = after.get_channel(Mod_Logs_ID)

            embed = discord.Embed(
                title="Guild Update Log",
                description=f"{self.get_time()} - Guild {before.name} updated",
                color=0xFFD700
            )

            if before.name != after.name:
                embed.add_field(name="Name Update", value=f"{before.name} changed their name to {after.name}", inline=False)

            elif before.afk_timeout != after.afk_timeout:
                embed.add_field(name="AFK Timeout Update", value=f"{before.name} changed their AFK timeout to {after.afk_timeout}", inline=False)

            elif before.afk_channel != after.afk_channel:
                embed.add_field(name="AFK Channel Update", value=f"{before.name} changed their AFK channel to {after.afk_channel}", inline=False)

            elif before.owner != after.owner:
                embed.add_field(name="Owner Update", value=f"{before.name} changed their owner to {after.owner}", inline=False)

            elif before.verification_level != after.verification_level:
                embed.add_field(name="Verification Level Update", value=f"{before.name} changed their verification level to {after.verification_level}", inline=False)

            elif before.explicit_content_filter != after.explicit_content_filter:
                embed.add_field(name="Explicit Content Filter Update", value=f"{before.name} changed their explicit content filter to {after.explicit_content_filter}", inline=False)

            elif before.mfa_level != after.mfa_level:
                embed.add_field(name="MFA Level Update", value=f"{before.name} changed their MFA level to {after.mfa_level}", inline=False)

            elif before.system_channel != after.system_channel:
                embed.add_field(name="System Channel Update", value=f"{before.name} changed their system channel to {after.system_channel}", inline=False)

            elif before.system_channel_flags != after.system_channel_flags:
                embed.add_field(name="System Channel Flags Update", value=f"{before.name} changed their system channel flags to {after.system_channel_flags}", inline=False)

            elif before.rules_channel != after.rules_channel:
                embed.add_field(name="Rules Channel Update", value=f"{before.name} changed their rules channel to {after.rules_channel}", inline=False)

            elif before.public_updates_channel != after.public_updates_channel:
                embed.add_field(name="Public Updates Channel Update", value=f"{before.name} changed their public updates channel to {after.public_updates_channel}", inline=False)

            elif before.preferred_locale != after.preferred_locale:
                embed.add_field(name="Preferred Locale Update", value=f"{before.name}'s preferred locale changed to {after.preferred_locale}", inline=False)

            elif before.features != after.features:
                embed.add_field(name="Features Update", value=f"{before.name}'s features changed to\n```{after.features}```", inline=False)

            elif before.premium_tier != after.premium_tier:
                embed.add_field(name="Premium Tier Update", value=f"{before.name}'s premium tier changed to {after.premium_tier}", inline=False)

            elif before.premium_subscription_count != after.premium_subscription_count:
                embed.add_field(name="Premium Subscription Count Update", value=f"{before.name}'s premium subscription count changed to {after.premium_subscription_count}", inline=False)

            elif before.banner != after.banner:
                embed.add_field(name="Banner Update", value=f"{before.name}'s banner changed to {after.banner}", inline=False)

            elif before.description != after.description:
                embed.add_field(name="Description Update", value=f"{before.name}'s description changed to {after.description}", inline=False)

            elif before.splash != after.splash:
                embed.add_field(name="Splash Update", value=f"{before.name}'s splash changed to {after.splash}", inline=False)

            elif before.discovery_splash != after.discovery_splash:
                embed.add_field(name="Discovery Splash Update", value=f"{before.name}'s discovery splash changed to {after.discovery_splash}", inline=False)

            elif before.max_video_channel_users != after.max_video_channel_users:
                embed.add_field(name="Max Video Channel Users Update", value=f"{before.name}'s max video channel users changed to {after.max_video_channel_users}", inline=False)

            elif before.max_presences != after.max_presences:
                embed.add_field(name="Max Presences Update", value=f"{before.name}'s max presences changed to {after.max_presences}", inline=False)

            elif before.max_members != after.max_members:
                embed.add_field(name="Max Members Update", value=f"{before.name}'s max members changed to {after.max_members}", inline=False)

            elif before.max_emoji != after.max_emoji:
                embed.add_field(name="Max Emoji Update", value=f"{before.name}'s max emoji changed to {after.max_emoji}", inline=False)

            elif before.max_channels != after.max_channels:
                embed.add_field(name="Max Channels Update", value=f"{before.name}'s max channels changed to {after.max_channels}", inline=False)

            elif before.max_roles != after.max_roles:
                embed.add_field(name="Max Roles Update", value=f"{before.name}'s max roles changed to {after.max_roles}", inline=False)

            elif before.max_attachments != after.max_attachments:
                embed.add_field(name="Max Attachments Update", value=f"{before.name}'s max attachments changed to {after.max_attachments}", inline=False)

            elif before.max_webhooks != after.max_webhooks:
                embed.add_field(name="Max Webhooks Update", value=f"{before.name}'s max webhooks changed to {after.max_webhooks}", inline=False)

            await Mod_Logs.send(embed=embed)
        except Exception as e:
            print(f"on_guild_update {Fore.RED} [ FAILED ]: {e}{Fore.RESET}")


    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        try:
            config = await self.get_config(role.guild)
            Mod_Logs_ID = config.get("mod_logs_channel")
            Mod_Logs = role.guild.get_channel(Mod_Logs_ID)

            embed = discord.Embed(
                title="Guild Role Creation Log",
                description=f"{self.get_time()} - {role.name} role was created",
                color=0x43B581
            )
            await Mod_Logs.send(embed=embed)
        except Exception as e:
            print(f"on_guild_role_create {Fore.RED} [ FAILED ]: {e}{Fore.RESET}")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        try:
            config = await self.get_config(role.guild)
            Mod_Logs_ID = config.get("mod_logs_channel")
            Mod_Logs = role.guild.get_channel(Mod_Logs_ID)

            embed = discord.Embed(
                title="Guild Role Deletion Log",
                description=f"{self.get_time()} - {role.name} role was deleted",
                color=0xF04747
            )
            await Mod_Logs.send(embed=embed)
        except Exception as e:
            print(f"on_guild_role_delete {Fore.RED} [ FAILED ]: {e}{Fore.RESET}")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        try:
            config = await self.get_config(guild)
            Mod_Logs_ID = config.get("mod_logs_channel")
            Mod_Logs = guild.get_channel(Mod_Logs_ID)

            embed = discord.Embed(
                title="Member Ban Log",
                description=f"{self.get_time()} - {user.name} was banned from {guild.name}",
                color=0xE53935
            )
            await Mod_Logs.send(embed=embed)
        except Exception as e:
            print(f"on_member_ban {Fore.RED} [ FAILED ]: {e}{Fore.RESET}")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        try:
            config = await self.get_config(guild)
            Mod_Logs_ID = config.get("mod_logs_channel")
            Mod_Logs = guild.get_channel(Mod_Logs_ID)

            embed = discord.Embed(
                title="Member Unban Log",
                description=f"{self.get_time()} - {user.name} was unbanned from {guild.name}",
                color=0x43B581
            )
            await Mod_Logs.send(embed=embed)
        except Exception as e:
            print(f"on_member_unban {Fore.RED} [ FAILED ]: {e}{Fore.RESET}")

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        try:
            config = await self.get_config(invite.guild)
            Mod_Logs_ID = config.get("mod_logs_channel")
            Mod_Logs = invite.guild.get_channel(Mod_Logs_ID)

            embed = discord.Embed(
                title="Invite Creation Log",
                description=f"{self.get_time()} - {invite.inviter.name} created an invite for {invite.guild.name}",
                color=0x5865F2
            )
            await Mod_Logs.send(embed=embed)
        except Exception as e:
            print(f"on_invite_create {Fore.RED} [ FAILED ]: {e}{Fore.RESET}")

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        try:
            config = await self.get_config(invite.guild)
            Mod_Logs_ID = config.get("mod_logs_channel")
            Mod_Logs = invite.guild.get_channel(Mod_Logs_ID)

            embed = discord.Embed(
                title="Invite Deletion Log",
                description=f"{self.get_time()} - {invite.inviter.name} deleted an invite for {invite.guild.name}",
                color=0xF9A825
            )
            await Mod_Logs.send(embed=embed)
        except Exception as e:
            print(f"on_invite_delete {Fore.RED} [ FAILED ]: {e}{Fore.RESET}")

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        try:
            config = await self.get_config(channel.guild)
            Mod_Logs_ID = config.get("mod_logs_channel")
            Mod_Logs = channel.guild.get_channel(Mod_Logs_ID)

            embed = discord.Embed(
                title="Guild Channel Creation Log",
                description=f"{self.get_time()} - {channel.name} was created in {channel.guild.name}",
                color=0x5865F2
            )
            await Mod_Logs.send(embed=embed)
        except Exception as e:
            print(f"on_guild_channel_create {Fore.RED} [ FAILED ]: {e}{Fore.RESET}")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        try:
            config = await self.get_config(channel.guild)
            Mod_Logs_ID = config.get("mod_logs_channel")
            Mod_Logs = channel.guild.get_channel(Mod_Logs_ID)

            embed = discord.Embed(
                title="Guild Channel Deletion Log",
                description=f"{self.get_time()} - {channel.name} was deleted in {channel.guild.name}",
                color=0xF9A825
            )
            await Mod_Logs.send(embed=embed)
        except Exception as e:
            print(f"on_guild_channel_delete {Fore.RED} [ FAILED ]: {e}{Fore.RESET}")

async def setup(client):
    try:
        await client.add_cog(Logs(client))
    except Exception as e:
        print(f"{Fore.RED}Error adding Logs Cog: {e}{Fore.RESET}")
