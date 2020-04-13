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
from thingsthatcouldbeuseful import formatname, getFile, uploadFile




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

getFile('settings.json')
with open('settings.json') as settings_file:
    settingsList = json.load(settings_file)
    GUILD = settingsList["serverName"]
    summon = settingsList["summon"]


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
    theMessage = message.content.split(' ')
    header = theMessage[0]

    #if message.channel.name != "bot-testing":
    #    return

    

    #help
    if header == f'{summon}help':
        embedHelp = discord.Embed(title = "Help", description = "A quick how 2 on how to do things")
        embedHelp.add_field(name = "c!me", value = "View all your teachers including ongoing assignments (don't worry, we already know who your teachers are lul)\nUse `c!me` to summon, and then check your Dm's")
        embedHelp.add_field(name = "c!add", value = "Adds homework and due date to a certain teacher\nUse `c!add teacher: {teacher} title: {title of assignment} description: {description of assignment} due: {due date}` \n(note: YES IT'S CASE SENSITIVE)", inline = False)
        embedHelp.add_field(name = "c!view", value = "Views current assignments and due dates for a certain teacher\nUse `c!view {teacher}` to summon", inline = False)
        embedHelp.add_field(name = "c!remove", value = "Removes an assignment from a certain teacher, remember to use c!view {teacher} so you can copy/paste the assignment name\nUse `c!remove {teacher} {exact assignment name}` to remove", inline = False)
        embedHelp.add_field(name="c!help2", value="For when you're bored") 
        embedHelp.set_footer(text = "developed with python, by colin the sleep waster, waster of all sleep", icon_url="https://i.imgur.com/trIK0QD.jpg")
        await channel.send(embed = embedHelp)
    
    #help2
    if header == f'{summon}help2':
        embedHelp2 = discord.Embed(title = "Help for other things", description = "some other stuff you can do with Rainsta bot")
        embedHelp2.add_field(name = "`c!help`", value = "What do you think it does you mega 5head :5head:\nUse 'c!help' to summon", inline = False)
        embedHelp2.add_field(name = "`c!god`", value = "Praise be")
        embedHelp2.add_field(name = "`c!ppsize`", value = "They tell you all the time, if you want the results, you gotta measure it, but when you have Rainsta, why measure?\nUse `'c!ppsize {person}'` to get the size instantly", inline = False)
        embedHelp2.add_field(name = "`c!gt`", value = "You've seen Gnapika talk, it's weird init?\nUse `c!gt {word}` to get the translation of Gnap's fruits", inline = False)
        embedHelp2.add_field(name = "`c!_______`", value = "So you're bored huh? I can offer you some, 'exclusive' rewards for completing the hunt. More specifically, a role, which no-one, not even the admins will have. That is of course, assuming they don't complete the puzzle. happy hunting, `___saysgo`", inline = False)
        embedHelp2.set_footer(text = "developed with python, by colin the sleep waster, waster of all sleep", icon_url="https://i.imgur.com/trIK0QD.jpg")
        await channel.send(embed = embedHelp2)

    

    #viewme v2.0
    if header == f'{summon}meold':
        usersTeacherListTemp = CBU.getTeachers(message.author.roles)
        usersHWListTemp = []
        getFile('teachers.json')
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
        #await channel.send(embed = CBU.makeEmbedMessage(message.author, message.author.roles, usersHWListTemp))
    
    if header == f'{summon}me':
        if message.author.dm_channel == None:
            await message.author.create_dm()
        usersTeacherListTemp = CBU.getTeachers(message.author.roles)
        usersHWListTemp = []
        getFile('teachers.json')
        with open('teachers.json', 'r') as teachers_homework:
            teachersHomeworkDict = json.load(teachers_homework)
            for eachTeacher in usersTeacherListTemp:
                for eachTeacherFile in teachersHomeworkDict:
                    if eachTeacher.lower() == eachTeacherFile["name"]:
                        if len(eachTeacherFile["homework"]) != 0:
                            await message.author.dm_channel.send(embed = CBU.makeEmbedMessage2(eachTeacherFile["name"], eachTeacherFile["homework"]))
        await channel.send("You've been DM'ed a list of your Homework go check it")

    #add
    if header == f'{summon}add':
        if ("teacher:" not in theMessage or
            "title:" not in theMessage or
            "description:" not in theMessage or
            "due:" not in theMessage):
            await channel.send("incorrect usage of c!add command, use c!help to view usage")
        else:
            getFile('teachers.json')
            with open('teachers.json', 'r') as teachersList:
                teachersLista = json.load(teachersList)  
            sortThis = theMessage
            print(sortThis)
            indexTeacher = sortThis.index("teacher:")
            indexTitle = sortThis.index("title:")
            indexDescription = sortThis.index("description:")
            indexDueDate = sortThis.index("due:")
            if indexDueDate - indexDescription == 1:    #reference https://www.geeksforgeeks.org/python-list-insert/
                sortThis.insert(indexDueDate, "there is no description")
            indexDueDate = sortThis.index("due:")
            whereteacheris = 0 
            for eachTeacher in teachersLista:
                if sortThis[indexTeacher+1].lower() == eachTeacher["name"]:
                    addHomework = {
                            "title": formatname(' '.join(sortThis[(indexTitle+1):indexDescription])),
                            "description": formatname(' '.join(sortThis[(indexDescription+1):indexDueDate])),
                            "duedate": sortThis[-1]
                        }
                    for teacher in teachersLista:
                        if teacher["name"] == sortThis[indexTeacher + 1].lower():
                            teachersLista[teachersLista.index(teacher)]["homework"].append(addHomework)
                            break
                    break
            with open('teachers.json', 'w') as teachersList:
                json.dump(teachersLista, teachersList, indent=4)
            uploadFile('teachers.json')
            await channel.send("it has been added")  
    
    #remove
    if header == f'{summon}remove':
        theTeacher = theMessage[1].lower()
        theTitle = formatname(' '.join(theMessage[2:]))
        errorReason = ""
        getFile('teachers.json')
        with open('teachers.json', 'r') as teachers_List:
            teachersList = json.load(teachers_List)
        for teacher in teachersList:
            if teacher['name'] == theTeacher:
                teacherFound = True
                updatedHomework = teacher["homework"].copy()
                if len(updatedHomework):
                    for homework in updatedHomework:
                        if theTitle == homework["title"]:
                            updatedHomework.remove(homework)
                else:
                    errorReason = "there is no homework for this teacher"
                    await channel.send(f'Failed to delete homework because {errorReason}')
                    break
                if teacher["homework"] != updatedHomework:
                    await channel.send(f'Successfully deleted "{theTitle}" from {formatname(theTeacher)}')
                teacher["homework"] = updatedHomework
        with open('teachers.json', 'w') as teachers_List:
            teachers_List.seek(0)
            json.dump(teachersList, teachers_List, indent=4)
            teachers_List.truncate()
        uploadFile('teachers.json')
            
        
                    
    #view
    if header == f'{summon}view':
        if len(theMessage) != 2:
           await channel.send("format incorrect, use c!help to view proper usage")
        else:
            theTeacher = theMessage[1].lower()
            getFile('teachers.json')
            with open('teachers.json', 'r') as teachersLista:  #reference https://www.w3schools.com/python/python_file_open.asp
                teachersList = json.load(teachersLista)

            descriptionEmoji = ''
            """ if theTeacher in ['ton', 'villagomez', 'oliveira', 'kickham', 'yanez', 'thompson', 'stearns', 'lockett', 'gatewood', 'gadre']:
                descriptionEmoji = f':{theTeacher}:' """
                
            embedView = discord.Embed(title=f'{formatname(theMessage[1])} assignments', description = descriptionEmoji)

            homeworkList = ""
            for eachTeacher in teachersList:
                if eachTeacher["name"] == theTeacher:
                    if len(eachTeacher["homework"]) == 0 :
                        embedView.add_field(name = "Homework", value = f'There is no homework for {formatname(theTeacher)}, rejoice for you are free')
                    else:
                        for eachHomework in eachTeacher["homework"]:
                            embedView.add_field(name = f'**"{eachHomework["title"]}" due on {eachHomework["duedate"]}**', value = f"> {eachHomework['description']}", inline = False) 
    
        
            await channel.send(embed = embedView)
    
    #customdescription
    if header == f'{summon}description':
        descriptor = ' '.join(theMessage[1:])
        getFile('customDescription.json')
        with open('customDescription.json', 'r') as registeredNames:
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
        with open('customDescription.json', 'w') as registeredNames:
            registeredNames.seek(0)
            json.dump(replaceWith, registeredNames, indent = 4)
            registeredNames.truncate()
        uploadFile('customDescription')
        await channel.send("Your description has been updated!")
            
 #------------------------------------------------------
 # fun things            
    #erik
    if header == f'{summon}god':
        if isinstance(message.channel, discord.TextChannel):
            await channel.send("```so it seems that your server has erik jma, the so called god of salvation, the jesus- nobody knows what he really is quite frankly. it's the most amazing thing, everyone knew about erik jma for centuries except me. The moment I heard about it, the man the myth the legend, erik jma or erik juuumaaaa, that's our god. many people don't know that, but the moment I heard about this mythical creature i came a driving in my car, and it's an amazing car. I have better cars than anywhere in the world. Some say that newport has better cars but they don't, our cars are better.```")
        elif isinstance(message.channel, discord.DMChannel):
            await channel.send("So weird how if you invoke me here it's different than if you invoke me in the main discord.... weird indeed\nEvery line underneath this or even above this contains a clue. A small piece to the puzzle, and i'll just let you go solve it, but\nnot before making a very specific change in how i type, that will just, basically give it away.\nDon't think to hard about it though, I promise you it won't be that difficult.\nNow where was I? Oh right, we should be talking about our lord and savior Erik Jma. But um, i just remembered to tell you that\nu should probably be using a desktop to read this message, or it'll be hard to solve the puzzle. If you\ndo happen to be using a phone, I'm sorry to let you down. You might not get past this.\nEhhhh maybe not really, it's\nstill possible.")

    if header ==f'{summon}testing':
        await channel.send("c!testing")

    if header == f'{summon}ppsize':
        person = ' '.join(theMessage[1:])
        if theMessage[1:] == "me":
            person = message.author.nick
        ppdict = {1:"small", 2:"medium", 3:"large", 4:"massive", 5:"XTRA LARGE", 6:"the smallest thing you've ever seen", 7:"... what? you have a pp? couldn't tell...", 8:"tiny, 'it's laughable, really", 9:" MA S S I VE DIK EN E  R G Y", 10: "small, it's small, that's all there to say about it", 11: ":tanushtanush:", 12: "....HAHAHAH", 13:":Penetration:", 14:"average, i'll let you figure out which average", 15:"it's bigger than most, i'll give u that"}  
        ppchosen = random.randint(1,15)
        await channel.send(f"{person} has pp size {ppdict[ppchosen]}")

