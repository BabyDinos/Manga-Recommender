import PySimpleGUI as sg 
from GetData import GData
from threading import Thread

class App:

    def __init__(self, user):
        self.user = user
        self.gdata = user.mdata.gdata
        self.manga_info = self.gdata.df
    
    def setup(self):

        rating_buttons = [
            [
                sg.Btn(size=(10, 5), enable_events=True, key="-DISLIKE-", button_color = 'white on red', button_text= 'Dislike'),
                sg.Btn(size=(10, 5), enable_events=True, key="-MANGA-", button_color = 'white on black', button_text = 'New Manga'),
                sg.Btn(size=(10, 5), enable_events=True, key="-LIKE-", button_color = 'white on green', button_text = 'Like')
            ]
        ]

        ld_list = [
            [sg.Text(text = 'Favorited List', size = (30, 1))],
            [sg.Listbox([], size=(30, 4), enable_events=True, key='-LIKELIST-')],
            [sg.Text(text = 'Dislike List', size = (30, 1))],
            [sg.Listbox([], size=(30, 4), enable_events=True, key='-DISLIKELIST-')]
        ]

        manga_show = [
            [sg.Text(size=(40,1), key='-OUTPUT-', justification = 'center', font = ("Arial", 20))],
            [sg.Image(size = (300,300), key = '-IMAGE-')],
            [sg.Input(size = (40, 1), key='-SEARCH-', enable_events= True)],
            [sg.Listbox([], size=(40, 4), enable_events=True, key='-LIST-', select_mode= 'single')],
        ]

        recommendation = [
            [sg.Text(size = (30,1), text = 'Recommendation List', key = '-REOMMENDATION-')],
            [sg.Listbox([], size=(30, 4), enable_events=True, key='-RECOMMENDATIONLIST-', select_mode= 'single')]
        ]

        # ----- Full layout -----
        self.layout = [
            [sg.Column(ld_list, vertical_alignment = 'top'),
            sg.VerticalSeparator(),
            sg.Column(manga_show, justification = 'center', element_justification= 'center'),
            sg.VerticalSeparator(),
            sg.Column(recommendation, vertical_alignment = 'top')
            ],
            [
            [sg.HorizontalSeparator()],
            [sg.Column(rating_buttons, element_justification= 'center')]
            ]
        ]

    def getManga(self, name = None):
        if name:
            mal_id = self.manga_info.loc[name, 'mal_id']
        else:
            mal_id = self.gdata.getRandomMalID()
        manga = self.gdata.getManga(mal_id) 
        title = manga.title
        image = self.gdata.getImage(manga)
        self.manga = {'title': title, 'image':image}
        return self.manga

    def start(self):

        names = list(self.manga_info.index)
        window = sg.Window("Image Viewer", self.layout, element_justification='c')

        def updateManga(manga):
            window['-OUTPUT-'].update(manga['title'])
            window['-IMAGE-'].update(manga['image'])

        ld_dictionary = {}
        thread = Thread(target = self.getManga)
        thread.start()

        # Run the Event Loop
        while True:
            event, values = window.read(timeout=200) 
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            # Buttons
            if event == '-MANGA-':
                thread = Thread(target = self.getManga)
                thread.start()
            if event == '-LIKE-':
                ld_dictionary[self.manga['title']] = 1
                window['-LIKELIST-'].update([name for name, value in ld_dictionary.items() if value == 1])
                thread = Thread(target = self.getManga)
                thread.start()
            if event == '-DISLIKE-':
                ld_dictionary[self.manga['title']] = -1
                window['-DISLIKELIST-'].update([name for name, value in ld_dictionary.items() if value == -1])
                thread = Thread(target = self.getManga)
                thread.start()
            # Search
            if values['-SEARCH-'] != '':
                search = values['-SEARCH-']
                new_values = [x for x in names if search in x]
                window['-LIST-'].update(new_values)
            else:
                window['-LIST-'].update([])
            # Listbox
            if event == '-LIST-' and len(values['-LIST-']):
                thread = Thread(target = self.getManga, args=(values['-LIST-'][0],))
                thread.start()
            if event == '-LIKELIST-' and len(values['-LIKELIST-']):
                thread = Thread(target = self.getManga, args=(values['-LIKELIST-'][0],))
                thread.start()
            if event == '-DISLIKELIST-' and len(values['-DISLIKELIST-']):
                thread = Thread(target = self.getManga, args=(values['-DISLIKELIST-'][0],))
                thread.start()
            if not thread.is_alive():
                updateManga(self.manga)
        window.close()


