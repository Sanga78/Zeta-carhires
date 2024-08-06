from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout
from car_rental.EmailBackEnd import EmailBackEnd
from django.contrib import  messages
from .models import Vehicle,CustomUser
from django.core.files.storage import FileSystemStorage
from .models import *
from django.views.decorators.csrf import csrf_exempt
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
                    messages.success(request,f"Account Successfully created:{user.username}")
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

def earn(request):
    return render(request,'earn.html')
def response(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed !</h2>")
    else:
        customer_name = request.POST['full_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        message= request.POST['message']
        try:
            response = Responses(customer_name=customer_name, email=email, phone_number=phone_number,message=message)
            response.save()
            messages.success(request,"Successfully sent message")
            return HttpResponseRedirect(reverse("earn"))
        except:
            messages.error(request,"Failed to send message")
            return HttpResponseRedirect(reverse("earn"))

def grow(request):
    return render(request,'grow.html')

def list_fleet(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed !</h2>")
    else:
        full_name = request.POST['personal_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        company_name = request.POST['company_name']
        no_of_cars = request.POST.get('cars')
        try:
            fleet =Fleet(full_name=full_name, company_name=company_name, phone_number=phone_number,email=email,no_of_cars=no_of_cars)
            fleet.save()
            messages.success(request,"Your request has been received successfully We will get back to you")
            return HttpResponseRedirect(reverse("grow"))
        except:
            messages.error(request,"Failed to send message")
            return HttpResponseRedirect(reverse("grow"))
        
def hire_request(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed !</h2>")
    else:
        full_name = request.POST['full-name']
        destination = request.POST['destination']
        phone_number = request.POST['phone']
        car_id = request.POST.get('car')
        rented_on = request.POST['start-date']
        rented_to = request.POST['end-date']
        try:
            car = Vehicle.objects.get(id=car_id)
            hire =Hire_Request(full_name=full_name, destination=destination, phone_number=phone_number,car_id=car,rented_on=rented_on,rented_to=rented_to)
            hire.save()
            messages.success(request,"Successfully sent message")
            return HttpResponseRedirect(reverse("car"))
        except:
            messages.error(request,"Failed to send message")
            return HttpResponseRedirect(reverse("car"))

def buy(request):
    cars = Car.objects.all()
    return render(request,'buy.html', {'cars': cars})

def tour_request(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed !</h2>")
    else:
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        message= request.POST['reply']
        try:
            response = Tours_request(full_name=full_name, email=email, phone_number=phone_number,message=message)
            response.save()
            messages.success(request,"Successfully sent message")
            return HttpResponseRedirect(reverse("tours"))
        except:
            messages.error(request,"Failed to send message")
            return HttpResponseRedirect(reverse("tours"))
        
@csrf_exempt     
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    
@csrf_exempt     
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)