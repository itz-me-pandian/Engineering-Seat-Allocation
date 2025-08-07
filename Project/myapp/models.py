from django.db import models

class User(models.Model):
    CASTE_CHOICES = (
        ('OC', 'OC'),
        ('BC', 'BC'),
        ('MBC', 'MBC'),
        ('SC', 'SC'),
        ('ST', 'ST'),
    )

    DOB_CHOICES = (
        (2002, '2002'),
        (2003, '2003'),
        (2004, '2004'),
        (2005, '2005'),
        (2006, '2006'),
    )

    uname=models.CharField(max_length=30)
    upass=models.CharField(max_length=25,default='')
    uemail=models.EmailField()
    ucaste=models.CharField(max_length=3, choices=CASTE_CHOICES,default='OC')
    uyear=models.PositiveIntegerField(choices=DOB_CHOICES,default='2005')
    um1=models.PositiveSmallIntegerField(default=35)
    um2=models.PositiveSmallIntegerField(default=35)
    um3=models.PositiveSmallIntegerField(default=35)
    um4=models.PositiveSmallIntegerField(default=35)
    utotal=models.PositiveIntegerField(default=140)
    ucutoff=models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    unvalue=models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    urank=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.uname
    
    class Meta:
        db_table = "user"

class Student(models.Model):
    name = models.CharField(max_length=100)
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    rank = models.PositiveSmallIntegerField(default=0)
    pref1 = models.CharField(max_length=250)
    pref2 = models.CharField(max_length=250)
    pref3 = models.CharField(max_length=250)
    allotted_course = models.CharField(max_length=250,default='Not allotted')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "student"