import json
import discord
import boto3
import os
from datetime import datetime

#S3_BUCKET = os.environ['S3_BUCKET']
S3_BUCKET = "cloud-cube"

client = discord.Client()

s3 = boto3.client('s3', aws_access_key_id=os.environ['CLOUDCUBE_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['CLOUDCUBE_SECRET_ACCESS_KEY'])

def get_file(filename):
    s3.download_file(S3_BUCKET, f'jbmhhy234xp5/public/{filename}', f'{filename}')
    with open(filename, 'r') as filenameAsJson:
        return json.load(filenameAsJson)

def upload_file(savethis, filename):
    with open(filename, 'w') as filenameAsJson:
        json.dump(savethis, filenameAsJson, indent = 4)
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
                if str(eachRole.name).lower() == eachTeacher:
                    teachers.append(str(eachRole))
                teachers.append("ee")

    return(teachers)



def makeEmbedMessage(user, userTeachers, homework_dict):                             #reference https://discordjs.guide/popular-topics/embeds.html#embed-preview
    descriptionThis = ""                                                            #reference api https://discordpy.readthedocs.io/en/latest/api.html#embed
    get_file('customDescription.json')
    with open('customDescription.json', 'r') as customDescription:
        readHere = json.load(customDescription)
        for eachDescription in readHere:
            if eachDescription["discord id"] == user.id:
                descriptionThis = eachDescription["descriptor"]
    embed_this = discord.Embed(title=user.nick, description=f'{descriptionThis}')
    
    for each_homework in homework_dict:
        add_value = " "
        for eachIndivHW in homework_dict[each_homework]:
            add_value += f"\n__'{eachIndivHW['title']}' due on **{eachIndivHW['duedate']}**__\n> Description: {eachIndivHW['description']} "
        embed_this.add_field(name = f'`{formatname(each_homework["teacher"])}`', value = add_value, inline = False)
    embed_this.set_thumbnail(url = user.avatar_url)
    #embed_this.set_footer(text = "developed with python", icon_url="https://i.imgur.com/trIK0QD.jpg")
    return(embed_this)

def makeEmbedMessage2(teacher, homework_dict):
    embed_this = discord.Embed(title=teacher, description = "")
    add_value = ""
    for each_homework in homework_dict:
        embed_this.add_field(name = f"'{each_homework['title']}' due on **{each_homework['duedate']}**", value = f"Description: {each_homework['description']}")
    return(embed_this)


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
            if eachRole.lower() == eachTeacher:
                addUserRoles.append(eachRole.lower())
    addUser["teachers"] = addUserRoles
    teachersList.close()
    open
    with open('users.json', 'r+')  as usersList:
        usersListList = json.load(usersList)
        usersListList.append(addUser)
        usersList.seek(0)
        json.dump(usersListList, usersList, indent=4)


""" def log(logThis):
    with open("log.txt", 'w') as log:
        log. """

#{"title": "Covid chronicles", "description": "Check onenote content library > covid chronicles and follow instructions", "duedate": "4/6"}

print("TTCBU is up and running!")