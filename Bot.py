# bot.py
import os
import random
from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonplayerinfo
import numpy as np
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

player_dict = players.get_players()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0:7] == '/player':
        playername = message.content[8:]
        player = [player for player in player_dict if player['full_name'] == playername][0]
        player_id = player['id']
        player_info = commonplayerinfo.CommonPlayerInfo(player_id)
        response = player_info.player_headline_stats.get_dict()['data']
        await message.channel.send(response)

    if message.content[0:5] == '/team':
        teamname = message.content[6:]
        response = teams.find_teams_by_full_name(teamname)
        await message.channel.send(response)


client.run(TOKEN)
