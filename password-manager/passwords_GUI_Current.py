import random, string, os, json
import PySimpleGUI as sg
import nltk
from nltk.corpus import wordnet

passwords = dict()
pass_str = ''
dividers = '!@#$%^&*_+=-/<>?|~'


def generate_password(length):
    pass_elements = random.choices(string.ascii_letters, k=length-4) + random.choices(string.digits, k=2) + random.choices(string.punctuation, k=2)
    return ''.join(random.sample(pass_elements, len(pass_elements)))

def get_custom_password():
    city = sg.PopupGetText("What city or country do you most want to visit?")
    animal = sg.PopupGetText("What is your favorite animal?")
    date = sg.PopupGetText("Enter a date that is significant to you. Include only numbers.")    
        
    animal_synonym = random.choice(wordnet.synsets(animal)) 
    animal_lems = animal_synonym.lemmas()
    animal_names = []
    for lem in animal_lems:
        animal_names.append(lem.name())
        
    city_synonym = random.choice(wordnet.synsets(city)) 
    city_lems = city_synonym.lemmas()
    city_names = []
    for lem in city_lems:
        city_names.append(lem.name())
        
    password = str(random.choice(animal_names))+str(random.choice(dividers))+str(random.choice(city_names))+date
    return password


#~~~~~~~ Set the theme aesthetic ~~~~~~~#
sg.theme('Black')


#~~~~~~~ Create the user windows ~~~~~~~#
def popup_window():
    """ The main menu where user chooses to generate a password, add their own password, or view saved passwords. """
    layout = [
        [sg.Text('Password Manager', justification='center', font=("Helvetica", 20))],
        [sg.Text('Choose an option below:', justification='center', font=("Helvetica", 16))],
        [sg.Button('Generate Password', font=("Helvetica", 14), button_color=('white', 'green')), 
         sg.Button('Add Password', font=("Helvetica", 14), button_color=('white', 'green'))],
        [sg.Button('View Passwords', font=("Helvetica", 14), button_color=('white', 'green'))]
    ]

    window = sg.Window('Password Manager', layout, element_justification='center')

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Generate Password':
            window.close()
            generate_window()
        elif event == 'Add Password':
            window.close()
            add_window()
        elif event == 'View Passwords':
            window.close()
            view_passwords()

    window.close()


def generate_window():
    """ This window enables the user to generate a random, strong password. Options to personalize or completely randomize. """
    layout1 = [
         [sg.Text('Password Manager', font=('Helvetica', 16))], 
         [sg.Text('Personalize your password with the button below', font=('Helvetica', 12))],
         [sg.Button('Generate Custom Password', font=('Helvetica', 12), button_color=('white', 'blue'), key='-CUSTOM-')],
         [sg.Text('Or enter the desired length of your new password and click the button for a random one.', font=('Helvetica', 12))],
         [sg.Spin([i for i in range(8,20)], font=('Helvetica', 12), key='-LEN-'), sg.Button('Generate Random Password', font=('Helvetica', 12),button_color=('black', 'lightblue'))],
         [sg.HorizontalSeparator(pad=(0,15))],
         [sg.In(key='-IN-', size=(30,20))],
         [sg.Text('Account Name: ', font=('Helvetica', 12)), sg.In(key='-ACC-', size=(10,20)),
          sg.Text('Username:', font=('Helvetica', 12)),sg.In(key='-USR-', size=(10,20))],
         [sg.Button('Copy Password', key='-COPY-'), sg.Button('Save', key='-SAVE-')],
         [sg.Button('Back to Main Menu', key='-BACK-', button_color=('white', 'blue'))]
    ]
    
    win1=sg.Window('Password Manager', layout1, element_justification='center')

    while True:
        event, values = win1.read()
        if event == sg.WIN_CLOSED:
            break
        
        if event == '-BACK-':
            win1.close()
            popup_window()
            
        if event == '-CUSTOM-':
            password=get_custom_password()
            win1['-IN-'].update(password)
            
        if event == 'Generate Password':
            pass_str = generate_password(int(values['-LEN-']))
            win1['-IN-'].update(pass_str)
            
        if event == '-COPY-':
            sg.clipboard_set(values['-IN-'])
            sg.popup('Copied!')
            
        if event == '-SAVE-':
            directory=os.getcwd()
            with open(f'{directory}/passwords.json', 'r') as f:
                content = json.load(f)
                content.update({values['-ACC-']: (values['-USR-'], values['-IN-'])})
            with open(f'{directory}/passwords.json', 'w') as f:
                json.dump(content, f)
            sg.popup('Password saved!')

    win1.close()


