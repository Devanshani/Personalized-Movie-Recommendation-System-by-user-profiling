import pypyodbc;
import operator;

if __name__ == "__main__":
    con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-7PTBIGN\DEVANSHANI',
                           database='MovieRecomendationDatabase', Uid='sa', Pwd='1234')
    cursor = con.cursor()
    for id in range(1,51):
        cursor.execute("SELECT LikeCount FROM UserReviews WHERE userId="+ str(id))
        count=0
        for row in cursor.fetchall():
            likecount=row[0]
            count=count+int(likecount)


        print(count)
        print(id)
        cursor.execute("UPDATE UserInfo SET AvLikesCount ='" + str(count) + "'WHERE Id =" + str(id))
        cursor.commit()
    cursor.close()