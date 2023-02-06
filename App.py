import PySimpleGUI as sg 
from GetData import GData

gdata = GData()
gdata.getRevisedMangaDataframe('themes')

rating_buttons = [
    [
        sg.Btn(size=(10, 5), enable_events=True, key="-DISLIKE-", button_color = 'white on red', button_text= 'Dislike'),
        sg.Btn(size=(10, 5), enable_events=True, key="-MANGA-", button_color = 'white on black', button_text = 'Get Manga'),
        sg.Btn(size=(10, 5), enable_events=True, key="-LIKE-", button_color = 'white on green', button_text = 'Like')
    ]
]

# ----- Full layout -----
layout = [
    [sg.Text(size=(40,1), key='-OUTPUT-', justification = 'center', font = ("Arial", 20))],
    [sg.Image(size = (300,300), key = '-IMAGE-')],
    rating_buttons
]

window = sg.Window("Image Viewer", layout, element_justification='c')

like_list = []
dislike_list = []

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == '-MANGA-':
        mal_id = gdata.getRandomMalID()
        manga = gdata.getManga(mal_id)
        title = manga.title
        window['-OUTPUT-'].update(title)
        image = gdata.getImage(manga)
        window['-IMAGE-'].update(image)
    if event == '-LIKE-':
        like_list.append(manga.title)
    if event == '-DISLIKE-':
        dislike_list.append(manga.title)
window.close()

