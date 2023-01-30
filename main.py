from SQL import SQL
from Ray import Supervisor
import modin.pandas as pd
import numpy as np
from GetData import Data


data = Data()
matrix = data.getSimilarityMatrix(16)


def getNLargest(n, input_manga):
    sorted_column = matrix[input_manga].sort_values(ascending = False)
    sorted_column = sorted_column[sorted_column.index != input_manga]
    return sorted_column[0:n]

recommendation = getNLargest(10, 'Tensei shitara Slime Datta Ken')