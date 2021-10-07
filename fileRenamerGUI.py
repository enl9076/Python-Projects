import os
import PySimpleGUI as sg

sg.theme('DarkAmber')

layout = [[sg.Text('Rename Some Files')],
          [sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),sg.FolderBrowse('Select folder')],
          [sg.Listbox(values=[], size=(40, 20), key="-FILE LIST-")],
          [sg.Text('Enter the extension of the files you wish to rename:')],
          [sg.In(size=(10, 1), key="-EXTENSION-")],
          [sg.Text('Enter the new prefix of the files:')],
          [sg.In(size=(10, 1), key="-PREFIX-")],
          [sg.Button('Rename')]]

window = sg.Window('RENAMER', layout=layout)

while True:  # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == '-FOLDER-':
        folder = values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
        ]
        window["-FILE LIST-"].update(fnames)

    if event == 'Rename':
        folder = values["-FOLDER-"]
        extension = values["-EXTENSION-"]
        prefix = values["-PREFIX-"]
        i =0 
        file_list = os.listdir(folder)
        for f in file_list:
            if f.endswith(extension):
                    new = prefix + str(i) + extension
                    source = folder +'/'+ f
                    new = folder +'/'+ new
                    os.rename(source, new)
                    i += 1
        sg.popup("You've successfully renamed the files!")

window.close()

    
