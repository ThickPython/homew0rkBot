#VE reference https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

import os

#activate environment
#os.system('cmd /k "poetry shell" ')
#os.system('cmd /k "python bot.py"')

import calendar
import discord
import json
import thingsthatcouldbeuseful as CBU
import random
import time
import boto3
from datetime import datetime, timedelta
from threading import Timer
from thingsthatcouldbeuseful import formatname, get_file, upload_file




#-----------------------------------------------
#timer to keep track of things

""" x=datetime.today()
y = x.replace(day=x.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
delta_t = y - x

secs=delta_t.total_seconds()

t = Timer(secs, CBU.deleteOld())
t.start() """

#------------------------------------------------

#------------------------------------------------
#discord client setup

get_file('settings.json')
with open('settings.json') as settings_file_json:
    settings_list = json.load(settings_file_json)
    GUILD = settings_list["serverName"]
    summon = settings_list["summon"]


TOKEN = os.environ['DISCORD_TOKEN']

client = discord.Client()

#-------------------------------------------------

#class CustomClient(discord.Client):
@client.event
async def on_ready():
    print('lets get this party started')
    await client.change_presence(status = discord.Status.online, activity= discord.Game(name = "Fluffy the bruh, c!help"))
    """ 
    guild = discord.utils.get(client.guilds, name=GUILD)
    listOfMembers = guild.members
    for member in guild.members:
        CBU.addMember(member.id, member.roles) """


    

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
        embedHelp.add_field(name = "c!me", value = "View all your teachers including ongoing assignments (don't worry, we already know who your teachers are lul)\nUse `c!me` to summon, and then check your Dm's")
        embedHelp.add_field(name = "c!add", value = "Adds homework and due date to a certain teacher\nUse `c!add teacher: {teacher} title: {title of assignment} description: {description of assignment} due: {due date}` \n(note: YES IT'S CASE SENSITIVE)", inline = False)
        embedHelp.add_field(name = "c!view", value = "Views current assignments and due dates for a certain teacher\nUse `c!view {teacher}` to summon", inline = False)
        embedHelp.add_field(name = "c!remove", value = "Removes an assignment from a certain teacher, remember to use c!view {teacher} so you can copy/paste the assignment name\nUse `c!remove {teacher} {exact assignment name}` to remove", inline = False)
        embedHelp.add_field(name="c!help2", value="Misc commands") 
        await channel.send(embed = embedHelp)
    
    #help2
    if header == f'{summon}help2':
        embedHelp2 = discord.Embed(title = "Help for other things", description = "some other stuff you can do with Ton bot")
        embedHelp2.add_field(name = "`c!help`", value = "What do you think it does you mega 5head :5head:\nUse 'c!help' to summon", inline = False)
        embedHelp2.add_field(name = "`c!god`", value = "Praise be")
        embedHelp2.add_field(name = "`c!gt`", value = "Translates gnap's words to English\nUse `c!gt {word}`", inline = False)
        embedHelp2.add_field(name = "`c!gtreverse`", value = "Translates normal words to gnapish (if they exist)", inline = False)
        await channel.send(embed = embedHelp2)

    

    #viewme v2.0
    if header == f'{summon}meold':
        usersTeacherListTemp = CBU.getTeachers(message.author.roles)
        usersHWListTemp = []
        get_file('teachers.json')
        with open('teachers.json', 'r') as teachers_homework_json:
            teachersHomeworkDict = json.load(teachers_homework_json)
            for each_teacher in usersTeacherListTemp:
                for each_teacher_file in teachersHomeworkDict:
                    if each_teacher.lower() == each_teacher_file["name"]:
                        if len(each_teacher_file["homework"]) != 0:
                            usersHWListTemp.append({
                                "teacher":each_teacher_file["name"],
                                "homework":each_teacher_file["homework"]
                            })
        #await channel.send(embed = CBU.makeEmbedMessage(message.author, message.author.roles, usersHWListTemp))
    
    if header == f'{summon}me':
        if message.author.dm_channel == None:
            await message.author.create_dm()
        usersTeacherListTemp = CBU.getTeachers(message.author.roles)
        usersHWListTemp = []
        get_file('teachers.json')
        with open('teachers.json', 'r') as teachers_homework_json:
            teachersHomeworkDict = json.load(teachers_homework_json)
            for each_teacher in usersTeacherListTemp:
                for each_teacher_file in teachersHomeworkDict:
                    if each_teacher.lower() == each_teacher_file["name"]:
                        if len(each_teacher_file["homework"]) != 0:
                            await message.author.dm_channel.send(embed = CBU.makeEmbedMessage2(each_teacher_file["name"], each_teacher_file["homework"]))
        await channel.send("You've been DM'ed a list of your Homework go check it")

    #add
    if header == f'{summon}add':
        if ("teacher:" not in the_message or
            "title:" not in the_message or
            "description:" not in the_message or
            "due:" not in the_message):
            await channel.send("incorrect usage of c!add command, use c!help to view usage")
        else:
            get_file('teachers.json')
            with open('teachers.json', 'r') as teachers_list_json:
                teachers_lista = json.load(teachers_list_json)  
            sort_this = the_message
            print(sort_this)
            indexTeacher = sort_this.index("teacher:")
            indexTitle = sort_this.index("title:")
            indexDescription = sort_this.index("description:")
            indexDueDate = sort_this.index("due:")
            if indexDueDate - indexDescription == 1:    #reference https://www.geeksforgeeks.org/python-list-insert/
                sort_this.insert(indexDueDate, "there is no description")
            indexDueDate = sort_this.index("due:")
            whereteacheris = 0 
            for each_teacher in teachers_lista:
                if sort_this[indexTeacher+1].lower() == each_teacher["name"]:
                    addHomework = {
                            "title": formatname(' '.join(sort_this[(indexTitle+1):indexDescription])),
                            "description": formatname(' '.join(sort_this[(indexDescription+1):indexDueDate])),
                            "duedate": sort_this[-1]
                        }
                    for teacher in teachers_lista:
                        if teacher["name"] == sort_this[indexTeacher + 1].lower():
                            teachers_lista[teachers_lista.index(teacher)]["homework"].append(addHomework)
                            break
                    break
            with open('teachers.json', 'w') as teachers_list_json:
                json.dump(teachers_lista, teachers_list_json, indent=4)
            upload_file('teachers.json')
            await channel.send("it has been added")  
    
    #remove
    if header == f'{summon}remove':
        the_teacher = the_message[1].lower()
        the_title = formatname(' '.join(the_message[2:]))
        errorReason = ""
        get_file('teachers.json')
        with open('teachers.json', 'r') as teachers_list_json:
            teachers_list = json.load(teachers_list_json)
        teacher_found = False
        for teacher in teachers_list:
            if teacher['name'] == the_teacher:
                teacher_found = True
                updatedHomework = teacher["homework"].copy()
                if len(updatedHomework):
                    for homework in updatedHomework:
                        if the_title == homework["title"]:
                            updatedHomework.remove(homework)
                else:
                    errorReason = "there is no homework for this teacher"
                    await channel.send(f'Failed to delete homework because {errorReason}')
                    break
                if teacher["homework"] != updatedHomework:
                    await channel.send(f'Successfully deleted "{the_title}" from {formatname(the_teacher)}')
                teacher["homework"] = updatedHomework
        if teacher_found == False:
            await channel.send(f"We couldn't find `{the_teacher}`. Check your spelling and try again")
        with open('teachers.json', 'w') as teachers_list_json:
            teachers_list_json.seek(0)
            json.dump(teachers_list, teachers_list_json, indent=4)
            teachers_list_json.truncate()
        upload_file('teachers.json')
            
        
                    
    #view
    if header == f'{summon}view':
        if len(the_message) != 2:
           await channel.send("format incorrect, use c!help to view proper usage")
        else:
            the_teacher = the_message[1].lower()
            get_file('teachers.json')
            with open('teachers.json', 'r') as teachers_list_json:  #reference https://www.w3schools.com/python/python_file_open.asp
                teachers_list = json.load(teachers_list_json)

            descriptionEmoji = ''
            """ if the_teacher in ['ton', 'villagomez', 'oliveira', 'kickham', 'yanez', 'thompson', 'stearns', 'lockett', 'gatewood', 'gadre']:
                descriptionEmoji = f':{the_teacher}:' """
                
            embedView = discord.Embed(title=f'{formatname(the_message[1])} assignments', description = descriptionEmoji)

            homework_list = ""
            for each_teacher in teachers_list:
                teacher_found = False
                if each_teacher["name"] == the_teacher:
                    teacher_found = True
                    if len(each_teacher["homework"]) == 0 :
                        embedView.add_field(name = "Homework", value = f'There is no homework for {formatname(the_teacher)}')
                    else:
                        for eachHomework in each_teacher["homework"]:
                            embedView.add_field(name = f'**"{eachHomework["title"]}" due on {eachHomework["duedate"]}**', value = f"> {eachHomework['description']}", inline = False) 
                if teacher_found:
                    await channel.send(embed = embedView)
                else:
                    await channel.send(f"`{the_teacher}` check your spelling and try again (If you're confident that this teacher exists, contact an admin)")
                return



