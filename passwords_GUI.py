import random, string, os
import PySimpleGUI as sg

sg.theme('Black')

#pass_len = values[0]
pass_str = ''

layout = [[sg.Text('Either choose the length of the PW you wish to generate or enter your own PW.')], 
         [sg.Spin([8,9,10,11,12,13,14,15,16,17,18,19,20], key='-LEN-'), sg.Button('Generate Password')],
         [sg.In(key='-IN-', size=(10,20))],
         [sg.Text('Your password:'),sg.In(key='-PW-', size=(10,20)), sg.Text('What account is this for?'), sg.In(key='-ACC-', size=(10,20))],
         [sg.Button('Copy', key='-COPY-'), sg.Button('Save', key='-SAVE-')]]

window = sg.Window('PASSWORD GENERATOR', layout)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Generate Password':
        pass_letters = random.choices(string.ascii_letters, k=values['-LEN-']-4)
        pass_letters = ''.join(pass_letters)
        pass_dig = random.choices(string.digits, k=2)
        pass_dig = ''.join(pass_dig)
        pass_chars = random.choices(string.punctuation, k=2)
        pass_chars = ''.join(pass_chars)
        pass_str = pass_letters+str(pass_dig)+pass_chars
        window['-IN-'].update(pass_str)
    if event == '-COPY-':
        sg.clipboard_set(values['-IN-'])
    if event == '-SAVE-':
        directory=os.getcwd()
        f = open(directory+'/passwords.txt', 'a')
        if values['-IN-'] == '':
            f.write(values['-ACC-']+'\t'+ values['-PW-']+'\n')
        else:
            f.write(values['-ACC-']+'\t'+values['-IN-']+'\n')
        f.close()
        sg.popup('Password saved!')

window.close()