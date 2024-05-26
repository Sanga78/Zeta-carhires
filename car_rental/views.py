from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout
from car_rental.EmailBackEnd import EmailBackEnd
from django.contrib import  messages
from .models import Vehicle,CustomUser
from django.core.files.storage import FileSystemStorage
# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request,'User Already Exists')
                return redirect('show_login')
            elif CustomUser.objects.filter(username=username).exists():
                messages.info(request,'Username Already Exists')
                return redirect('show_login')
            else:
                try:
                    user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
                    user.save()
                    messages.success(request,"Registration Successfull!")
                    return HttpResponseRedirect(reverse("show_login"))
                except:
                    messages.error(request,"Failed to Add Customer")
                    return HttpResponseRedirect(reverse("register"))
        else:
            messages.info(request,'Password Not The Same')
            return redirect('register')
    else:
        return render(request,'register.html')

def loginPage(request):
    return render(request,'login.html')

def Login(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed !</h2>")
    else:
        user = EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user != None:
            login(request,user)
            if user.user_type == "1":
                return HttpResponseRedirect(reverse("admin_home"))
            else:
                return HttpResponseRedirect(reverse("customer_home"))
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")
        
def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User : "+request.user.email+ " usertype : "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")
    
def Logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def car(request):
    cars = Vehicle.objects.all()
    return render(request,"car.html",{"cars":cars})
      
def about(request):
    return render(request,'about.html')

def tours(request):
    return render(request,'tours.html')
         
def policy(request):
    return render(request,'policy.html')