#------------------------------------------------------

#------------------------------------------------------
#gnap
    if message.author.name == "NapKat":
        getFile('settings.json')
        with open('settings.json', 'r') as settings_List:
            translated = []
            settingsList = json.load(settings_List)
            if settingsList["gnapToggle"] == "on":
                #gnapMessage = message.content.split('')
                getFile('gnap.json')
                with open('gnap.json', 'r') as gnap_List:
                    gnapList = json.load(gnap_List)
                    for word in theMessage:
                        foundword = False
                        for stupidWord in gnapList:
                            if stupidWord["word"] == word.lower():
                                translated.append(stupidWord["def"])
                                foundword = True
                                break
                        if foundword == False:
                                    translated.append(word)       
                if translated != theMessage:
                    embedGnap = discord.Embed(title = "GnapTranslator", description = "Translates wtf Gnap is saying")
                    embedGnap.add_field(name="Original language", value=message.content)
                    embedGnap.add_field(name="English translation", value=' '.join(translated))
                    await channel.send(embed=embedGnap) 
            #embedGnap.set_footer(text = "developed with python, by colin the sleep waster, waster of all sleep", icon_url="https://i.imgur.com/trIK0QD.jpg")
            
        
    if header == f'{summon}gnapadd':
        if (message.author.name == "Rez" or
            message.author.name == "NapKat"):
            addWord = theMessage[1]
            addDef = ' '.join(theMessage[2:])
            getFile('gnap.json')
            with open('gnap.json', 'r') as gnap_List:
                gnapList = json.load(gnap_List)
            if addWord in gnapList:
                await channel.send("You've already added this word")
                return
            gnapList[addWord] = addDef
            with open('gnap.json', 'w') as gnap_List:
                gnap_List.seek(0)
                json.dump(gnapList, gnap_List, indent = 4)
                gnap_List.truncate()
            uploadFile('gnap.json')
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
            getFile('settings.json')
            with open('settings.json', 'r+') as settings_List:
                settingsList = json.load(settings_List)
                if settingsList["gnapToggle"] == "on":
                    settingsList["gnapToggle"] = "off"
                else:
                    settingsList["gnapToggle"] = "on"
                json.dump(settingsList, settings_List, indent=4)
                await channel.send(f'_Gnap Translator has been set to `{settingsList["gnapToggle"]}`_')
            uploadFile('settings.json')
    
    if header == f'{summon}gt':
        translateThis = ' '.join(theMessage[1:])
        getFile('gnap.json')
        with open('gnap.json', 'r') as gnap_List:
            gnapList = json.load(gnap_List)
        for word in gnapList:
            if word == translateThis:
                await channel.send(f'{translateThis} = {gnapList[word]}')
                return

    if header == f'{summon}gtreverse':
        translateThis = ' '.join(theMessage[1:])
        print(translateThis)
        getFile('gnap.json')
        with open('gnap.json', 'r') as gnap_List:
            gnapList = json.load(gnap_List)
        for word in gnapList:
            if gnapList[word].lower() = translateThis.lower():
                await channel.send(f'{translateThis} = {word}')
                return

