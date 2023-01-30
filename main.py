from mal import Manga, Anime
from SQL import SQL
from Threading import Threading
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Wordlist import stop_words, view_list

from Ray import Supervisor
import ray

supervisor = Supervisor.remote()
manga_stats = ray.get(supervisor.getMangas.remote())

df = pd.DataFrame(manga_stats).T

sql = SQL('Mangas')
sql.create(data=df)

vectorizer = CountVectorizer(analyzer = 'word', stop_words = 'english', stop_words = stop_words, lowercase=True)
vectorizer = vectorizer.fit_transform(df['genres'])
similarities = cosine_similarity(vectorizer)

similarities_matrix = pd.DataFrame(similarities, columns = df['title'], index = df['title']).reset_index()
similarities_matrix

similarities_matrix['title']

input_manga = 'Berserk'
recommendations = pd.DataFrame(similarities_matrix.nlargest(3, input_manga)['title'])
recommendations = recommendations[recommendations['title']!=input_manga]



