#VE reference https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

import os

#activate environment
#os.system('cmd /k "poetry shell" ')
#os.system('cmd /k "python bot.py"')

import discord
import json
import random

from devutil import *
from cmdutil import *

from homeworkfuncs import *
from gnapfuncs import *

#------------------------------------------------
#discord client setup

#settings_list = get_file('settings.json')
#GUILD = settings_list["serverName"]
#summon = settings_list["summon"]

summon = "c!"


TOKEN = os.environ['DISCORD_TOKEN']

client = discord.Client()

#-------------------------------------------------

#class CustomClient(discord.Client):
@client.event
async def on_ready():
    print('lets get this party started')
    await client.change_presence(status = discord.Status.online, activity= discord.Game(name = "c!help"))
    """ 
    guild = discord.utils.get(client.guilds, name=GUILD)
    listOfMembers = guild.members
    for member in guild.members:
        CBU.addMember(member.id, member.roles) """

commands = [
    "add",
    "view",
    "remove",
    "hw",
    "gnapadd",
    "gt",
    "gtreverse",

    "avy",
    "ping"

]

admincommands = [
    "allteachers",
    "addteacher",
    "removeteacher",
    "eval"
]
    

@client.event
async def on_message(message): 
    if (message.author.bot): return
    channel = message.channel
    the_message = message.content.split(' ')
    header = the_message[0]

    #if message.channel.name != "bot-testing":
    #    return
    
    #help
    if header == f'{summon}help':
        embedHelp = discord.Embed(title = "Help", description = "A quick how 2 on how to do things")
        embedHelp.add_field(name = "c!hw", value = "View all your teachers including ongoing assignments (don't worry, we already know who your teachers are lul)\nUse `c!me` to summon, and then check your Dm's")
        embedHelp.add_field(name = "c!add", value = "Adds homework and due date to a certain teacher\nUse `c!add teacher: {teacher} title: {title of assignment} description: {description of assignment} due: {due date}` \n(note: YES IT'S CASE SENSITIVE)", inline = False)
        embedHelp.add_field(name = "c!view", value = "Views current assignments and due dates for a certain teacher\nUse `c!view {teacher}` to summon", inline = False)
        embedHelp.add_field(name = "c!remove", value = "Removes an assignment from a certain teacher, remember to use c!view {teacher} so you can copy/paste the assignment name\nUse `c!remove {teacher} {exact assignment name}` to remove", inline = False)
        embedHelp.add_field(name="c!help2", value="Misc commands") 
        await channel.send(embed = embedHelp)
    
    #help2
    if header == f'{summon}help2':
        embedHelp2 = discord.Embed(title = "Help for other things", description = "some other stuff you can do with Ton bot")
        embedHelp2.add_field(name = "`c!help`", value = "What do you think it does you mega 5head :5head:\nUse 'c!help' to summon", inline = False)
        embedHelp2.add_field(name = "`c!gt`", value = "Translates gnap's words to English\nUse `c!gt {word}`", inline = False)
        embedHelp2.add_field(name = "`c!gtreverse`", value = "Translates normal words to gnapish (if they exist)", inline = False)
        await channel.send(embed = embedHelp2)


    for command in commands:
        if header.lower() == f"{summon}{command}":
            await eval(f"{command}")(message)

    if message.author.id == 241288855368499200:
        for command in admincommands:
            if header.lower() == f"{summon}{command}":
                if header.lower() == f"{summon}eval":
                    await eval(f"evaluate")(message)
                else:
                    await eval(f"{command}")(message)




client.run(TOKEN)






