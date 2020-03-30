import json
import discord

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
    embedThis = discord.Embed(title = user.nick, description = descriptionThis)
    for eachHomework in homeworkDict:
        addValue = " "
        for eachIndivHW in eachHomework["homework"]:
            addValue += f"\n{eachIndivHW['description']} due on {eachIndivHW['duedate']}"
        embedThis.add_field(name = formatname(eachHomework["teacher"]), value = addValue, inline = False)
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
        json.dump(usersListList, usersList, indent = 4)