#------------------------------------------------------

    

#------------------------------------------------------
#puzzle

    if header == f'{summon}osaysgo':
        CBU.updatePuzzle(str(message.author.id), "stage 1")
        CBU.updatePuzzle(str(message.author.id), "completion")
        await channel.send("rmurtncxbnncqnvjwjpna")
    if header == f'{summon}karenroper':
        CBU.updatePuzzle(str(message.author.id), "stage 2")
        await channel.send("https://images2.imgbox.com/d1/73/1MmF73HB_o.jpg")
    if header == f'{summon}sendnudes':
        CBU.updatePuzzle(str(message.author.id), "stage 3")
        print(message.channel.type)
        if isinstance(message.channel, discord.DMChannel):
            await channel.send("ok well someone's dirty mInded, looking at the side text and all. fiNe, i'll give you what you want. It's the role right? Yeah I thought so. The command to get the role is c!-, wait, why am i even giving it to you this early. There's more. Of coURse there's more, you didn't think you were done yeT **haH**. We aren't.")
        else:
            await channel.send("bro i don't think, i don't think you're supposed to do that here...")
    if header == f'{summon}INIITOURTH':
        CBU.updatePuzzle(str(message.author.id), "stage 4")
        if isinstance(message.channel, discord.DMChannel):
            await channel.send("cool, so, you did that. I'm not surprised that you're still going. Here's one more scrambled mess and you're done ok? The key is 'bruh' 'tzelzfoaifonik'")
    if header == f'{summon}syt':
        CBU.updatePuzzle(str(message.author.id), "stage 5")
        if isinstance(message.channel, discord.DMChannel):
            await channel.send("fine, FINE, YOU'RE DONE. That's what you want isn't it? Good job, you did it. Go get your reward. You earned it.")
            await channel.send("just remember, you made it to the top, so you have the responsibility to not tell anyone the right commands ok? I'm watching, I know if you tell.")
            await channel.send("just use c!claim")
    if header == f'{summon}claim':
        if isinstance(message.channel, discord.TextChannel):
            with open('settings.json', 'r+') as settings_List:
                settingsList = json.load(settings_List)
                if settingsList["atTheTop"] < 3:
                    
                    with open('puzzleRegistry.json', 'r+') as puzzle_Registry:
                        puzzleRegistryDict = json.load(puzzle_Registry)
                        completion = False
                        alreadycomplete = False
                        for user in puzzleRegistryDict:
                            if user["id"] == str(message.author.id) and len(user) == 7 and user["completition"] != "completed":
                                completion = True
                                user["completition"] = "completed"
                                settingsList["atTheTop"] += 1

                            if user["completion"] == "completed":
                                alreadycomplete = True
                        if alreadycomplete == True:
                            await channel.send(f'you already got your reward ok')
                        elif completion == False:
                            await channel.send("you think you can just c!claim and be done with? no man, you have to do the other commands first u mega 5head")
                        elif completion == True:
                            await channel.send(f'{message.author.name} has reached the top and claimed the role of "Cipher Master" everyone give them a big round of applause or something')
                            guild = message.guild
                            await guild.create_role(name="Cipher Master", color=discord.Colour(0xFFDF00))
                            user = message.author
                            role = discord.utils.get(user.guild.roles, name="Cipher Master")
                            await user.add_roles(role)
                            print(message.author.name)
                        puzzle_Registry.seek(0)
                        json.dump(puzzleRegistryDict, puzzle_Registry, indent=4)
                        puzzle_Registry.truncate()
                else:
                    await channel.send("the hunt has ended, sorry mate but the first 3 have already reached the end :/")
                settings_List.seek(0)
                json.dump(settingsList, settings_List, indent=4)
                settings_List.truncate()

    if header == f'{summon}channelid':
        await channel.send(str(message.channel.id))

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