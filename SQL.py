import os
import sqlite3
import pandas as pd


class SQL():

    def __init__(self, database):

        self.database = database
        self.table = database

        if not os.path.exists("Databases"):
            os.makedirs("Databases")

        if not os.path.exists("Databases/" + self.database + ".db"):
            self.create(data = pd.DataFrame())

    def create(self, data = None):

        connection = sqlite3.connect('Databases/' + self.database + '.db')
        data.to_sql(name = self.table, con = connection, if_exists = 'replace')
        connection.commit()
        connection.close()

    def getRow(self, id = None):
        
        connection = sqlite3.connect('Databases/' + self.database + '.db')
        cursor = connection.cursor()
        description = self.getDescription()
        index = self.getIndex()
        query = 'SELECT * FROM {} WHERE {}'.format(self.table, '"{}" = {}'.format(index, id))
        cursor.execute(query)
        values = cursor.fetchall()
        row_dict = self.getColumnsValues(description, values)
        connection.commit()
        connection.close()
        return row_dict
        
    def getColumnsValues(self, description, values):
        names = list(map(lambda x: x[0], description))
        dictionary = dict(map(lambda name, value: (name, value), names, values[0]))
        return dictionary

    def getDescription(self):
        connection = sqlite3.connect('Databases/' + self.database + '.db')
        cursor = connection.cursor()
        query = "SELECT * FROM {}".format(self.table)
        cursor.execute(query)
        return cursor.description

    def getIndex(self):
        description = self.getDescription()
        return description[0][0]

    def update(self, id = None, update_dict = None):
        connection = sqlite3.connect('Databases/' + self.database + '.db')
        index = self.getIndex()
        set_string = []
        for key, value in update_dict.items():
            set_string.append("{} = {}".format(key, value))
        set_string = ', '.join(set_string)
        query = 'UPDATE Mangas SET {} WHERE {}'.format(set_string, '"{}" = 0'.format(index))
        connection.execute(query)
        connection.commit()
        connection.close()
