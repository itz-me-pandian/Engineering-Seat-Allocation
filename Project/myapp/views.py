from django.contrib import messages
from django.http import HttpResponse,request
from django.shortcuts import render,redirect,get_object_or_404
from .models import User,Student
from django.core.mail import send_mail
from .ranking import fun 
from .all import allocate_seats
import random,csv
from django.contrib.auth.models import User as djangouser

def index(request):
    return render(request,"myapp/index.html",{})

# function for writting the user details in a csv file
def write(users):
    with open('myapp/details.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Username', 'Email', 'CONTACT NUMBER', 'Caste', 'Year', 'Mark 1', 'Mark 2', 'Mark 3', 'Mark 4', 'Total', 'Cutoff', 'N-Value', 'Rank'])
        for user in users:
            writer.writerow([user.uname, user.uemail, user.id, user.ucaste, user.uyear, user.um1, user.um2, user.um3, user.um4, user.utotal, user.ucutoff, user.unvalue, user.urank])


# function for calculating cutoff and new value
def calc(cut,caste):
    if caste=='OC':
        nv=cut*0.92
    elif caste=="BC":
        nv=cut*0.94
    elif caste=="MBC":
        nv=cut*0.96
    elif caste=="SC":
        nv=cut*0.98
    elif caste=="ST":
        nv=cut
    return nv

# function for calling template for displaying all users in the admin page
def viewusers(request):
    users = User.objects.all()
    all_ranks_positive = all(user.urank > 0 for user in users)
    write(users)
    return render(request, "myapp/viewusers.html", {'userdata': users,'all_ranks_positive': all_ranks_positive})

# function for deleting a particular user from the database in the admin page
def deleteprofile(request,id):
    us = User.objects.get(id=id)
    try:
        us1 = Student.objects.get(id=id)
        us1.delete()

    except Student.DoesNotExist:
        print("Student doesn't have any choices !")

    us.delete()
    return redirect("/viewusers")

# function for calling template for displaying a particular candidate
def view(request,id):
    users = User.objects.get(id=id)
    return render(request,"myapp/viewprofile.html",{'user':users})

# function for calling the user registration template 
def userreg(request):
    return render(request,"myapp/userreg.html",{})

# function for getting new user details from the template and sending otp to the registered mail 
def insertuser(request):
    vuid = request.POST.get('tuid');
    vuname = request.POST.get('tuname');
    vuemail = request.POST.get('tuemail');
    vucaste = request.POST.get('tucaste');
    vuyear = request.POST.get('tuyear');
    vum1 = request.POST.get('tum1');
    vum2 = request.POST.get('tum2');
    vum3 = request.POST.get('tum3');
    vum4 = request.POST.get('tum4');
    vtot = int(vum1) +int(vum2) + int(vum3) +int(vum4);
    vcut = round(int(vum1)+(int(vum2)+int(vum3))/2,2)
    vupass=vuname[:4].lower()+vuyear;
    vnvalue=calc(vcut,vucaste);

    try:
        us=User.objects.get(id=vuid)
        Us=User(id=vuid,uname=vuname,upass=vupass,uemail=vuemail,ucaste=vucaste,uyear=vuyear,um1=vum1,um2=vum2,um3=vum3,um4=vum4,utotal=vtot,ucutoff=vcut,unvalue=vnvalue);
       
        messages.error(request, 'Already registered with the same contact number !')
        return render(request,'myapp/userreg.html',{'messages':messages.get_messages(request)})

    except:
        otp=str(random.randint(1000,9999))
        request.session['otp']=otp
        request.session['vuid']=vuid
        request.session['vuname']=vuname
        request.session['vuemail']=vuemail
        request.session['vucaste']=vucaste
        request.session['vuyear']=vuyear
        request.session['vum1']=vum1
        request.session['vum2']=vum2
        request.session['vum3']=vum3
        request.session['vum4']=vum4
        request.session['vtot']=vtot
        request.session['vcut']=vcut
        request.session['vupass']=vupass
        request.session['vnvalue']=vnvalue

        send_mail(
                    'OTP for Validating',
                    f'To complete your verification, please use the following OTP\n\nOTP:{otp}\n\nThis OTP is valid for 10 minutes.\n\nPlease do not share this OTP with anyone for security reasons.\n\nIf you did not request this OTP or have any concerns, ignore this mail.',
                    'alloteasyregofficial@gmail.com',
                    [vuemail],
                    fail_silently=True,
                )
        return render(request,"myapp/otp.html",{'user':vuname})

