"""Shelley Bercy
"""

import sqlite3

conn = sqlite3.connect('movieData.db')
print ('Opened database successfully')

conn.execute('CREATE TABLE Reviews (Username TEXT, MovieID TEXT, ReviewTime TEXT, Rating FLOAT, Review TEXT)')
print('Created Reviews table')

conn.execute('CREATE TABLE Movies (MovieID TEXT, Title TEXT, Director TEXT, Genre TEXT, Year INTEGER)')
print('Created Movie table')


conn.commit()




conn.close()
