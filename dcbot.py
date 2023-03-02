import os
import random
import discord
from datetime import datetime
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
from chatbot import Session

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
YOUR_CHANNEL_ID = int(os.getenv('YOUR_CHANNEL_ID'))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)

# A dictionary to keep track of which user is in which session
sessions = {}

@bot.command(name='start', help='start to chat with chatGPT')
async def start_session(ctx):
    if ctx.channel.id != YOUR_CHANNEL_ID:
        return
    author = ctx.author
    channel = ctx.channel
    if (author,channel) in sessions:
        await ctx.send('You already have an active session!')
        return
    
    # Create a new session for this user
    sessions[(author,channel)] = []
    # Send a message to the user to let them know the session has started
    await ctx.send('Session started! Type messages to get a response. Type !close to end the session.')
    chat_session = Session()
    # Listen to the user's input
    while chat_session.token_used_total<10000:
        try:
            message = await bot.wait_for('message', check=lambda msg: msg.author == author and msg.channel == channel, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send('Session timed out. Type !start to begin a new session.')
            break

        # If the user types !close, end the session
        if message.content.startswith('!close'):
            await ctx.send('Session closed. Type !start to begin a new session.')
            break

        # Otherwise, respond to the user's message
        response = chat_session.chat(message.content)
        sessions[(author,channel)].append(response)
        await ctx.send(response)
    else:
        ctx.send('Maximum chat load reached! Session end.')

    # Remove the user's session from the dictionary
    del sessions[(author,channel)]

bot.run(TOKEN)
