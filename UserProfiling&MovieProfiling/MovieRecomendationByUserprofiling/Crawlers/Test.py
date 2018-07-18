import json, requests
import pypyodbc
from time import sleep

con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-7PTBIGN\DEVANSHANI',
                       database='MovieRecomendationDatabase', Uid='sa', Pwd='1234')
cursor = con.cursor()
# cursor.execute("UPDATE IMDBMovieData SET CC='FALSE'")
cursor.execute("SELECT Movie,TblId from UserReviews WHERE AAA='FALSE'")

for r in cursor.fetchall():
    if r[0] is not None:

        movieImdbtitle = r[0]
        # cursor.execute("SELECT DISTINCT IMDB_Id FROM MovieData")
        ID=r[1]

        print(movieImdbtitle,"ggggggggggggg")

        # movieImdbId="tt0065421"
        url = "http://www.omdbapi.com/?apikey=7d34e0a8&t=%s&plot=full&r=json" % movieImdbtitle




        response = requests.get(url)
        print(response.text)
        movie_data = json.loads(response.text)
        imdbId=movie_data['imdbID']
        title=movie_data['Title']
        year=movie_data['Year']
        genre=movie_data['Genre']
        director=movie_data['Director']
        writter=movie_data['Writer']
        actors=movie_data['Actors']
        plot=movie_data['Plot']
        imdbVotes=movie_data['imdbVotes']
        imdbRating=movie_data['imdbRating']

        cursor.execute('INSERT INTO MovieWatched (imdb_id,title,releasedYear,Genre,Director,Writter,actors,moviePlot,imdb_rating,imdb_votes)VALUES (?,?,?,?,?,?,?,?,?,?)', (imdbId,title,year,genre,director,writter,actors,plot,imdbVotes,imdbRating))
        # # cursor.execute("UPDATE  ReviewsNew SET readData='TRUE' WHERE imdb =" + str(imdbid))
        #
        cursor.execute("UPDATE UserReviews SET AAA='TRUE' WHERE TblId =" + str(ID))
        cursor.commit()
cursor.close()