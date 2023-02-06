import PySimpleGUI as sg 
from GetData import GData


class App:

    def __init__(self, user):
        self.gdata = user.mdata.gdata
    
    def setup(self):
        self.rating_buttons = [
            [
                sg.Btn(size=(10, 5), enable_events=True, key="-DISLIKE-", button_color = 'white on red', button_text= 'Dislike'),
                sg.Btn(size=(10, 5), enable_events=True, key="-MANGA-", button_color = 'white on black', button_text = 'Get Manga'),
                sg.Btn(size=(10, 5), enable_events=True, key="-LIKE-", button_color = 'white on green', button_text = 'Like')
            ]
        ]

        # ----- Full layout -----
        self.layout = [
            [sg.Text(size=(40,1), key='-OUTPUT-', justification = 'center', font = ("Arial", 20))],
            [sg.Image(size = (300,300), key = '-IMAGE-')],
            self.rating_buttons
        ]

    def getManga(self, window):
        mal_id = self.gdata.getRandomMalID()
        manga = self.gdata.getManga(mal_id)
        title = manga.title
        image = self.gdata.getImage(manga)
        window['-OUTPUT-'].update(title)
        window['-IMAGE-'].update(image)
        return {'title': title, 'image':image}


    def start(self):

        window = sg.Window("Image Viewer", self.layout, element_justification='c')

        like_list = []
        dislike_list = []

        # Run the Event Loop
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == '-MANGA-':
                manga = self.getManga(window)
            if event == '-LIKE-':
                like_list.append(manga['title'])
                manga = self.getManga(window)
            if event == '-DISLIKE-':
                dislike_list.append(manga['title'])
                manga = self.getManga(window)
        window.close()


