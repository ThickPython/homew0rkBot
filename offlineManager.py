import discord
import os
import json
from thingsthatcouldbeuseful import getFile

TOKEN = os.environ['DISCORD_TOKEN']

getFile('settings.json')
with open('settings.json') as settings_file:
    settingsList = json.load(settings_file)
    GUILD = settingsList["serverName"]
    summon = settingsList["summon"]


client = discord.Client()

print("offline manager ironically online")

@client.event
async def on_message(message):
    if message.channel.name == "calendar":
        if summon in message:
            await message.channel.send("no idea if you were trying to invoke the bot, but I'm offline now so")

client.run(TOKEN)