"""Shelley Bercy
"""

from flask import Flask, render_template, request, redirect
import sqlite3 as sql
from datetime import datetime

app = Flask(__name__)
conn = sql.connect('movieData.db')

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/AddReview')
def AddReview():
    return render_template('addReview.html')

@app.route('/addReview', methods=['POST', 'GET'])
def addReview():
    if request.method == 'POST':
        try:
            # All the fields in the table 
            Title = request.form['Title']
            Genre = request.form['Genre']
            Review = request.form['Review']
            Rating = request.form['Rating']
            UserName = request.form['Username']
            Director = request.form['Director']
            Years = request.form['Year']
            ReviewTime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            MovieID = Title[:5] + Years
            Year = int(Years)


            with sql.connect("movieData.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO Movies (MovieID, Title, Director, Genre, Year) VALUES (?,?,?,?,?)",
                            (MovieID, Title, Director, Genre, Year))
                cur.execute("INSERT INTO Reviews (Username, MovieID, ReviewTime, Rating, Review) VALUES (?,?,?,?,?)",
                            (UserName, MovieID, ReviewTime, Rating, Review))
                con.commit()
        except:
            con.rollback()    
        finally:
            return render_template("index.html")
            con.close()

@app.route('/GetReviews')
def GetReviews():
    return render_template('getReviews.html')


@app.route('/getReviewByGenre', methods = ['POST', 'GET'])
def getReview():
    if request.method == 'POST':
            genre = request.form['Genre']
            with sql.connect("movieData.db") as con:
                    con.row_factory = sql.Row
                    cur = con.cursor()
                    cur.execute("""SELECT Movies.Title, Movies.Director, Reviews.Review, Reviews.Rating FROM Movies
                                    JOIN Reviews ON Reviews.MovieID = Movies.MovieID WHERE Movies.Genre=?""",(genre,))
                    rows = cur.fetchall()
            return render_template('listByGenre.html', rows=rows, genre=genre)

                  
@app.route('/getYear')
def year():
   return render_template('getYear.html')
    

@app.route('/top5', methods=['POST', 'GET'])
def topMovie():
    if request.method == 'POST':
        try:
            year = request.form['year']
            with sql.connect("movieData.db") as con:
                con.row_factory = sql.Row
                cur = con.cursor()
                cur.execute(
                    #Gets the average of the the ratings 
                    "SELECT Movies.Title, Movies.Genre, AVG(Reviews.Rating) AS Rating FROM Movies JOIN Reviews ON Movies.MovieID = Reviews.MovieID WHERE Movies.Year = ? GROUP BY Movies.MovieID ORDER BY Rating DESC LIMIT 5", (year,))
                rows = cur.fetchall()
        except Exception as e:
            print(e)
            msg = "Error in select operation"
        finally:
            con.close()
            return render_template("bestInYear.html", top_movies=rows, year=year)

if __name__ == '__main__':
   app.run(debug = True)
