#Function for Seat Allotment

import mysql.connector as sqltor
from myapp.models import User, Student
from django.core.exceptions import ObjectDoesNotExist
import random
import csv

def allocate_seats(c):
    if c == 1:
        # Connect to the database
        mycon = sqltor.connect(host="localhost", user="root", passwd="", database="mydjangodb")
        cursor = mycon.cursor()
        students=[]
        
        try:
            user_data = User.objects.all()
            
            for us in user_data:
                try:
                    stu = Student.objects.get(id=us.id)
                    stu2 = Student(
                        id=us.id,
                        name=us.uname,
                        marks=us.ucutoff,
                        rank=us.urank,
                        pref1=stu.pref1,
                        pref2=stu.pref2,
                        pref3=stu.pref3,
                        allotted_course=stu.allotted_course
                    )
                    stu.delete()
                    students.append(stu2)
                    continue

                except ObjectDoesNotExist:
                    dep=["BME","IT","MTECH","ECE","EEE","CSE","CHEMICAL","CIVIL","MECH"]
                    l=[]
                    v = random.randint(0, 8)
                    pref1=dep[v]
                    l.append(v)

                    while(True):
                        v = random.randint(0, 8)
                        if v not in l:
                            pref2=dep[v]
                            l.append(v)
                            break

                    while(True):
                        v = random.randint(0, 8)
                        if v not in l:
                            pref3=dep[v]
                            l.append(v)
                            break

                    stu1 = Student(
                        id=us.id,
                        name=us.uname,
                        rank=us.urank,
                        marks=us.ucutoff,
                        pref1=pref1,
                        pref2=pref2,
                        pref3=pref3
                    )
                    students.append(stu1)

            for student in students:
                student.save()
            

            # Fetch student data
            cursor.execute("SELECT * FROM student ORDER BY `rank` ASC")
            student_data = cursor.fetchall()

            # Read the content of seat.txt once
            with open("myapp/seat.txt") as f2:
                seats = f2.readlines()
            
            for i in range(len(seats)):
                seats[i] = seats[i].strip().split(",")
                seats[i][1] = int(seats[i][1])

            for student_row in student_data:
                user_id = student_row[0]  # Assuming the first column is the user ID
                choices = [student_row[3], student_row[4], student_row[5]]  # Get pref1, pref2, pref3
                flag = 0

                if student_row[7] not in ['Not allotted','Waiting list']:
                    print(student_row[1],"Already allotted!", student_row[7])   
                    continue
                
                for choice in choices:
                    choice = choice.strip()  # Remove any leading/trailing whitespace

                    if flag != 1:
                        for j in range(len(seats)):
                            if choice == seats[j][0] and seats[j][1] > 0:
                                print(student_row[1], "has been allotted", choice)   
                                seats[j][1] -= 1
                                cursor.execute("UPDATE student SET allotted_course = %s WHERE id = %s", (choice, user_id))
                                flag = 1
                                break
                
                if flag == 0:
                    print(student_row[1], "has not been allotted")
                    cursor.execute("UPDATE student SET allotted_course = %s WHERE id = %s", ("Waiting list", user_id))

            # Write back updated seats to the file
            with open("myapp/seat.txt", "w") as f2:
                for seat in seats:
                    f2.write(f"{seat[0]},{seat[1]}\n")

            with open('myapp/allotment.csv', 'w', newline='') as fp:
                writer = csv.writer(fp)
                writer.writerow(['Username', 'Contact number', 'Cutoff', 'Rank', 'Preference 1', 'Preference 2', 'Preference 3', 'Allotted course'])

                for student_row in student_data:
                    writer.writerow([student_row[1], student_row[0], student_row[2], student_row[6], student_row[3], student_row[4], student_row[5], student_row[7]])   
            
            # Commit the changes
            mycon.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Ensure the cursor and connection are closed
            cursor.close()
            mycon.close()

# Run the function
allocate_seats(0)
