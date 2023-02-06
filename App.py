import PySimpleGUI as sg 
from GetData import GData

gdata = GData()
gdata.getRevisedMangaDataframe('themes')

# ----- Full layout -----
layout = [
    [sg.Text("Manga")],
    [sg.Btn(size=(10, 5), enable_events=True, key="-MANGA-")],
    [sg.Text(size=(40,1), key='-OUTPUT-', justification = 'center')],
    [sg.Image(size = (300,300), key = '-IMAGE-')]
]

window = sg.Window("Image Viewer", layout, element_justification='c')

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
window.close()

