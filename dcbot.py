import os
import random
import discord
from datetime import datetime
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True  # Enable the privileged gateway intent
bot = commands.Bot(command_prefix='!',intents=intents)

# A dictionary to keep track of which user is in which session
sessions = {}

@bot.command(name='start')
async def start_session(ctx):
    if ctx.author in sessions:
        await ctx.send('You already have an active session!')
        return
    
    # Create a new session for this user
    sessions[ctx.author] = []

    # Send a message to the user to let them know the session has started
    await ctx.send('Session started! Type messages to get a response. Type !close to end the session.')

    # Listen to the user's input
    while True:
        try:
            message = await bot.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=120)
        except asyncio.TimeoutError:
            await ctx.send('Session timed out. Type !start to begin a new session.')
            break

        # If the user types !close, end the session
        if message.content.startswith('!close'):
            await ctx.send('Session closed. Type !start to begin a new session.')
            break

        # Otherwise, respond to the user's message
        response = f'You said: {message.content}'
        sessions[ctx.author].append(response)
        await ctx.send(response)

    # Remove the user's session from the dictionary
    del sessions[ctx.author]

bot.run(TOKEN)
