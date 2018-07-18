import pypyodbc
from rake_nltk import Rake
import nltk
import RAKE
import operator
# import SentimentAnalysis.PolarityAnalyze.polarityClassify as PAU
if __name__ == "__main__":

    rake_object = RAKE.Rake("E:\MovieRecomendationByUserprofiling\Preprocessor\smartstopwords.txt")
    # rake_object =Rake(nltk.corpus.stopwords.words())
    con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-7PTBIGN\DEVANSHANI',
                           database='MovieRecomendationDatabase', Uid='sa', Pwd='1234')
    cursor = con.cursor()
    for id in range(1, 36):
        # cursor.execute("SELECT Comment FROM UserReviews WHERE userId="+ str(id))
        cursor.execute("SELECT Comment FROM UserReviews WHERE userId=" + str(id))
        for r in cursor.fetchall():
            print(r[0])
            keywords = rake_object.run(r[0])
            print("Keywords:", keywords)
            print(" ")
    #     userid=r[1]
    #
    #
    #     commentid=r[2]
    #     categoryid=r[3]
    #     id=r[4]
    #     # decoded = ([[word for word in sets] for sets in keywords])
    #
    #
    #     keyWordSet = ''
    #
    #     for words in keywords:
    #         keyWordSet = keyWordSet + ',' + words[0]
    #
    #     print(keyWordSet.replace(',', '', 1))
    #     # result = keyWordSet.replace(',', '', 1)
    #
    #     result = keyWordSet.replace(',', '', 1).split(',')
    #     print(result)
    #     # for res in result:
    #     #     result = PAU.AccessNemesisClassifier(res)
    #     #     print(res)
    #     #     polarity = result[0]
    #     #     pol = -1
    #     #     if (polarity == 'pos'):
    #     #         count = count + 1
    #     #         pol = 1
    #     #     elif (polarity == 'neg'):
    #     #         pol = 0
    #     #
    #     #     confidence = result[1]
    #     #     print(polarity)
    #     #     # cursor.execute('INSERT INTO Features (UserId,CommentId,keywords,CategoryId,PosorNeg) VALUES (?,?,?,?,?)',(userid, commentid, sent, categoryid,polarity))
    #     #     # cursor.commit()
    #     #     print(confidence)
    #
    #         # cursor.execute('INSERT INTO Features (UserId,CommentId,keywords,CategoryId) VALUES (?,?,?,?)', (userid,commentid,res,categoryid))
    #         # cursor.execute("UPDATE UserPreference SET IsExtracted='TRUE' WHERE PreferenceId =" + str(id))
    #         # cursor.commit()
    # # cursor.close()