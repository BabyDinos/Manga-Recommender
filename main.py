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
df = data.getRevisedMangaDataframe('genres')
genre_matrix = data.getSimilarityMatrix('genres',32)

def getNLargest(similarity_matrix, n, input_manga):
    sorted_column = similarity_matrix[input_manga].sort_values(ascending = False)
    sorted_column = sorted_column[sorted_column.index != input_manga]
    return sorted_column[0:n]

def sortMangas(recommendation_titles, sort_by, ascending):

    rows = list(recommendation_titles.index)

    recommendation = df[df.index.isin(rows)].sort_values(by = sort_by, ascending = ascending)

    return recommendation['synopsis']

recommendation_titles = getNLargest(genre_matrix, 1000, 'Black Clover')
mangas = sortMangas(recommendation_titles, ['score'], [False])

print('|*| '+ mangas.index[0] + ' |*|\n' + mangas[0])

mangas