# function for fetching the otp and verifying the otp and then storing the user details in the database
def otp_verify(request):
    otp1=request.POST.get('otp1')
    otp2=request.POST.get('otp2')
    otp3=request.POST.get('otp3')
    otp4=request.POST.get('otp4')
    votp=otp1+otp2+otp3+otp4
    uotp=request.session.get('otp')
    vuname = request.session.get('vuname')
    print(uotp,votp)
    if(votp==uotp):
        vuid = request.session.get('vuid')
        vuname = request.session.get('vuname')
        vuemail = request.session.get('vuemail')
        vucaste = request.session.get('vucaste')
        vuyear = request.session.get('vuyear')
        vum1 = request.session.get('vum1')
        vum2 = request.session.get('vum2')
        vum3 = request.session.get('vum3')
        vum4 = request.session.get('vum4')
        vtot = request.session.get('vtot')
        vcut = request.session.get('vcut')
        vnvalue = request.session.get('vnvalue')
        vupass = request.session.get('vupass')
        us=User(id=vuid,uname=vuname,upass=vupass,uemail=vuemail,ucaste=vucaste,uyear=vuyear,um1=vum1,um2=vum2,um3=vum3,um4=vum4,utotal=vtot,ucutoff=vcut,unvalue=vnvalue);
        us.save()
        send_mail(
                'Password for login',
                f'Hi {vuname},\n\nYour details are verified, please use the following Password for login\n\nPassword:{vupass}\n\nPlease reach out us for any Queries\n\nThank You.',
                'alloteasyregofficial@gmail.com',
                [vuemail],
                fail_silently=True,
            )
        messages.error(request, 'Successfully Registered ! ')
        messages.error(request, 'See your email for login details !!')
        return render(request,'myapp/login.html',{'messages':messages.get_messages(request),'user':vuname})
    else:
        messages.error(request, 'Enter correct OTP !!')
        return render(request,'myapp/otp.html',{'messages':messages.get_messages(request),'user':vuname})


# function for caling login template for user
def login(request):
    return render(request,"myapp/login.html",{'messages':messages.get_messages(request)})

# function for caling login template for admin
def adlogin(request):
    return render(request,"myapp/adlogin.html",{})

# function for verifying the login credentials with the existing data in the database (user)
def login_check(request):
    if request.method == 'POST':
        id=request.POST.get('contact_number')
        uname = request.POST.get('name')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(id=id)

        except User.DoesNotExist:
            print('Invalid Username!!!')
            messages.error(request, "Username Doesn't exist !")
            return render(request,"myapp/login.html",{'messages': messages.get_messages(request)})
        
        except ValueError:
            messages.error(request, 'Invalid user ID format !')
            return redirect('login')
        
        if user.upass==password and user.uname==uname:
            user1=User.objects.get(id=id)
            return render(request,"myapp/viewprofile.html",{'user':user1})
        else:
            print('Invalid Password!!!')
            messages.error(request, 'Invalid username or password !!')
            return render(request,"myapp/login.html",{'messages': messages.get_messages(request)})
    else:
        return redirect('login')
    

# function for verifying the login credentials with the existing data in the database (admin)
def adlogin_check(request):
    if request.method == 'POST':
        id=request.POST.get('contact_number')
        password = request.POST.get('password')

        if(id=='1234567890') and (password=='abc2005'):
            return redirect('viewusers')
        
        else:
            messages.error(request, 'Invalid username or password')
            return render(request,"myapp/adlogin.html",{'messages': messages.get_messages(request)})
        
    else:
        return redirect('adlogin')

# function for calling the ranking function when admin clicks on Generate ranklist button  
def ranking(request):
    user=User.objects.all()
    fun(1)
    users = User.objects.all()
    all_ranks_positive = all(user.urank > 0 for user in users)
    messages.error(request, 'Candidates are ranked !')
    return render(request, "myapp/viewusers.html", {'userdata': users,'all_ranks_positive': all_ranks_positive,'messages': messages.get_messages(request)})


# function for calling the choice filling template for individual candidate
def c_fill(request,id):
    user = get_object_or_404(User, id=id)
    try:
        student = Student.objects.get(id=id)
        return render(request, 'myapp/choice.html', {'user': user,'student':student})
    
    except Student.DoesNotExist:
        return render(request, 'myapp/choice.html', {'user': user})

# function for saving the preferences of an individual candidate in the database 'student'
def save_choices(request):
    unum=request.POST.get('num')
    user=User.objects.get(id=unum)
    uname=user.uname
    urank=user.urank
    umark=request.POST.get('cutoff')
    upref1=request.POST.get('pref1')
    upref2=request.POST.get('pref2')
    upref3=request.POST.get('pref3')
    if uname and umark and upref1 and upref2 and upref3:
        stu=Student(id=unum,name=uname,marks=umark,pref1=upref1,pref2=upref2,pref3=upref3,rank=urank)
        stu.save()

    messages.error(request, 'Choice filled ! Login !!')
    return render(request,"myapp/login.html",{'messages': messages.get_messages(request)})

# function for calling the function which fills the preferences for all students and then allotting seats for the candidates    
def allot(request):
    allocate_seats(1)
    users = User.objects.all()
    all_ranks_positive = all(user.urank > 0 for user in users)
    write(users)
    messages.error(request, 'Seats are Allotted to the candidates !')
    return render(request, "myapp/viewusers.html", {'userdata': users,'all_ranks_positive': all_ranks_positive,'messages': messages.get_messages(request)})
