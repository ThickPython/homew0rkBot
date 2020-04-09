import time
import json
from datetime import datetime
from thingsthatcouldbeuseful import getFile, uploadFile

starttime=time.time()

def deleteOld():
    getFile('teachers.json')
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
    uploadFile('teachers.json')

print("cleaner is up and running!")

while True:
  deleteOld()
  time.sleep(86400)