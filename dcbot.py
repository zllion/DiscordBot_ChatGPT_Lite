import os
import random
import discord
from datetime import datetime
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
from chatbot import Session
import logging
import logging.handlers

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
YOUR_CHANNEL_ID = int(os.getenv('YOUR_CHANNEL_ID'))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)

# A dictionary to keep track of which user is in which session
sessions = {}

@bot.event
async def on_message(message):
    author,channel = message.author,message.channel
    if channel.id != YOUR_CHANNEL_ID:
        return
    # Check if the bot was mentioned in the message
    if bot.user in message.mentions or message.content.startswith('-start'):
        # Do something in response to the mention
        if (author,channel) in sessions:
            return
        await start_session(author,channel,message.content)
    if message.content.startswith('-continue') or message.content.startswith('-load'):
        if (author,channel) in sessions:
            return
        ipt = message.content.split(' ')
        if len(ipt)>2:
            await channel.send('invalid input')
        else:
            session_id = ipt[1]
        await start_session(author,channel,session_id = session_id)

async def start_session(author, channel, text=None, session_id = None):
    
    # Create a new session for this user
    sessions[(author,channel)] = []
    # Send a message to the user to let them know the session has started
    await channel.send('Session started! Type messages to get a response. Type -close to end the session.')
    chat_session = Session()
    # Listen to the user's input
    session_close_output = f'Session id is {chat_session.session_id}. Type -continue session_id to continue. Type -start or mention to begin a new session.'
    if text is not None:
        response = chat_session.chat(text)
        sessions[(author,channel)].append(response)
        await channel.send(response)
    if session_id is not None:
        channel.send(chat_session.load(author, session_id))
    while chat_session.token_used_total<15000:
        try:
            message = await bot.wait_for('message', check=lambda msg: msg.author == author and msg.channel == channel, timeout=180)
        except asyncio.TimeoutError:
            await channel.send(f'{author.mention} Session timed out. '+session_close_output )
            break
        # If the user types -close, end the session
        if message.content.startswith('-close') or message.content == 'close':
            await channel.send(f'{author.mention} Session closed. '+session_close_output)
            break

        # Otherwise, respond to the user's message
        response = chat_session.chat(message.content)
        if response.startswith('!!close') or response.endswith('!!close') or response.startswith('Goodbye!'):
            await channel.send(f'{author.mention} Session closed. '+session_close_output)
            break
        sessions[(author,channel)].append(response)
        await channel.send(response)
    else:
        await channel.send(f'{author.mention} Maximum chat load reached! Session end.')
    chat_session.save(author)
    del chat_session
    # Remove the user's session from the dictionary
    del sessions[(author,channel)]

bot.run(TOKEN)
