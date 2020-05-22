import time
import json
from datetime import datetime
from devutil import *

starttime=time.time()

def deleteOld():
    teacher_list = get_file('teachers.json')
    todayIs = datetime.today()
    for teacher in teacher_list:
        updated_hw = teacher_list[teacher].copy()
        for homework in updated_hw:
            homeworkDueDate = homework["duedate"].split("/")
            if int(todayIs.day) > int(homeworkDueDate[1]) and int(todayIs.month) >= int(homeworkDueDate[0]):
                print(f'removing {homework}')
                updated_hw.remove(homework)
            elif int(todayIs.day) <= int(homeworkDueDate[1]) and int(todayIs.month) > int(homeworkDueDate[0]):
                print(f'removing {homework}')
                updated_hw.remove(homework)
            elif int(todayIs.day) > int(homeworkDueDate[1]) and int(todayIs.month) > int(homeworkDueDate[0]):
                print(f'removing {homework}')
                updated_hw.remove(homework)
        teacher_list[teacher] = updated_hw
    upload_file(teacher_list, 'teachers.json')

print("cleaner is up and running!")

while True:
    print("CLEANING TIMEEEEEEEEEEEEEEEEEEEEEE")
    deleteOld()
    time.sleep(86400)