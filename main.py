import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
from gtts import gTTS

# Load environment variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You need to be in a voice channel to use this command.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel.")

@bot.command()
async def tts(ctx, *, text):
    if ctx.voice_client:
        tts = gTTS(text=text, lang='en')
        tts.save("tts.mp3")
        
        source = discord.FFmpegPCMAudio("tts.mp3")
        ctx.voice_client.play(source)
        
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        
        os.remove("tts.mp3")
    else:
        await ctx.send("I need to be in a voice channel to use text-to-speech. Use !join first.")

# Get the bot token from the environment variable
bot_token = os.getenv('BOT_TOKEN')

if bot_token is None:
    raise ValueError("No BOT_TOKEN found in .env file")

bot.run(bot_token)