from SQL import SQL
from Ray import Supervisor
import pandas as pd
import numpy as np
from GetData import GData
from ManipulateData import MData
from User import User
import pyarrow as pa
import pyarrow.parquet as pq

# GUI | Character synopsis and relation


gdata = GData()

df = gdata.getRevisedMangaDataframe('themes')

mdata = MData(gdata)

mdata.updateRecommendationRanks(['Overlord','Berserk'])

user = User('BabyDino', mdata)

user.updateList(['Overlord', 'Tensei shitara Slime Datta Ken'])

user.getCompleteList()

user.getRecommendation()

user.mdata.recommendation_dict