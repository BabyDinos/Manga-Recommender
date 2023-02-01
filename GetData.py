from Ray import Supervisor
import ray
import pandas as pd
import numpy as np
from SQL import SQL
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Wordlist import stop_words, view_list
from scipy import sparse

class Data:

    def __init__(self):
        pass

    def getMangaDataframe(self):
        supervisor = Supervisor.remote()
        manga_stats = ray.get(supervisor.getMangas.remote())

        self.df = pd.DataFrame(manga_stats).T
        return self.df

    def getRevisedMangaDataframe(self, df = None):
        if df == None:
            sql = SQL('Mangas')
            df = sql.getTable()
        df['genres'].replace('', np.nan, inplace=True)
        df = df[df['genres'].notna()]
        self.df = df
        return self.df

    def getchunks(self, iterable, chunk_size):
        size = len(iterable)
        if size < chunk_size:
            yield iterable
        chunks_nb = int(size / chunk_size)
        iter_ints = range(0, chunks_nb)
        for i in iter_ints:
            j = i * chunk_size
            if i+1 < chunks_nb:
                k = j + chunk_size
                yield iterable.iloc[j:k]
            else:
                yield iterable.iloc[j:]

    def getSimilarityMatrix(self, size = None):
        if size != None:
            try:
                self.similarities_matrix = pd.read_pickle("Databases/SimilarityMatrix{}.pkl".format(size))  
            except:
                vocabulary_set = set()
                for row in self.df['genres']:
                    genre_list = row.split(' ')
                    for genre in genre_list:
                        vocabulary_set.add(genre.lower())
                vocabulary_set = list(vocabulary_set)
                model = CountVectorizer(analyzer='word', stop_words=stop_words, vocabulary = vocabulary_set, dtype = getattr(np, 'float{}'.format(size)), lowercase = True
                )

                dtm_chunked = []
                for chunk in self.getchunks(self.df['genres'], 5000):
                    dtm_chunked.append(model.fit_transform(chunk))

                # matrices concates
                dtm = sparse.vstack(dtm_chunked)

                similarities = cosine_similarity(dtm, dense_output = True)
                self.similarities_matrix = pd.DataFrame(similarities, columns = self.df['title'], index = self.df['title']).reset_index()
            self.similarities_matrix.index = self.similarities_matrix['title']
            return self.similarities_matrix

    def saveMatrix(self, matrix, size):
        matrix.to_pickle("Databases/SimilarityMatrix{}.pkl".format(size))

    def compressMatrix(self, matrix, size):
        var_type = getattr(np, 'float{}'.format(size))
        convert_dict = {name:var_type for name in matrix.index if name != 'title'}
        matrix = matrix.astype(convert_dict)
        return matrix

