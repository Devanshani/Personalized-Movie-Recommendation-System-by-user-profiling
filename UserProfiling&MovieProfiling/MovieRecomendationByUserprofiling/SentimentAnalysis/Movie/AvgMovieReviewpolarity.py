import pypyodbc;
import operator;

if __name__ == "__main__":
    con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-7PTBIGN\DEVANSHANI',
                           database='MovieRecomendationDatabase', Uid='sa', Pwd='1234')
    cursor = con.cursor()

    cursor.execute("SELECT imdb,AVG(PolarityConfidence) FROM ReviewsNew GROUP BY imdb")
    count=0
    countarray=[]
    for row in cursor.fetchall():
        print(row)
        id=row[0]
        average=row[1]

        movieImdbId=id
        if (len(str(movieImdbId)) == 6):
            movieImdbId = "tt0" + movieImdbId
        elif (len(str(movieImdbId)) == 5):
            movieImdbId = "tt00" + movieImdbId
        else:
            movieImdbId = "tt" + movieImdbId
        print(movieImdbId,average)
        cursor.execute("UPDATE Movieinfos SET PolarityConfidence ='" + str(average) + "' WHERE imdb_id ="+str(movieImdbId))
        cursor.commit()
cursor.close()