from datetime import datetime
from plyer import notification
import sys

datetime_default = datetime.now()

date = ''
time = ''
reminder_text = ''

if sys.argv > 1:
    date = sys.argv[1]
    time = sys.argv[2]
    reminder_text = sys.argv[3]
    print(date, time, reminder_text)

else:
    date = input('Enter date (YYYY-MM-DD): ')
    time = input('Enter time (HH:MM): ')
    reminder_text = input('Enter reminder text: ')

notification.notify(title = "REMEMBER TO", message = f"{reminder_text}", timeout = 10)