def add_window():
    """ This window enables the user to add their own password to saved passwords.json file. """
    layout2 = [
         [sg.Text('Password Manager', font=('Helvetica', 14))], 
         [sg.Text('Account Name: ', font=('Helvetica', 12)), sg.In(key='-ACC-', size=(10,20))],
         [sg.Text('Username:', font=('Helvetica', 12)),sg.In(key='-USR-', size=(10,20)), 
          sg.Text('Password:', font=('Helvetica', 12)),sg.In(key='-PW-', size=(10,20))],
         [sg.Button('Save', key='-SAVE-')],
         [sg.Button('Back to Main Menu', key='-BACK-', button_color=('white', 'blue'))]
         ]
    
    win2=sg.Window('Password Manager', layout2, element_justification='center')
    
    while True:
        event, values = win2.read()
        if event == sg.WIN_CLOSED:
            break
        
        if event == '-BACK-':
            win2.close()
            popup_window()
            
        if event == '-SAVE-':
            directory=os.getcwd()
            try:
                with open(f'{directory}/passwords.json', 'r') as f:
                    content = json.load(f)
                    content.update({values['-ACC-']: (values['-USR-'], values['-PW-'])})
            except FileNotFoundError:
                with open(f'{directory}/passwords.json', 'a') as f:
                    content = {values['-ACC-']: (values['-USR-'], values['-PW-'])}
                    json.dump(content, f)
                
            with open(f'{directory}/passwords.json', 'w') as f:
                json.dump(content, f)
            sg.popup('Password saved!')

    win2.close()


def view_passwords():
    """ This window allows the user to either search for a specific saved password or view all saved passwords. """
    layout = [[sg.Text('Password Manager', font=('Helvetica', 14))],
              [sg.Text('Search by Account or Username'), 
               sg.InputText(size=(10, 1), key='-SEARCHTERMS-'), sg.Button('Search', key='-SEARCH-')],
              [sg.Checkbox('Show All', enable_events=True, key='-SHOW-')],
              [sg.Output(size=(50,10), key='-OUTPUT-', pad=(0,20))],
              [sg.Button('Back to Main Menu', key='-BACK-', button_color=('white', 'blue'), pad=((0,0),(20,5)))]]
    
    win3=sg.Window('Password Manager', layout, element_justification='center', size=(500,400))
    
    while True:
        event, values = win3.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        
        if event == '-BACK-':
            win3.close()
            popup_window()
            
        if event == '-SEARCH-' and values['-SEARCHTERMS-'] != '':
            win3['-OUTPUT-'].update('')
            directory = os.getcwd()
            try:
                with open(f'{directory}/passwords.json', 'r') as f:
                    contents = json.load(f)
                    if values['-SEARCHTERMS-'] in contents.keys():
                        win3['-OUTPUT-'].update(f'Account Name: {values["-SEARCHTERMS-"]}\nUsername: {contents[values["-SEARCHTERMS-"]][0]}\nPassword: {contents[values["-SEARCHTERMS-"]][1]}')
                    else:
                        sg.popup('Account not found!')
            except FileNotFoundError:
                sg.popup('No passwords saved!')
        
        if values['-SHOW-']:
            win3['-OUTPUT-'].update('')
            directory = os.getcwd()
            try:
                with open(f'{directory}/passwords.json', 'r') as f:
                    contents = json.load(f)
                    for key in contents.keys():
                        print(f'Account Name: {key}\nUsername: {contents[key][0]}\tPassword: {contents[key][1]}\n\n')
            except FileNotFoundError:
                sg.popup('No passwords saved!')
        if values['-SHOW-']==False and values['-SEARCHTERMS-'] == '':
            win3['-OUTPUT-'].update('')
    
    win3.close()


#~~~~~~~ Begin the program ~~~~~~~#
popup_window()