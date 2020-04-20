import json
import discord
import boto3
import os
from datetime import datetime

S3_BUCKET = os.environ['S3_BUCKET']


s3 = boto3.client('s3', aws_access_key_id=os.environ['CLOUDCUBE_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['CLOUDCUBE_SECRET_ACCESS_KEY'])


def get_file(filename):
    s3.download_file(S3_BUCKET, f'jbmhhy234xp5/public/{filename}', f'{filename}')

def upload_file(filename):
    s3.upload_file(f'{filename}', S3_BUCKET, f'jbmhhy234xp5/public/{filename}')

def formatname(name):
    splitname = list(str(name))  #reference https://www.w3schools.com/python/ref_string_split.asp
    fixedname = [splitname[0].upper()]
    for eachLetter in splitname[1:]:
        fixedname.append(eachLetter.lower())
    return str(''.join(fixedname))

def getTeachers(RolesList):

    teachers = []
    for eachRole in RolesList:
        get_file('teachers.json')
        with open('teachers.json', 'r') as teachersList:
            teachersListDict = json.load(teachersList)
            for eachTeacher in teachersListDict:
                if str(eachRole.name).lower() == eachTeacher["name"]:
                    teachers.append(str(eachRole))
                teachers.append("ee")

    return(teachers)



def makeEmbedMessage(user, userTeachers, homeworkDict):                             #reference https://discordjs.guide/popular-topics/embeds.html#embed-preview
    descriptionThis = ""                                                            #reference api https://discordpy.readthedocs.io/en/latest/api.html#embed
    get_file('customDescription.json')
    with open('customDescription.json', 'r') as customDescription:
        readHere = json.load(customDescription)
        for eachDescription in readHere:
            if eachDescription["discord id"] == user.id:
                descriptionThis = eachDescription["descriptor"]
    embedThis = discord.Embed(title=user.nick, description=f'{descriptionThis}')
    
    for eachHomework in homeworkDict:
        addValue = " "
        for eachIndivHW in eachHomework["homework"]:
            addValue += f"\n__'{eachIndivHW['title']}' due on **{eachIndivHW['duedate']}**__\n> Description: {eachIndivHW['description']} "
        embedThis.add_field(name = f'`{formatname(eachHomework["teacher"])}`', value = addValue, inline = False)
    embedThis.set_thumbnail(url = user.avatar_url)
    #embedThis.set_footer(text = "developed with python", icon_url="https://i.imgur.com/trIK0QD.jpg")
    return(embedThis)

def makeEmbedMessage2(teacher, homeworkDict):
    embedThis = discord.Embed(title=teacher, description = "")
    addValue = ""
    for eachHomework in homeworkDict:
        addValue += f"\n__'{eachHomework['title']}' due on **{eachHomework['duedate']}**__\n> Description: {eachHomework['description']} "
    embedThis.add_field(name = 'homework', value = addValue)
    return(embedThis)


def addMember(userId, userRoles):
    addUser = {"discord id":userId}
    userRolesClean = []
    addUserRoles = []
    for eachRole in userRoles:
        userRolesClean.append(str(eachRole))
    teachersList = open('teachers.json', 'r')
    teachersListDict = json.load(teachersList)
    for eachRole in userRolesClean:
        for eachTeacher in teachersListDict:
            if eachRole.lower() == eachTeacher["name"]:
                addUserRoles.append(eachRole.lower())
    addUser["teachers"] = addUserRoles
    teachersList.close()
    open
    with open('users.json', 'r+')  as usersList:
        usersListList = json.load(usersList)
        usersListList.append(addUser)
        usersList.seek(0)
        json.dump(usersListList, usersList, indent=4)

def updatePuzzle(user, stage):
    currentStage = stage
    with open('puzzleRegistry.json', 'r+') as puzzle_Registry:
        puzzleRegistryDict = json.load(puzzle_Registry)
        alreadyRegistered = False
        for users in puzzleRegistryDict:
            if users["id"] == user:
                alreadyRegistered = True
                users[currentStage] = "complete"
        if alreadyRegistered == False:
            puzzleRegistryDict.append({
                "id": user,
                stage: "complete"
            })
        puzzle_Registry.seek(0)
        json.dump(puzzleRegistryDict, puzzle_Registry, indent = 4)
        puzzle_Registry.truncate()

""" def log(logThis):
    with open("log.txt", 'w') as log:
        log. """

#{"title": "Covid chronicles", "description": "Check onenote content library > covid chronicles and follow instructions", "duedate": "4/6"}

print("TTCBU is up and running!")