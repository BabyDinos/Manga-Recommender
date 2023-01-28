from mal import Manga, Anime
from SQL import SQL
from Threading import Threading
import pandas as pd

nonexistant_manga_id = []
manga_stats = {}
def getMangas(manga_id):
    dict = {}
    try:
        manga = Manga(manga_id)
    except:
        nonexistant_manga_id.append(manga_id)
        return
    view = ['authors', 'chapters', 'favorites', 'genres', 'mal_id', 'members',
    'popularity', 'published', 'rank', 'related_manga', 'score', 'scored_by', 'status', 
    'themes', 'title', 'title_english', 'title_japanese', 'title_synonyms', 'type', 'volumes']
    for entry in view:
        dict[entry] = getattr(manga, entry)
    manga_stats[manga.title] = dict

Threading.thread(getMangas, range(1,50))

pd.DataFrame(manga_stats)

manga = Manga(1)

manga.related_manga