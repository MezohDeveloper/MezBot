import discord
import os
import asyncio
from itertools import cycle
from discord.ext import commands, tasks
from datetime import datetime
from dotenv import load_dotenv
from colorama import Fore

# Load environment variables #
load_dotenv()
Dtoken = os.getenv('TOKEN')
# --------- #

# Set prefix, client, and remove defualt help command #
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
client.remove_command('help')
# --------- #

current = datetime.now()
TimeStamp = current.strftime('%H:%M:%S')
# ASCII ART #
ascii_logo = """
'##::::'##:'########:'########::::'########:::'#######::'########:
 ###::'###: ##.....::..... ##::::: ##.... ##:'##.... ##:... ##..::
 ####'####: ##::::::::::: ##:::::: ##:::: ##: ##:::: ##:::: ##::::
 ## ### ##: ######:::::: ##::::::: ########:: ##:::: ##:::: ##::::
 ##. #: ##: ##...:::::: ##:::::::: ##.... ##: ##:::: ##:::: ##::::
 ##:.:: ##: ##:::::::: ##::::::::: ##:::: ##: ##:::: ##:::: ##::::
 ##:::: ##: ########: ########:::: ########::. #######::::: ##::::
..:::::..::........::........:::::........::::.......::::::..:::::                                                                                                      
|Developed by: Mezoh|
----------------------------
"""
# --------- #

# When the bot is ready (on_ready event) #
@client.event
async def on_ready():
    try: 
        synced = await client.tree.sync()
        print(f"{TimeStamp} - {Fore.GREEN}[ OK ]{Fore.RESET} Synced {len(synced)} commands!")
    except:
        print(f'{TimeStamp} - {Fore.RED}[ FAILED ]{Fore.RESET} already synced')
    print(f"{TimeStamp} - {Fore.GREEN}[ OK ]{Fore.RESET} Connected to {client.user.name}!\n\n{Fore.YELLOW}{ascii_logo}{Fore.RESET}")
    change_status.start()
# --------- #

# Bot status cycle #
status = cycle([
"😈 My Lmanburg Phil! My unfinished symphony forever unfinished!!",
"💩 Made By <@1205617300875771984> damn writing this feels sad",
"🤖 NO IM NOT FUCKING JARVIS",
"👩 just killed a woman feeling good",
"🔛 https://discord.gg/jCZJNgz7DB 🔝"
""
])

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=next(status))) # Status cycle and display status, do_not_disturb | online | idle | compete
# --------- #

# Load Cogs #
async def load_cogs():
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
# --------- #

# Main func. to run the bot #
async def main():
    async with client:
        try:
            await load_cogs()
        except Exception as e:
            print(f"{TimeStamp} - {Fore.RED}[ FAILED ]{Fore.RESET} Error loading cogs: {e}") # Check if any "cogs"(python files) have an error when loading into the bot. 
        await client.start(Dtoken)
# --------- #

# Run the main function #
asyncio.run(main())
# --------- #