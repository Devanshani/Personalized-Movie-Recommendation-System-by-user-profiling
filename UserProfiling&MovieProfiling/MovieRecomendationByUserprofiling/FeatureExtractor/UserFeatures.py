import pypyodbc
from nltk.tokenize import sent_tokenize,word_tokenize
import nltk
from nltk import FreqDist
import re
if __name__ == "__main__":


    con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-7PTBIGN\DEVANSHANI',
                           database='MovieRecomendationDatabase', Uid='sa', Pwd='1234')
    cursor = con.cursor()
    for id in range(1, 51):
        # cursor.execute("SELECT Comment FROM UserReviews WHERE userId="+ str(id))
        cursor.execute("SELECT preprocessedReview FROM UserReviews WHERE userId=" + str(id))
        count=0
        count1=0
        sentence = []
        keyWordSet = ''
        for r in cursor.fetchall():
            if r:
                # print(r[0],"****************************")
                sentence = re.sub(r'[^A-Za-z\s]+', '', r[0])
                print(sentence,"hhhhhhhhhhhhhhhh")
                processed=word_tokenize(sentence)
                pos_tagged=nltk.tag.pos_tag(processed)
                # if pos_tagged:
                print(pos_tagged)

                def leaves(tree):
                    for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
                        yield subtree.leaves()
                grammer = """NP: {(<JJ.?><NN.?><NN.?>(<NN.?>?)(<VB.?>?))|(<NN.?><VB.?>?<JJ.?><NN.?>?)|(<JJ.?><NN.?>)|(<NN.?><VB.?>)|(<VB.?><NN.?>(<VB.?>)?)|(<NN.?><NN.?>(<NN.?>?))|(<RB.?><JJ.?><NN.?>)|(<JJ.?><VB.?>)|(<NN.?><VB.?>?<JJ.?>)}"""

                chunkparser = nltk.RegexpParser(grammer)
                tree = chunkparser.parse(pos_tagged)

                keywordarray=[]
                for leaf in leaves(tree):
                    length=len(leaf)
                    sent=""
                    for n in range(0,length):
                        sent=sent+" "+leaf[n][0]
                    print(sent)
                    keywordarray.append(sent)

                for words in keywordarray:
                    keyWordSet = keyWordSet + ',' + words
                # print(keyWordSet)
                result = keyWordSet.replace(',', '', 1)
                print(str(result))
                cursor.execute("UPDATE UserInfo SET keywords ='" + str(result) + "'WHERE Id =" + str(id))
                #
                #
                cursor.commit()
    cursor.close()