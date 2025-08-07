#Function for Ranking the Students

import mysql.connector as sqltor
def fun(c):

    if(c==1):
        mycon=sqltor.connect(host="localhost",user="root",passwd="",database="mydjangodb")
        cursor=mycon.cursor()

        try:
            cursor.execute("SELECT * FROM user ORDER BY unvalue DESC, um1 DESC, um2 DESC, um3 DESC, utotal DESC,uyear ASC,uname ASC")
            data=cursor.fetchall()
            data=list(data)
            c=0
            cursor.execute("delete from user")
            for i in data:
                l1=list(i)
                l1[12]=c+1
                c+=1
                query="insert into user(id,uname,uemail,ucaste,um1,um2,um3,um4,utotal,uyear,unvalue,upass,urank,ucutoff) values({},'{}','{}','{}',{},{},{},{},{},{},{},'{}',{},{})".format(l1[0],l1[1],l1[2],l1[3],l1[4],l1[5],l1[6],l1[7],l1[8],l1[9],l1[10],l1[11],l1[12],l1[13])
                cursor.execute(query)
            mycon.commit()
            mycon.close()

        except "'mydjangodb.user' doesn't exist":
            print("Table doesn't exist")

fun(0)
