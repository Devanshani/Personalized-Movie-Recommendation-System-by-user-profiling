import pypyodbc
con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-7PTBIGN\DEVANSHANI',
                           database='MovieRecomendationDatabase', Uid='sa', Pwd='1234')
cursor = con.cursor()
cursor.execute("SELECT preprocessedReview FROM ReviewsNew WHERE ReviewPolarity='pos'")
# cursor.execute("SELECT imdb FROM ReviewsNew")


for row in cursor.fetchall():
    print(row[0])
#     title="Metropolitan"
# cursor.execute("UPDATE  MovieData SET AvReviewPolarity="+str(90)+" WHERE title =" + str(title))