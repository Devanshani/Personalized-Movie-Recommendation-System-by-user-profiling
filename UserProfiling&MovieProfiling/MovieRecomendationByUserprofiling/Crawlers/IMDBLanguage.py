# Language

import json, requests
import pypyodbc
from time import sleep

con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-7PTBIGN\DEVANSHANI',
                       database='MovieRecomendationDatabase', Uid='sa', Pwd='1234')
cursor = con.cursor()
# cursor.execute("UPDATE IMDBMovieData SET CC='FALSE'")
cursor.execute("SELECT imdb_id,ID FROM MovieInfos WHERE AA='FALSE'")

for r in cursor.fetchall():
    imdbid=r[0]
    movieImdbId = r[0]
    # cursor.execute("SELECT DISTINCT IMDB_Id FROM MovieData")

    url = "http://www.omdbapi.com/?apikey=65d34f23&i=%s&plot=full&r=json" % movieImdbId
    id=r[1]


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
    language=movie_data['Language']
    print(language)
    cursor.execute('INSERT INTO IMDBLanguage (im_id,language)VALUES (?,?)', (imdbid,language))
    cursor.execute("UPDATE  MovieInfos SET AA='TRUE' WHERE ID =" + str(id))
    # cursor.execute("UPDATE  MovieInfos SET Language="+str(language)+" WHERE ID =" + str(id))
    cursor.commit()
cursor.close()