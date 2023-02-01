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

    def getRevisedMangaDataframe(self, compare, df = None):
        self.compare = compare
        if df == None:
            sql = SQL('Mangas')
            df = sql.getTable()
        df[compare].replace('', np.nan, inplace=True)
        df = df[df[compare].notna()]
        df.index = df['title']
        df['score'] = df['score'].astype(np.float32)
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

    def getSimilarityMatrix(self, compare, size = None):
        if size != None:
            try:
                self.similarities_matrix = self.readParquet(compare, size) 
            except:
                vocabulary_set = set()
                for row in self.df[compare]:
                    compare_list = row.split(' ')
                    for comp in compare_list:
                        vocabulary_set.add(comp.lower())
                vocabulary_set = list(vocabulary_set)
                model = CountVectorizer(analyzer='word', stop_words=stop_words, vocabulary = vocabulary_set, 
                dtype = getattr(np, 'float{}'.format(size)), lowercase = True
                )

                dtm_chunked = []
                for chunk in self.getchunks(self.df[compare], 5000):
                    dtm_chunked.append(model.fit_transform(chunk))

                # matrices concates
                dtm = sparse.vstack(dtm_chunked)

                similarities = cosine_similarity(dtm, dense_output = True)
                self.similarities_matrix = pd.DataFrame(similarities, columns = self.df['title'], index = self.df['title']).reset_index()
        self.similarities_matrix.index = self.df['title']
        return self.similarities_matrix

    def readParquet(self, compare, size):
        list_of_dataframes = []
        columns = list(self.df['title'])
        path = 'Databases/SimilarityMatrix_{}_{}.parquet.gzip'.format(compare, size)

        def divide_chunks(list, chunks):
            for i in range(0, len(list), chunks):
                print(i)
                yield list[i:i+chunks]

        for chunk in divide_chunks(columns, 10000):
            new_matrix = pd.read_parquet(path, columns = chunk)
            new_matrix = new_matrix.astype(np.float16)
            list_of_dataframes.append(new_matrix)

        big_matrix = pd.concat(list_of_dataframes, axis = 1)

        return big_matrix

    def saveMatrix(self, matrix, compare, size):
        path = 'Databases/SimilarityMatrix_{}_{}.parquet.gzip'.format(compare, size)
        try:
            matrix.to_parquet(path, compression = 'GZIP')
        except:
            print("Matrix Not Saved")