from SQL import SQL
from Ray import Supervisor
import pandas as pd
import numpy as np
from GetData import GData
from ManipulateData import MData
from User import User
import pyarrow as pa
import pyarrow.parquet as pq
from App import App

# GUI | Character synopsis and relation


def main():
        
    gdata = GData('themes')

    mdata = MData(gdata)

    user = User('User', mdata)

    app = App(user)

    app.setup()

    app.start()

if __name__ == '__main__':
    main()

