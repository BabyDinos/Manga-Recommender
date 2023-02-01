from SQL import SQL
from Ray import Supervisor
import pandas as pd
import numpy as np
from GetData import Data
import pyarrow as pa
import pyarrow.parquet as pq


data = Data()
df = data.getRevisedMangaDataframe()
columns = list(df['title'])

# matrix = data.getSimilarityMatrix(32)
# matrix.to_parquet('Databases/SimilarityMatrix32.parquet.gzip', compression = 'GZIP')

big_matrix = pd.DataFrame()

def divide_chunks(list, chunks):
    for i in range(0, len(list), chunks):
        print(i)
        yield list[i:i+chunks]

for chunk in divide_chunks(columns, 10000):
    new_matrix = pd.read_parquet('Databases/SimilarityMatrix32.parquet.gzip', columns = chunk)
    new_matrix = new_matrix.astype(np.float16)
    big_matrix = pd.concat([big_matrix, new_matrix], axis = 1)


def getNLargest(n, input_manga):
    sorted_column = matrix[input_manga].sort_values(ascending = False)
    sorted_column = sorted_column[sorted_column.index != input_manga]
    return sorted_column[0:n]

recommendation = getNLargest(10, 'Tensei shitara Slime Datta Ken')