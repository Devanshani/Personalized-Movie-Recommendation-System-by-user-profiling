from textblob import TextBlob
import pypyodbc

con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-7PTBIGN\DEVANSHANI',
                           database='MovieRecomendationDatabase', Uid='sa', Pwd='1234')
cursor = con.cursor()
cursor.execute("SELECT preprocessedReview,ReviewId FROM ReviewsNew")
count=0
count1=0
for row in cursor.fetchall():

    tweet=row[0]
    id=row[1]
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        count = count + 1
        print(count)
        print("pos")
        cursor.execute("UPDATE ReviewsNew SET ReviewPolarity='pos' WHERE ReviewId =" + str(id))
        cursor.commit()

    elif analysis.sentiment.polarity == 0:
        print("neutral")
        cursor.execute("UPDATE ReviewsNew SET ReviewPolarity='neutral' WHERE ReviewId =" + str(id))
        cursor.commit()



    else:
        print("neg")
        count1 = count1 + 1
        cursor.execute("UPDATE ReviewsNew SET ReviewPolarity='neg' WHERE ReviewId =" + str(id))
        cursor.commit()
print(count)
print(count1)





