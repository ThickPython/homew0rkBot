import calendar
import discord
from devutil import *

client = discord.Client()

#viewme v2.0
async def hw(message):
    channel = message.channel
    the_message = message.content.split(' ')
    if message.author.dm_channel == None:
        await message.author.create_dm()
    usersTeacherListTemp = getTeachers(message.author.roles)
    homework_dict = get_file('teachers.json')
    oh_look_theres_homework = False
    for each_teacher in usersTeacherListTemp:
        for each_teacher_file in homework_dict:
            if each_teacher.lower() == each_teacher_file:
                if len(homework_dict[each_teacher_file]) != 0:
                    oh_look_theres_homework = True
                    await message.author.dm_channel.send(embed = makeEmbedMessage2(each_teacher_file, homework_dict[each_teacher_file]))
    if oh_look_theres_homework:
        await channel.send("You've been DM'ed a list of your Homework!")
    else:
        await channel.send("You have no homework! (disclaimer: at this time no one realy enters anything which means there is probably homework)")

async def add(message):
    channel = message.channel
    the_message = message.content.split(' ')
    if ("teacher:" not in the_message or
        "title:" not in the_message or
        "description:" not in the_message or
        "due:" not in the_message):
        await channel.send("incorrect usage of c!add command, use c!help to view usage")
    else:
        homework_dict = get_file('teachers.json')
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
        teacher_found = False
        for each_teacher in homework_dict:
            if sort_this[indexTeacher+1].lower() == each_teacher:
                teacher_found = True
                addHomework = {
                        "title": formatname(' '.join(sort_this[(indexTitle+1):indexDescription])),
                        "description": formatname(' '.join(sort_this[(indexDescription+1):indexDueDate])),
                        "duedate": sort_this[-1]
                    }
                for teacher in homework_dict:
                    if teacher == sort_this[indexTeacher + 1].lower():
                        homework_dict[teacher].append(addHomework)
                        break
                    
                await channel.send("it has been added") 
                break
        
        if teacher_found == False:
            await channel.send("We couldn't find that teacher, try again")
            return
        else:
            with open('teachers.json', 'w') as teachers_list_json:
                json.dump(homework_dict, teachers_list_json, indent=4)
            upload_file(homework_dict, 'teachers.json')  
    
    #remove
async def remove(message):
    channel = message.channel
    the_message = message.content.split(' ')
    the_teacher = the_message[1].lower()
    the_title = formatname(' '.join(the_message[2:]))
    errorReason = ""
    homework_list = get_file('teachers.json')
    teacher_found = False
    for teacher in homework_list:
        if teacher == the_teacher:
            teacher_found = True
            updatedHomework = homework_list[teacher].copy()
            if len(updatedHomework):
                for homework in updatedHomework:
                    if the_title == homework["title"]:
                        updatedHomework.remove(homework)
            else:
                errorReason = "there is no homework for this teacher"
                await channel.send(f'Failed to delete homework because {errorReason}')
                break
            if homework_list[teacher] != updatedHomework:
                await channel.send(f'Successfully deleted "{the_title}" from {the_teacher}')
            homework_list[teacher] = updatedHomework
    if teacher_found == False:
        await channel.send(f"We couldn't find `{the_teacher}`. Check your spelling and try again")
    with open('teachers.json', 'w') as teachers_list_json:
        teachers_list_json.seek(0)
        json.dump(homework_list, teachers_list_json, indent=4)
        teachers_list_json.truncate()
    upload_file(homework_list, 'teachers.json')
            
        
                    
    #view
async def view(message):
    channel = message.channel
    the_message = message.content.split(' ')
    if len(the_message) != 2:
        await channel.send("format incorrect, use c!help to view proper usage")
    else:
        the_teacher = the_message[1].lower()
        homework_list = get_file('teachers.json')
        print(homework_list)
        print(the_teacher)

        descriptionEmoji = ''
        """ if the_teacher in ['ton', 'villagomez', 'oliveira', 'kickham', 'yanez', 'thompson', 'stearns', 'lockett', 'gatewood', 'gadre']:
            descriptionEmoji = f':{the_teacher}:' """
            
        embed_view = discord.Embed(title=f'{the_message[1]} assignments', description = descriptionEmoji)

        return_homework_list = ""
        teacher_found = False
        for each_teacher in homework_list:
            if each_teacher == the_teacher:
                teacher_found = True
                if len(homework_list[each_teacher]) == 0 :
                    embed_view.add_field(name = "Homework", value = f'There is no homework for {the_teacher}')
                else:
                    for eachHomework in homework_list[each_teacher]:
                        embed_view.add_field(name = f'**"{eachHomework["title"]}" due on {eachHomework["duedate"]}**', value = f"> {eachHomework['description']}", inline = False) 
                break
        if teacher_found == True:
            await channel.send(embed = embed_view)
        elif teacher_found == False:
            await channel.send(f"`{the_teacher}` check your spelling and try again (If you're confident that this teacher exists, contact colin)")
            return

async def addteacher(message):
    teacher_list = get_file("teachers.json")

    teacher_to_add = message.content.split(' ')
    teacher_to_add.remove(teacher_to_add[0])
    teacher_to_add = ' '.join(teacher_to_add)

    if teacher_to_add in teacher_list:
        await message.channel.send("This teacher already exists!")
    else:
        teacher_list[teacher_to_add] = []
        await message.channel.send(f"Successfully added {teacher_to_add}!")
    upload_file(teacher_list, "teachers.json")

async def allteachers(message):
    teacher_list = get_file('teachers.json')

    embed_this = discord.Embed(title = "Teachers")
    list_of_teachers = ""
    for teacher in teacher_list:
        list_of_teachers += f"{formatname(teacher)}\n"
    embed_this.add_field(name = "list", value = list_of_teachers)

    await message.channel.send(embed = embed_this)

async def removeteacher(message):
    teacher_list = get_file("teachers.json")

    teacher_to_remove = message.content.split(' ')
    teacher_to_remove.remove(teacher_to_remove[0])
    teacher_to_remove = ' '.join(teacher_to_remove)

    if teacher_to_remove not in teacher_list:
        await message.channel.send("This teacher doesn't exist!")
    else:
        del(teacher_list[teacher_to_remove])
        await message.channel.send(f"Successfully removed {teacher_to_remove}!")
    upload_file(teacher_list, "teachers.json")