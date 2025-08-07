#File for Generating the marks for the Students for Project Demo

import random
import mysql.connector as sqltor

mycon = sqltor.connect(host="localhost", user="root", passwd="", database="mydjangodb")
cursor = mycon.cursor()
f = open("myapp/stuname.txt", "r")
l = f.readlines()
l2 = []
l1 = []

for i in l:
    s = i[0:-1]
    l1.append(s)

for i in l1:
    while True:
        number = random.randint(9000000000, 9999999999)
        if number in l2:
            continue
        else:
            l2.append(number)
            break

    s = random.randint(3, 9)
    if s == 3:
        phy = random.randint(35, 40)
        chem = random.randint(35, 40)
        mat = random.randint(35, 40)
        cs = random.randint(35,40)
    elif s == 4:
        phy = random.randint(40, 50)
        chem = random.randint(40, 50)
        mat = random.randint(40, 50)
        cs = random.randint(40,50)
    elif s == 5:
        phy = random.randint(50, 60)
        chem = random.randint(50, 60)
        mat = random.randint(50, 60)
        cs = random.randint(50,60)
    elif s == 6:
        phy = random.randint(60, 70)
        chem = random.randint(60, 70)
        mat = random.randint(60, 70)
        cs = random.randint(60,70)
    elif s == 7:
        phy = random.randint(70, 80)
        chem = random.randint(70, 80)
        mat = random.randint(70, 80)
        cs = random.randint(70,80)
    elif s == 8:
        phy = random.randint(80, 90)
        chem = random.randint(80, 90)
        mat = random.randint(80, 90)
        cs = random.randint(80,90)
    elif s == 9:
        phy = random.randint(90, 100)
        chem = random.randint(90, 100)
        mat = random.randint(90, 100)
        cs = random.randint(90,100)

    cut = (phy + chem) / 2 + mat
    tot = phy + chem + mat + cs
    dob = random.randint(2004, 2006)
    ct = random.randint(0, 100)
    passwd = i.lower()[0:4] + str(dob)
    rank = 0
    em = i.lower() + (str(number))[8:10] + '@gmail.com'
    em = em.replace(' ', '_')

    if ct >= 55:
        caste = 'OC'
        nv = cut * 0.92
    elif ct >= 25:
        caste = "BC"
        nv = cut * 0.94
    elif ct >= 10:
        caste = "MBC"
        nv = cut * 0.96
    elif ct >= 4:
        caste = "SC"
        nv = cut * 0.98
    else:
        caste = "ST"
        nv = cut

    cursor.execute("insert into user(id,uname,uemail,ucaste,um1,um2,um3,um4,utotal,uyear,unvalue,upass,urank,ucutoff) values({},'{}','{}','{}',{},{},{},{},{},{},{},'{}',{},{})".format(number, i, em, caste, mat, phy, chem, cs, tot, dob, nv, passwd, rank, cut))

mycon.commit()
mycon.close()