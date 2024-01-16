import discord
import json
import random
intents = discord.Intents.all()
intents.members = True
from discord.ext import commands
bot = commands.Bot(command_prefix='$', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------------')
    print("The bot is ready!")
    await bot.change_presence(
        #activity=discord.listening(f"with {len(bot.guilds)} servers | version: 1.0.2"),
        activity=discord.Activity(type=discord.ActivityType.watching, name="Someone 👀"),
    )

async def get_source():
    file = await get_elements("file")
    source = discord.FFmpegPCMAudio(file)
    return source

async def get_elements(need):
    with open('config.json', 'r') as f:
        data = json.load(f)
        if need == "memberId":
            return data['memberId']
        elif need == "file":
            return data['filename']

@bot.event
async def on_voice_state_update(member: discord.Member, before, after):
    memberId = await get_elements("memberId")
    
    if member.id == memberId and before.channel is not None and after.channel is None:
        try:
            voice_client = bot.voice_clients[0]
            await voice_client.disconnect()
        except:
            pass
    elif member.id == memberId and before.channel != after.channel:
        source = await get_source()
        if before.channel != None:
            voice_client = bot.voice_clients[0]
            await voice_client.disconnect()
        # Connect to the new voice channel
            vc = after.channel
            await vc.connect()
            voice_client = bot.voice_clients[0]
            voice_client.play(source)
        else:
            vc = after.channel
            await vc.connect()
            voice_client = bot.voice_clients[0]            
            voice_client.play(source)

bot.run('Your token goes here.')

