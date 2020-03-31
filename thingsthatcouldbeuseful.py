import json
import discord
from datetime import datetime

def formatname(name):
    print(f"format name has been called with {name}")
    splitname = list(str(name))  #reference https://www.w3schools.com/python/ref_string_split.asp
    fixedname = [splitname[0].upper()]
    for eachLetter in splitname[1:]:
        fixedname.append(eachLetter.lower())
    return str(''.join(fixedname))

def getTeachers(RolesList):

    teachers = []
    for eachRole in RolesList:
        with open('teachers.json', 'r') as teachersList:
            teachersListDict = json.load(teachersList)
            for eachTeacher in teachersListDict:
                if str(eachRole.name).lower() == eachTeacher["name"]:
                    teachers.append(str(eachRole))
    return(teachers)



def makeEmbedMessage(user, userTeachers, homeworkDict):                             #reference https://discordjs.guide/popular-topics/embeds.html#embed-preview
    descriptionThis = ""                                                            #reference api https://discordpy.readthedocs.io/en/latest/api.html#embed
    with open('customDescription.json', 'r') as customDescription:
        readHere = json.load(customDescription)
        for eachDescription in readHere:
            if eachDescription["discord id"] == user.id:
                descriptionThis = eachDescription["descriptor"]
    embedThis = discord.Embed(title=user.nick, description=f'> {descriptionThis}')
    
    for eachHomework in homeworkDict:
        addValue = " "
        for eachIndivHW in eachHomework["homework"]:
            addValue += f"\n__'{eachIndivHW['title']}' due on **{eachIndivHW['duedate']}**__\n> Description: {eachIndivHW['description']} "
        embedThis.add_field(name = f'-----------\n`{formatname(eachHomework["teacher"])}`', value = addValue, inline = False)
    embedThis.set_thumbnail(url = user.avatar_url)
    embedThis.set_footer(text = "developed with python", icon_url="https://i.imgur.com/trIK0QD.jpg")
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
    with open('users.json', 'r+')  as usersList:
        usersListList = json.load(usersList)
        usersListList.append(addUser)
        usersList.seek(0)
        json.dump(usersListList, usersList, indent=4)
        
def deleteOld():
    with open('teachers.json', 'r+') as teacherList:
        teacherListDict = json.load(teacherList)
        todayIs = datetime.today()
        for teacher in teacherListDict:
            updatedHomework = teacher["homework"].copy()
            for homework in updatedHomework:
                homeworkDueDate = homework["duedate"].split("/")
                if int(todayIs.day) > int(homeworkDueDate[1]) and int(todayIs.month) > int(homeworkDueDate[0]):
                    print(f'removing {homework}')
                    updatedHomework.remove(homework)
                elif int(todayIs.day) < int(homeworkDueDate[1]) and int(todayIs.month) > int(homeworkDueDate[0]):
                    print(f'removing {homework}')
                    updatedHomework.remove(homework)
                elif int(todayIs.day) > int(homeworkDueDate[1]) and int(todayIs.month) > int(homeworkDueDate[0]):
                    print(f'removing {homework}')
                    updatedHomework.remove(homework)
            teacher["homework"] = updatedHomework
        teacherList.seek(0)
        json.dump(teacherListDict, teacherList, indent=4)
        teacherList.truncate()

#{"title": "Covid chronicles", "description": "Check onenote content library > covid chronicles and follow instructions", "duedate": "4/6"}
deleteOld()