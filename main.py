from SQL import SQL
from Ray import Supervisor
import pandas as pd
import numpy as np
from GetData import Data
import pyarrow as pa
import pyarrow.parquet as pq


data = Data()
df = data.getRevisedMangaDataframe()
matrix = data.getSimilarityMatrix(32)
matrix.index = matrix['title']
matrix.to_parquet('Databases/SimilarityMatrix32.parquet.gzip', compression = 'GZIP')


def getNLargest(n, input_manga):
    sorted_column = matrix[input_manga].sort_values(ascending = False)
    sorted_column = sorted_column[sorted_column.index != input_manga]
    return sorted_column[0:n]

recommendation = getNLargest(10, 'Tensei shitara Slime Datta Ken')