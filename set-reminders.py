from datetime import datetime
from plyer import notification
#import PySimpleGUI as gui
import sys

current_date = datetime.now()

date = ''
reminder_text = ''

def set_reminder():
    '''Takes user input and saves it as a txt file'''
    date = input("Enter date in format YYYY-MM-DD: ")
    reminder_text = input("Enter reminder: ")
    with open('reminders.txt', 'a') as f:
        f.write(f"\n{date}|{reminder_text}\n")
    return date, reminder_text


def check_for_reminders():
    '''Check the "reminders.txt" doc for any reminders occurring today'''
    with open('reminders.txt', 'r') as f:
        reminders = f.readlines()
        reminders = [reminder.split("|") for reminder in reminders]
        date = datetime.strptime(reminders[0][0], "%Y-%m-%d")
    if current_date.date() == date.date():
        send_notification()
    else:
        pass

def send_notification():
    with open('reminders.txt', 'r') as f:
        reminders = f.readlines()
        reminders = [reminder.split("|") for reminder in reminders]
        reminder_text = reminders[0][1]
    notification.notify(title = "REMEMBER TO", 
                        message = f"{reminder_text}", 
                        timeout = 10)

set_reminder()
check_for_reminders()