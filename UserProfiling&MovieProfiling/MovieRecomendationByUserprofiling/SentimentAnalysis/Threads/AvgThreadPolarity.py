import pypyodbc;
import operator;

if __name__ == "__main__":
    con = pypyodbc.connect(Trusted_Connection='yes', driver='{SQL Server}', server='DESKTOP-7PTBIGN\DEVANSHANI',
                           database='MovieRecomendationDatabase', Uid='sa', Pwd='1234')
    cursor = con.cursor()
    for id in range(1,51):
        cursor.execute("SELECT PolarityConfidence FROM Threads WHERE userId="+ str(id))
        count=0
        countarray=[]
        print(id)
        for row in cursor.fetchall():
            # print(row[0])
            # count=count+float(row[0])
            countarray.append(row[0])

    # print(countarray)

        # print(sorted(countarray,key=float))
        # sortedarray=sorted(countarray, key=float)
        # print(sortedarray)
        # total=len(sortedarray)
        # # print(total)
        # polarityarray = []
        # for pol in sortedarray[total-3:total]:
        #     polarityarray.append(pol)
        #     polaritySet = ''
        #     for item in polarityarray:
        #         polaritySet = polaritySet + ',' + item
        #
        #     # print(polaritySet)
        #     result = polaritySet.replace(',', '', 1)
        # print(str(result))
        sum = 0
        array = []
        for pol in countarray:
            array.append(float(pol))
            sum = float(pol) + sum
        if (len(countarray) != 0):
            avg = sum / len(countarray)
            print(avg, "jjjjjjjjjjjjj")
            cursor.execute("UPDATE UserInfo SET AvThreadPolarity ='" + str(avg) + "'WHERE Id =" + str(id))
            cursor.commit()
        else:
            cursor.execute("UPDATE UserInfo SET AvThreadPolarity ='" + str(0) + "'WHERE Id =" + str(id))
            cursor.commit()
    cursor.close()