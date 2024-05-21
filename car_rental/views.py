from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout
from my_app.EmailBackEnd import EmailBackEnd
from django.contrib import  messages
from .models import Vehicle
# Create your views here.
def index(request):
    return render(request,'index.html')

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