import random, string, os
import PySimpleGUI as sg
from cryptography.fernet import Fernet

def generate_password(length):
    """ Function that takes in one parameter - length - to generate a strong password """
    pass_elements = random.choices(string.ascii_letters, k=length-4) + random.choices(string.digits, k=2) + random.choices(string.punctuation, k=2)
    return ''.join(random.sample(pass_elements, len(pass_elements)))

sg.theme('Black')

def popup_window():
    """ Create the main menu for user to choose desired option """
    layout = [
        [sg.Text('Password Manager', justification='center', font=("Helvetica", 20))],
        [sg.Text('Choose an option below:', justification='center', font=("Helvetica", 16))],
        [sg.Button('Generate Password', font=("Helvetica", 14), button_color=('white', 'green')), 
         sg.Button('Add Password', font=("Helvetica", 14), button_color=('white', 'green'))],
        [sg.Button('View All Passwords', font=("Helvetica", 14), button_color=('white', 'green'))]
    ]

    window = sg.Window('Password Manager', layout, element_justification='center')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Generate Password':
            generate_window()
        elif event == 'Add Password':
            add_window()
        elif event == 'View All Passwords':
            view_passwords()

    window.close()

pass_str = ''

def generate_window():
    """ Create the window that will allow the user to generate a random password """
    layout1 = [
         [sg.Text('Password Manager', font=('Helvetica', 14))], 
         [sg.Spin([i for i in range(8,20)], key='-LEN-'), sg.Button('Generate Password')],
         [sg.In(key='-IN-', size=(10,20))],
         [sg.Text('Account Name: ', font=('Helvetica', 12)), sg.In(key='-ACC-', size=(10,20)),
          sg.Text('Username:', font=('Helvetica', 12)),sg.In(key='-USR-', size=(10,20))],
         [sg.Button('Copy Password', key='-COPY-'), sg.Button('Save Only', key='-SAVE-'), sg.Button('Save & Encrypt', key='-ENC-')],
         [sg.Checkbox('Show All Passwords', key='-SHOW-', enable_events=True)],
         [sg.Button('Back to Main Menu', key='-BACK-', button_color=('white', 'blue'))]
         ]
    win1=sg.Window('Password Manager', layout1, element_justification='center')

    while True:
        event, values = win1.read()
        if event == sg.WIN_CLOSED or event == '-BACK-':
            break
        if event == 'Generate Password':
            pass_str = generate_password(int(values['-LEN-']))
            win1['-IN-'].update(pass_str)
        if event == '-COPY-':
            sg.clipboard_set(values['-IN-'])
            sg.popup('Copied!')
        if event == '-SAVE-':
            directory=os.getcwd()
            f = open(directory+'/passwords.txt', 'a')
            f.write(values['-ACC-']+'\t'+ values['-USR-'] +'\t'+ values['-IN-']+'\n')
            f.close()
            sg.popup('Password saved!')
        if event == '-ENC-':
            if 'keyfile.key' in os.listdir():
                with open('keyfile.key', 'rb') as unlock:
                    key = unlock.read()
                f = Fernet(key)
            else:
                key = Fernet.generate_key()
                f = Fernet(key)
                with open('keyfile.key', 'wb') as keyfile:
                    keyfile.write(key)
            with open(os.getcwd()+'/sensitive-passwords.txt', 'a') as f:
                new_pass = values['-ACC-']+'\t'+ values['-USR-'] +'\t'+ values['-IN-']+'\n'
                f.write(f.encrypt(new_pass.encode()))
                f.close()
        if values['-SHOW-']==True:
            directory=os.getcwd()
            f = open(directory+'\passwords.txt', 'r')
            contents = f.readlines()
            for i in contents:
                acc, usr, passw = i.split('\t')
                sg.Print("Account: " + acc + " | " + "Username: " + usr + " | " + "Password: " + passw)
    win1.close()

def add_window():
    """ Create the window that will allow the user to add their own passwords """
    layout2 = [
         [sg.Text('Password Manager', font=('Helvetica', 14))], 
         [sg.Text('Account Name: ', font=('Helvetica', 12)), sg.In(key='-ACC-', size=(10,20))],
         [sg.Text('Username:', font=('Helvetica', 12)),sg.In(key='-USR-', size=(10,20)), 
          sg.Text('Password:', font=('Helvetica', 12)),sg.In(key='-PW-', size=(10,20))],
         [sg.Button('Save', key='-SAVE-'), sg.Checkbox('Show All Passwords', key='-SHOW-', enable_events=True)],
         [sg.Button('Back to Main Menu', key='-BACK-', button_color=('white', 'blue'))]
         ]
    win2=sg.Window('Password Manager', layout2, element_justification='center')
    while True:
        event, values = win2.read()
        if event == sg.WIN_CLOSED or event == '-BACK-':
            break
        if event == '-SAVE-':
            directory=os.getcwd()
            f = open(directory+'/passwords.txt', 'a')
            f.write(values['-ACC-']+'\t'+ values['-USR-'] +'\t'+ values['-PW-']+'\n')
            f.close()
            sg.popup('Password saved!')
        if values['-SHOW-']==True:
            directory=os.getcwd()
            f = open(directory+'\passwords.txt', 'r')
            contents = f.readlines()
            for i in contents:
                acc, usr, passw = i.split('\t\t')
                sg.Print("Account: " + acc + " | " + "Username: " + usr + " | " + "Password: " + passw)
    
    win2.close()

def view_passwords():
    """ Create window that will allow the user to see all current saved passwords """
    layout = [[sg.Text('Password Manager', font=('Helvetica', 14))],
              [sg.Text('Search by Account or Username'), 
               sg.InputText(size=(10, 1), key='-SEARCHTERMS-'), sg.Button('Search', key='-SEARCH-')],
              [sg.Checkbox('Show All', enable_events=True, key='-SHOW-')],
              [sg.Text('', key='-OUTPUT-', auto_size_text=True)]]
    
    win3=sg.Window('Password Manager', layout, element_justification='center', size=(550,400))
    while True:
        event, values = win3.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == '-SEARCH-' and values['-SEARCHTERMS-'] != '':
            directory=os.getcwd()
            f = open(directory+'\passwords.txt', 'r')
            contents = f.readlines()
            for line in contents:
                if line.find(values['-SEARCHTERMS-'])==True:
                    sg.Print(line)
            win3['-OUTPUT-'].update(contents)
        if values['-SHOW-']==True:
            directory=os.getcwd()
            f = open(directory+'/passwords.txt', 'r')
            contents = f.read()
            win3['-OUTPUT-'].update(contents)
    win3.close()

popup_window()