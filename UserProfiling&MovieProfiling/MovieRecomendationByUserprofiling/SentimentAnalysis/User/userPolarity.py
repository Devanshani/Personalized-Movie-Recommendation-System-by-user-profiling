import pypyodbc;
import SentimentAnalysis.User.userClassifier as WSD
import  os.path

if __name__ == "__main__":
    con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-7PTBIGN\DEVANSHANI',
                           database='MovieRecomendationDatabase', Uid='sa', Pwd='1234')
    cursor = con.cursor()
    cursor.execute("SELECT PreprocessedReview,TblId FROM UserReviews")
    # cursor.execute("SELECT PreprocessedComment,PreferenceId FROM UserPreference WHERE IsPreprocessed='TRUE' AND validity_classify='TRUE'")


    count = 0
    count1=0
    for row in cursor.fetchall():
        if row[0] is not None:
        # print(row[0])
            tweet = str(row[0])
            # print(row[1])
            id = str(row[1])
            result = WSD.AccessNewClassifier(tweet)
            print(result)
            polarity=result[0]
            confidence=result[1]
            print(polarity)
            print(confidence)
            # cursor.execute("UPDATE UserPreference SET Validity_classify='FALSE' WHERE PreferenceId =" + str(id))

            cursor.commit()
            if polarity == 'pos':
                count=count+1
                confidencepos=(100)*confidence
                cursor.execute("UPDATE UserReviews SET PolarityConfidence='"+str(confidencepos)+"' WHERE TblId =" + str(id))
                cursor.execute("UPDATE UserReviews SET ReviewPolarity='" + str(polarity) + "' WHERE TblId =" + str(id))
                cursor.commit()
            else:
                count1=count1+1
                confidenceneg=(-100)*confidence
                cursor.execute("UPDATE UserReviews SET PolarityConfidence='" +str(confidenceneg) + "' WHERE TblId =" + str(id))
                cursor.execute("UPDATE UserReviews SET ReviewPolarity='" + str(polarity) + "' WHERE TblId =" + str(id))
                cursor.commit()

    print(count)
    print(count1)
    cursor.close()
