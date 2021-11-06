from datetime import datetime
from plyer import notification
import PySimpleGUI as gui

datetime_default = datetime.now()

date = ''
time = ''
reminder_text = ''


notification.notify(title = "REMEMBER TO", message = f"{reminder_text}", timeout = 10)
