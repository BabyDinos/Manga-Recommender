from SQL import SQL
from Ray import Supervisor
import pandas as pd
import numpy as np
from GetData import GData
from ManipulateData import MData
import pyarrow as pa
import pyarrow.parquet as pq

# GUI | Character synopsis and relation


gdata = GData()

df = gdata.getRevisedMangaDataframe('themes')
theme_matrix = gdata.getSimilarityMatrix('themes', 32, ['Overlord'])


mdata = MData(df, theme_matrix)

mdata.updateRecommendationRanks('Overlord', add = True)

mdata.getRecommendation()