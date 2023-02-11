import PySimpleGUI as sg 
from GetData import GData
from threading import Thread
import textwrap

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
                sg.Btn(size=(10, 5), enable_events=True, key="-NEUTRAL-", button_color = 'white on gray', button_text = 'Neutral'),
                sg.Btn(size=(10, 5), enable_events=True, key="-GETRECOMMENDATION-", button_color = 'white on black', button_text= 'Recommend'),
                sg.Btn(size=(10, 5), enable_events=True, key="-LIKE-", button_color = 'white on blue', button_text = 'Like'),
                
            ]
        ]

        ld_list = [
            [sg.Text(text = 'Favorited List', size = (30, 1))],
            [sg.Listbox([], size=(30, 4), enable_events=True, key='-LIKELIST-')],
            [sg.Text(text = 'Neutral List', size = (30, 1))],
            [sg.Listbox([], size=(30, 4), enable_events=True, key='-NEUTRALLIST-')],
            [sg.Text(text = 'Dislike List', size = (30, 1))],
            [sg.Listbox([], size=(30, 4), enable_events=True, key='-DISLIKELIST-')]
        ]

        manga_show = [
            [sg.Text(size=(40,1), key='-MANGATITLE-', justification = 'center', font = ("Arial", 15))],
            [sg.Image(size = (300,300), key = '-IMAGE-')],
            [sg.Text(size=(40,1), key='-GENRE-', justification = 'center', font = ("Arial", 10))],
            [sg.Text(size=(40,1), key='-THEME-', justification = 'center', font = ("Arial", 10))],
            [sg.Text(size=(40,None), key='-SYNOPSIS-', justification = 'center', font = ("Arial", 10))],
            [sg.Input(size = (40, 1), key='-SEARCH-', enable_events= True)],
            [sg.Listbox([], size=(40, 4), enable_events=True, key='-LIST-', select_mode= 'single')],
        ]

        recommendation = [
            [sg.Text(size = (30,1), text = 'Recommendation List', key = '-REOMMENDATION-')],
            [sg.Listbox([], size=(30, 4), enable_events=True, key='-RECOMMENDATIONLIST-', select_mode= 'single')]
        ]

        # ----- Full layout -----
        self.layout = [
            [sg.Column(ld_list, vertical_alignment = 'top', justification= 'center'),
            sg.VerticalSeparator(),
            sg.Column(manga_show, justification = 'center', element_justification= 'center'),
            sg.VerticalSeparator(),
            sg.Column(recommendation, vertical_alignment = 'top', justification= 'center')
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
        if manga.themes:
            theme = "Themes: " + ', '.join(manga.themes)
        else:
            theme = 'Themes: '
        if manga.genres:
            genre = "Genres: " + ', '.join(manga.genres) 
        else:
            genre = 'Genres: '
        if manga.synopsis:
            synopsis = textwrap.wrap(("Synopsis: " + manga.synopsis), 40)
        else:
            synopsis = 'Synopsis: '
        title = manga.title
        image = self.gdata.getImage(manga)
        self.manga = {'title': title, 'image':image, 'synopsis':synopsis, 'genre':genre, 'theme':theme}
        return self.manga

    def start(self):

        names = list(self.manga_info.index)
        window = sg.Window("Manga Recommender", self.layout, element_justification='c', resizable= True, finalize= True)
        
        def updateManga(manga):
            window['-MANGATITLE-'].update(manga['title'])
            window['-GENRE-'].update(manga['genre'])
            window['-THEME-'].update(manga['theme'])
            window['-SYNOPSIS-'].update(manga['synopsis'])
            window['-IMAGE-'].update(manga['image'])


        self.ld_dictionary = {}
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
                if self.ld_dictionary.get(self.manga['title']) == -1:
                    thread = Thread(target = self.user.updateRecommendationRanks, args = ([self.manga['title']]*2, True, True))
                    thread.start()
                elif self.ld_dictionary.get(self.manga['title'], 0) == 0:
                    thread = Thread(target = self.user.updateRecommendationRanks, args = ([self.manga['title']], True, True))
                    thread.start()
                self.ld_dictionary[self.manga['title']] = 1
            if event == '-NEUTRAL-':
                if self.ld_dictionary.get(self.manga['title']) == 1:
                    thread = Thread(target = self.user.updateRecommendationRanks, args = ([self.manga['title']], True, False))
                    thread.start()
                elif self.ld_dictionary.get(self.manga['title']) == -1:
                    thread = Thread(target = self.user.updateRecommendationRanks, args = ([self.manga['title']], False, False))
                    thread.start()
                self.ld_dictionary[self.manga['title']] = 0
            if event == '-DISLIKE-':
                if self.ld_dictionary.get(self.manga['title']) == 1:
                    thread = Thread(target = self.user.updateRecommendationRanks, args = ([self.manga['title']]*2, False, True))
                    thread.start()
                elif self.ld_dictionary.get(self.manga['title'], 0) == 0:
                    thread = Thread(target = self.user.updateRecommendationRanks, args = ([self.manga['title']], False, True))
                    thread.start()
                self.ld_dictionary[self.manga['title']] = -1
            if event == '-GETRECOMMENDATION-':
                window['-RECOMMENDATIONLIST-'].update(recommendation)
            # Search
            if values['-SEARCH-'] != '':
                search = values['-SEARCH-'].lower()
                new_values = [x for x in names if search in x.lower()]
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
            if event == '-NEUTRALLIST-' and len(values['-NEUTRALLIST-']):
                thread = Thread(target = self.getManga, args=(values['-NEUTRALLIST-'][0],))
                thread.start()
            if event == '-RECOMMENDATIONLIST-' and len(values['-RECOMMENDATIONLIST-']):
                thread = Thread(target = self.getManga, args=(values['-RECOMMENDATIONLIST-'][0],))
                thread.start()
            # After Thread
            if not thread.is_alive():
                updateManga(self.manga)
                recommendation = list(self.user.getRecommendation().index)
                window['-LIKELIST-'].update([name for name, value in self.ld_dictionary.items() if value == 1])
                window['-DISLIKELIST-'].update([name for name, value in self.ld_dictionary.items() if value == -1])
                window['-NEUTRALLIST-'].update([name for name, value in self.ld_dictionary.items() if value == 0])
                self.user.updateList(self.ld_dictionary)
        window.close()


