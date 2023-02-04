from SQL import SQL
from Ray import Supervisor
import pandas as pd
import numpy as np
from GetData import Data
import pyarrow as pa
import pyarrow.parquet as pq

# GUI | Character synopsis and relation


data = Data()
df = data.getRevisedMangaDataframe('themes')
theme_matrix = data.getSimilarityMatrix('themes', 32)

def getNLargest(similarity_matrix, n, input_manga):
    sorted_column = similarity_matrix[input_manga].sort_values(ascending = False)
    sorted_column = sorted_column[sorted_column.index != input_manga]
    return sorted_column[0:n]

def sortMangas(recommendation_titles, score = 0, rank = 9999999999999, popularity = 9999999999999):

    rows = list(recommendation_titles.index)

    recommendation = df.loc[rows]

    recommendation = recommendation.loc[(df['score'] >= score) & (df['rank'] <= rank) & (df['popularity'] <= popularity)]

    return recommendation['synopsis']


recommendation_titles = getNLargest(theme_matrix, 1000, 'Overlord')

mangas = sortMangas(recommendation_titles, 7, 10000)

print('|*| '+ mangas.index[0] + ' |*|\n' + mangas[0])
