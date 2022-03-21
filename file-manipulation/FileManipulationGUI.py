import os
import PySimpleGUI as sg
from PIL import Image


def resize(img_name, width, height, prefix, ext, new_name=None):
    img = Image.open(img_name)
    img = img.resize((width, height), Image.ANTIALIAS)
    img.save(prefix + '_' + new_name + '.' + ext)
    
def convert_img_type(img_name, prefix, to_ext):
    img = Image.open(img_name)
    converted_img = img.convert("RGB")
    converted_img.save(prefix + '.' + to_ext)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#~~~~ GUI CODE STARTS HERE ~~~~#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

sg.theme('DarkGrey14')


# Resize images window
def resize_imgs():
    resize_screen = [[sg.Text('Image Resizer', font=('Helvetica', 18), pad=(10, 10))],
                    [sg.In(size=(35, 1), enable_events=True, key="-FILES-"),sg.FilesBrowse('Choose image files')],
                    [sg.Listbox(values=[], size=(50, 10), key="-FILE LIST-")],
                    [sg.Text('Enter a suffix for the resized image (Optional):'), sg.In(size=(10, 1), key="-NEW NAME-")],
                    [sg.Text('Enter the desired width:'), sg.In(size=(10, 1), key="-WIDTH-")],
                    [sg.Text('Enter the desired height:'), sg.In(size=(10, 1), key="-HEIGHT-")],
                    [sg.Button('Resize', font=('Helvetica', 14), pad=(10, 10), button_color=('white', 'blue'), expand_x=True)]]

    resize_win = sg.Window('IMAGE RESIZE', layout=resize_screen, element_justification='center')

    while True:  
        event, values = resize_win.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-FILES-':
            files = values['-FILES-']
            file_list = files.split(';')
            resize_win['-FILE LIST-'].update(file_list)
        if event == 'Resize':
            width = int(values['-WIDTH-'])
            height = int(values['-HEIGHT-'])
            new_name = values['-NEW NAME-']
            for i in file_list:
                prefix = i.split('.')[0]
                ext = i.split('.')[1]
                resize(i, width, height, prefix, ext, new_name)
            sg.popup("SUCCESS", "Your images have been resized!", font=('Helvetica', 12))

    resize_win.close()


# Convert images window
def convert_imgs():
    convert_screen = [[sg.Text('Image Converter', font=('Helvetica', 18), pad=(10, 10))],
                      [sg.In(size=(35, 1), enable_events=True, key="-FILES-"),sg.FilesBrowse('Choose image files')],
                      [sg.Listbox(values=[], size=(50, 10), key="-FILE LIST-")],
                      [sg.Text('New File Type'), sg.Combo(('JPG', 'PNG', 'BMP'), size=(10, 1), key='-NEW TYPE-')],
                      [sg.Button('Convert', font=('Helvetica', 14), pad=(10, 10), button_color=('white', 'green'), expand_x=True)]]

    convert_win = sg.Window('IMAGE RESIZE', layout=convert_screen, element_justification='center')

    while True:
        event, values = convert_win.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-FILES-':
            files = values['-FILES-']
            file_list = files.split(';')
            convert_win['-FILE LIST-'].update(file_list)
        if event == 'Convert':
            for i in file_list:
                prefix = i.split('.')[0]
                prefix = prefix + str(values['-NEW TYPE-'])
                convert_img_type(i, prefix, values['-NEW TYPE-'])
            sg.popup('SUCCESS', 'Your images have been converted!', font=('Helvetica', 12))
        
    convert_win.close()


# Rename files window
def rename_files():
    rename_screen = [[sg.Text('Rename Files', font=('Helvetica', 18), pad=(10, 10))],
                    [sg.In(size=(35, 1), enable_events=True, key="-FOLDER-"),sg.FolderBrowse('Select folder')],
                    [sg.Listbox(values=[], size=(50, 10), key="-FILE LIST-")],
                    [sg.Text('Enter the extension of the files you wish to rename:')],
                    [sg.In(size=(10, 1), key="-EXTENSION-")],
                    [sg.Text('Enter the new prefix of the files:')],
                    [sg.In(size=(10, 1), key="-PREFIX-")],
                    [sg.Button('Rename', font=('Helvetica', 14), pad=(10, 10), button_color=('white', 'purple'), expand_x=True)]]

    rename_win = sg.Window('RENAMER', layout=rename_screen, element_justification='center')

    while True:  # Event Loop
        event, values = rename_win.read()
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
            rename_win["-FILE LIST-"].update(fnames)

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
            sg.popup("You've successfully renamed the files!", font=('Helvetica', 12))

    rename_win.close()


# Main menu window
def main():
    main_menu = [[sg.Text('Main Menu', font=('Helvetica', 30), justification='center')],
                [sg.HorizontalSeparator(p=(10,10))],
                [sg.Button('Resize', font=('Helvetica', 18), pad=(10, 10), key='-RESIZE-')], 
                [sg.Button('Convert', font=('Helvetica', 18), pad=(10, 10), key='-CONVERT-')],
                [sg.Button('Rename', font=('Helvetica', 18), pad=(10, 10), key='-RENAME-')]]
                

    main_win = sg.Window('FILE MANIPULATION', layout=main_menu, size=(300,300), element_justification='center')
    
    while True:
        event, values = main_win.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-RESIZE-':
            resize_imgs()
        if event == '-CONVERT-':
            convert_imgs()
        if event == '-RENAME-':
            rename_files()
    main_win.close()
    

main()