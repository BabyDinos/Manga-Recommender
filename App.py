import PySimpleGUI as sg 
from GetData import GData


class App:

    def __init__(self, user):
        self.gdata = user.mdata.gdata
        self.manga_info = self.gdata.df
    
    def setup(self):

        self.rating_buttons = [
            [
                sg.Btn(size=(10, 5), enable_events=True, key="-DISLIKE-", button_color = 'white on red', button_text= 'Dislike'),
                sg.Btn(size=(10, 5), enable_events=True, key="-MANGA-", button_color = 'white on black', button_text = 'New Manga'),
                sg.Btn(size=(10, 5), enable_events=True, key="-LIKE-", button_color = 'white on green', button_text = 'Like')
            ]
        ]

        left_part = [
            [sg.Text(text = 'Favorited List', size = (30, 1))],
            [sg.Listbox([], size=(30, 4), enable_events=True, key='-LIKELIST-')],
            [sg.Text(text = 'Dislike List', size = (30, 1))],
            [sg.Listbox([], size=(30, 4), enable_events=True, key='-DISLIKELIST-')]
        ]

        right_part = [
            [sg.Text(size=(60,1), key='-OUTPUT-', justification = 'center', font = ("Arial", 20))],
            [sg.Image(size = (300,300), key = '-IMAGE-')],
            [sg.Input(size = (60, 1), key='-SEARCH-', enable_events= True)],
            [sg.Listbox([], size=(60, 4), enable_events=True, key='-LIST-', select_mode= 'single')],
        ]

        # ----- Full layout -----
        self.layout = [
            [sg.Column(left_part, vertical_alignment = 'top'),
            sg.VerticalSeparator(),
            sg.Column(right_part),
            sg.HorizontalSeparator()]
        ]

    def getManga(self, name = None):
        if name:
            mal_id = self.manga_info.loc[name, 'mal_id']
        else:
            mal_id = self.gdata.getRandomMalID()
        manga = self.gdata.getManga(mal_id)
        title = manga.title
        image = self.gdata.getImage(manga)
        return {'title': title, 'image':image}


    def start(self):

        names = list(self.manga_info.index)
        window = sg.Window("Image Viewer", self.layout, element_justification='c')

        def updateManga(manga):
            window['-OUTPUT-'].update(manga['title'])
            window['-IMAGE-'].update(manga['image'])

        like_list = []
        dislike_list = []

        # Run the Event Loop
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == '-MANGA-':
                manga = self.getManga()
                updateManga(manga)
            if event == '-LIKE-':
                like_list.append(manga['title'])
                manga = self.getManga()
                updateManga(manga)
            if event == '-DISLIKE-':
                dislike_list.append(manga['title'])
                manga = self.getManga()
                updateManga(manga)
            if values['-SEARCH-'] != '':
                search = values['-SEARCH-']
                new_values = [x for x in names if search in x]
                window['-LIST-'].update(new_values)
            else:
                window['-LIST-'].update([])
            if event == '-LIST-' and len(values['-LIST-']):
                manga = self.getManga(values['-LIST-'][0])
                updateManga(manga)
        window.close()


