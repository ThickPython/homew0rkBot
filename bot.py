import os
import calendar
import discord
import json
import thingsthatcouldbeuseful as CBU
import random

client = discord.Client()

with open('settings.json') as settings_file:
    settingsList = json.load(settings_file)

TOKEN = settingsList["appToken"]
GUILD = settingsList["serverName"]
summon = settingsList["summon"]


client = discord.Client()

#class CustomClient(discord.Client):
@client.event
async def on_ready():""" 
    guild = discord.utils.get(client.guilds, name=GUILD)
    listOfMembers = guild.members
    for member in guild.members:
        CBU.addMember(member.id, member.roles) """
    

    

@client.event
async def on_message(message): 
    if (message.author.bot): return
    channel = message.channel
    theMessage = message.content.split(' ')
    header = theMessage[0]

    #help
    if header == f'{summon}help':
        embedHelp = discord.Embed(title = "Help", description = "A quick how 2 on how to do things")
        embedHelp.add_field(name = "c!viewme", value = "View all your teachers including ongoing assignments (don't worry, we already know who your teachers are ;)\nUse 'c!viewme' to summon")
        embedHelp.add_field(name = "c!add", value = "Adds homework and due date to a certain teacher\nUse 'c!add {teacher} {description} {due date}' (note: NOT case sensitive)", inline = False)
        embedHelp.add_field(name = "c!view", value = "Views current assignments and due dates for a certain teacher\nUse 'c!view {teacher}' to summon", inline = False)
        embedHelp.add_field(name = "c!descrip", value = "Updates your c!viewme description to whatever you want (even supports emojis!)\nUse 'c!descrip {description}' to update", inline = False)
        embedHelp.add_field(name = "c!help2", value = "I've coded in some fun easter eggs in this bot, here's a quick start")
        embedHelp.set_footer(text = "developed with python, by colin the sleep waster, waster of all sleep", icon_url="https://i.imgur.com/trIK0QD.jpg")
        await channel.send(embed = embedHelp)
    
    #help2
    if header == f'{summon}help2':
        embedHelp2 = discord.Embed(title = "Help for other things", description = "some other stuff you can do with Rainsta bot")
        embedHelp2.add_field(name = "c!help", value = "What do you think it does you mega 5head :5head:\nUse 'c!help' to summon", inline = False)
        embedHelp2.add_field(name = "c!god", value = "Praise be")
        embedHelp2.add_field(name = "c!ppsize", value = "They tell you all the time, if you want the results, you gotta measure it, but when you have Rainsta, why measure?\nUse 'c!ppsize {person}' to get the size instantly", inline = False)
        embedHelp2.add_field(name = "riddle", value = "I've hidden a command in the bot, here's a hint to what it is: 'says go', yup, that's the whole hint. It's kind of bias towards some certain students but whatever")
        embedHelp2.set_footer(text = "developed with python, by colin the sleep waster, waster of all sleep", icon_url="https://i.imgur.com/trIK0QD.jpg")
        await channel.send(embed = embedHelp2)

    

    #viewme v2.0
    if header == f'{summon}viewme':
        usersTeacherListTemp = CBU.getTeachers(message.author.roles)
        usersHWListTemp = []

        with open('teachers.json', 'r') as teachers_homework:
            teachersHomeworkDict = json.load(teachers_homework)
            for eachTeacher in usersTeacherListTemp:
                for eachTeacherFile in teachersHomeworkDict:
                    if eachTeacher.lower() == eachTeacherFile["name"]:
                        if len(eachTeacherFile["homework"]) != 0:
                            usersHWListTemp.append({
                                "teacher":eachTeacherFile["name"],
                                "homework":eachTeacherFile["homework"]
                            })
        await channel.send(embed = CBU.makeEmbedMessage(message.author, message.author.roles, usersHWListTemp))

    #add
    if header == f'{summon}add':
        if len(theMessage) < 4:
            await channel.send("insufficient variables to add homework, use h!help to view usage")
        else:
            with open('teachers.json') as teachersList:
                teachersLista = json.load(teachersList)  
            tempTeacher = theMessage[1].lower()
            hwDescription = ' '.join(theMessage[2:-1])
            dueDate = theMessage[-1]
        
            for eachTeacher in teachersLista:
                if tempTeacher == eachTeacher["name"]:
                    addHomework = {
                            "description": (hwDescription),
                            "duedate": dueDate
                        }
                    for teacher in teachersLista:
                        if teacher["name"] == tempTeacher:
                            teachersLista[teachersLista.index(teacher)]["homework"].append(addHomework)
                            with open('teachers.json', 'w') as teachersList:
                                teachersList.seek(0)
                                json.dump(teachersLista, teachersList, indent = 4)
                                teachersList.truncate()
                    await channel.send("it has been added")
                    break     
                        
                    
    #view
    if header == f'{summon}view':
        if len(theMessage) != 2:
           await channel.send("format incorrect, use h!help to view proper usage")
        else:
            theTeacher = theMessage[1].lower()
            teachersLista = open('teachers.json', 'r')  #reference https://www.w3schools.com/python/python_file_open.asp
            teachersList = json.load(teachersLista)
            homeworkList = ""
            for eachTeacher in teachersList:
                if eachTeacher["name"] == theTeacher:
                    if len(eachTeacher["homework"]) == 0 :
                        await channel.send(f'```There is no homework for {CBU.formatname(theTeacher)}, rejoice for you are free```')
                    else:
                        embedView = discord.Embed(title = f'{eachTeacher["name"]} Assignments', description = '')
                        for eachHomework in eachTeacher["homework"]:
                            embedView.add_field(name = f"{eachHomework['description']})
                            homeworkList += f'\t{eachHomework["description"]} due on {eachHomework["duedate"]}\n'
                        await channel.send(f'```\n{CBU.formatname(eachTeacher["name"])}\n{homeworkList}```')

            
            teachersLista.close()
    
    #customdescription
    if header == f'{summon}descrip':
        descriptor = ' '.join(theMessage[1:])
        with open('customDescription.json', 'r+') as registeredNames:
            replaceWith = json.load(registeredNames)
            addThis = {}
            for descriptors in replaceWith:
                if message.author.id == descriptors["discord id"]:
                    descriptors["descriptor"] = descriptor
                    break
                else:
                    addThis = {
                        "discord id":message.author.id,
                        "descriptor":descriptor
                    }
                    break
            replaceWith.append(addThis)
            registeredNames.seek(0)
            json.dump(replaceWith, registeredNames, indent = 4)
            registeredNames.truncate()
        await channel.send("Your description has been updated!")
            
            
    #erik
    if header == f'{summon}god':
        await channel.send("```it is known that there is only one erik jma, and we have that erik jma, the best erik jma anyone has ever known, i guarantee it. number one erik jma i tell you because there is only one to begin with, i actually had a friend who was almost erik jma, but he wasn't, because there is only one erik jma, and he's best in class```")
    
    if header ==f'{summon}testing':
        await channel.send("c!testing")

    if header == f'{summon}ppsize':
        person = ' '.join(theMessage[1:])
        if theMessage[1:] == "me":
            person = message.author.nick
        ppdict = {1:"small", 2:"medium", 3:"large", 4:"massive", 5:"XTRA LARGE", 6:"the smallest thing you've ever seen", 7:"... what? you have a pp? couldn't tell...", 8:"tiny, 'it's laughable, really", 9:" MA S S I VE DIK EN E  R G Y", 10: "small, it's small, that's all there to say about it", 11: ":tanushtanush:", 12: "....HAHAHAH", 13:":penetration:", 14:"average, i'll let you figure out which average", 15:"it's bigger than most, i'll give u that"}  
        ppchosen = random.randint(1,15)
        await channel.send(f"{person} has pp size {ppdict[ppchosen]}")

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