#------------------------------------------------------
#gnap
    if message.author.name == "NapKat":
        get_file('settings.json')
        with open('settings.json', 'r') as teachers_list_json:
            translated = []
            settings_list = json.load(settings_list_json)
            if settings_list["gnapToggle"] == "on":
                #gnapMessage = message.content.split('')
                get_file('gnap.json')
                with open('gnap.json', 'r') as gnap_list_json:
                    gnap_list = json.load(gnap_list_json)
                    for word in the_message:
                        foundword = False
                        for stupidWord in gnap_list:
                            if stupidWord["word"] == word.lower():
                                translated.append(stupidWord["def"])
                                foundword = True
                                break
                        if foundword == False:
                            translated.append(word)       
                if translated != the_message:
                    embedGnap = discord.Embed(title = "GnapTranslator", description = "Translates what Gnap is saying")
                    embedGnap.add_field(name="Original language", value=message.content)
                    embedGnap.add_field(name="English translation", value=' '.join(translated))
                    await channel.send(embed=embedGnap) 
            #embedGnap.set_footer(text = "developed with python, by colin the sleep waster, waster of all sleep", icon_url="https://i.imgur.com/trIK0QD.jpg")
            
        
    if header == f'{summon}gnapadd':
        if (message.author.name == "Rez" or
            message.author.name == "NapKat"):
            add_word = the_message[1]
            add_def = ' '.join(the_message[2:])
            get_file('gnap.json')
            with open('gnap.json', 'r') as gnap_list_json:
                gnap_list = json.load(gnap_list_json)
            if add_word in gnap_list:
                await channel.send("You've already added this word")
                return
            gnap_list[add_word] = add_def
            with open('gnap.json', 'w') as gnap_list_json:
                gnap_list_json.seek(0)
                json.dump(gnap_list, gnap_list_json, indent = 4)
                gnap_list_json.truncate()
            upload_file('gnap.json')
            await channel.send("added word")
        else:
            await channel.send("you're not gnap")
            return

    if header == f'{summon}togglegnap':
        if (message.author.name == "Rez" or 
            message.author.name == "Erikjma" or
            message.author.name == "Vish" or
            message.author.name == "NapKat" or
            message.author.name == "Aethernolt"):
            get_file('settings.json')
            with open('settings.json', 'r+') as settings_list_json:
                settings_list = json.load(settings_list_json)
                if settings_list["gnapToggle"] == "on":
                    settings_list["gnapToggle"] = "off"
                else:
                    settings_list["gnapToggle"] = "on"
                json.dump(settings_list, settings_list_json, indent=4)
                await channel.send(f'_Gnap Translator has been set to `{settings_list["gnapToggle"]}`_')
            upload_file('settings.json')
    
    if header == f'{summon}gt':
        translate_this = ' '.join(the_message[1:])
        get_file('gnap.json')
        with open('gnap.json', 'r') as gnap_list_jsont:
            gnap_list = json.load(gnap_list_json)
        for word in gnap_list:
            if word == translate_this:
                await channel.send(f'{translate_this} = {gnap_list[word]}')
                return
            else: 
                await channel.send(f"{translate_this} is not a word!")

    if header == f'{summon}gtreverse':
        translate_this = ' '.join(the_message[1:])
        print(translate_this)
        get_file('gnap.json')
        with open('gnap.json', 'r') as gnap_list_json:
            gnap_list = json.load(gnap_list_json)
        for word in gnap_list:
            if gnap_list[word].lower() == translate_this.lower():
                await channel.send(f'{translate_this} = {word}')
                return
            else: 
                await channel.send(f"{translate_this} doesn't have any Gnap equivalent!")

#------------------------------------------------------



client.run(TOKEN)







#things that don't matter

#print(
    #    f'{client.user} is connected to the following guild:\n'
    #    f'{guild.name}(id: {guild.id})'
    #)

    #members = '\n - '.join([member.name for member in guild.members])
    #print(f'Guild Members:\n - {members}')

# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my discord server!')