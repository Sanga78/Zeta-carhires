from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.contrib import messages
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .forms import AddCustomerForm,EditCustomerForm

def admin_home(request):
    return render(request, "Admin_templates/home.html")

def add_vehicle(request):
    return render(request, 'Admin_templates/add_vehicle.html')

def add_vehicle_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect('Method Not Allowed')
    else:
        car_name = request.POST['car_name']
        car_image = request.FILES['car_image']
        color = request.POST['color']
        price = request.POST['price']
        description = request.POST['description']
        capacity = request.POST['capacity']
        try:
            car = Vehicle(car_name=car_name, car_image=car_image,color=color, price=price, description = description, capacity=capacity)
            car.save()
            messages.success(request,"Successfully Added car")
            return HttpResponseRedirect(reverse("list_vehicles"))
        except:
            messages.error(request,"Failed to Add vehicle")
            return HttpResponseRedirect(reverse("add_vehicle"))

def edit_vehicle(request,vehicle_id):
    vehicle=Vehicle.objects.get(id=vehicle_id)
    return render(request,"admin_templates/edit_vehicle.html",{"vehicle":vehicle,"id":vehicle_id})

def edit_vehicle_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect("Method Not Allowed")
    else:
        vehicle_id = request.POST.get("vehicle_id")
        car_name = request.POST.get("car_name")
        car_image = request.FILES['car_image']
        color = request.POST['color']
        description = request.POST['description']
        capacity = request.POST['capacity']
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle.car_name = car_name
            vehicle.car_image = car_image
            vehicle.color = color
            vehicle.description = description
            vehicle.capacity = capacity
            vehicle.save()
            messages.success(request,"Successfully Edited vehicle")
            return HttpResponseRedirect(reverse("edit_vehicle",kwargs={"vehicle_id":vehicle_id}))
        except:
            messages.error(request,"Failed to Edit vehicle")
            return HttpResponseRedirect(reverse("edit_vehicle",kwargs={"vehicle_id":vehicle_id}))

def manage_vehicles(request):
    cars = Vehicle.objects.all()
    return render(request,"Admin_templates/manage_cars.html",{"cars":cars})

def earn_responses(request):    
    requests = Hire_Request.objects.all()
    responses = Responses.objects.all()
    return render(request,"Admin_templates/earn_requests.html",{"responses": responses,"requests": requests})

def hire_requests(request):
    responses = Responses.objects.all()
    requests = Hire_Request.objects.all()
    return render(request,"Admin_templates/hire_requests.html",{"requests": requests,"responses": responses})

def add_customer(request):
    form = AddCustomerForm()
    return render(request,"Admin_templates/add_customer.html",{"form":form})

def add_customer_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddCustomerForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"] 
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]

            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name,profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
                user.customer.address = address
                user.customer.profile_pic = profile_pic_url
                user.save()
                messages.success(request,"Successfully added customer")
                return HttpResponseRedirect(reverse("add_customer"))
            except:
                messages.error(request,"Failed to Add Customer")
                return HttpResponseRedirect(reverse("add_customer"))
        else:
            form=AddCustomerForm(request.POST)
            return render(request,"Admin_templates/add_customer.html",{"form":form})

def edit_customer(request,customer_id):
    request.session['student_id']=customer_id
    customer=Customer.objects.get(admin=customer_id)
    form = EditCustomerForm()
    form.fields['email'].initial=customer.admin.email
    form.fields['first_name'].initial=customer.admin.first_name
    form.fields['last_name'].initial=customer.admin.last_name
    form.fields['username'].initial=customer.admin.username
    form.fields['address'].initial=customer.address
    return render(request,"Admin_templates/edit_customer.html",{"form":form,"id":customer_id,"username":customer.admin.username})

def edit_customer_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        customer_id = request.session.get("customer_id")
        if customer_id == None:
            return HttpResponseRedirect(reverse("manage_customer"))
        form = EditCustomerForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"] 
            address = form.cleaned_data["address"]

            if request.FILES.get('profile_pic',False):
                profile_pic = request.FILES('profile_pic')
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name,profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None 

            try:
                user=CustomUser.objects.get(id=customer_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                customer = Customer.objects.get(admin=customer_id)
                customer.address=address
                if profile_pic_url != None:
                    customer.profile_pic = profile_pic_url
                customer.save() 
                del request.session['customer_id']
                messages.success(request,"Successfully Edited Customer")
                return HttpResponseRedirect(reverse("edit_customer",kwargs={"customer_id":customer_id}))
            except:
                messages.error(request,"Failed to Edit Customer")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"customer_id":customer_id}))
        else:
            form = EditCustomerForm(request.POST)
            customer = Customer.objects.get(admin=customer_id)
            return render(request,"Admin_templates/edit_customer.html",{"form":form,"id":customer_id,"username":customer.admin.username})

def manage_customer(request):
    customers=Customer.objects.all()
    return render(request,"Admin_templates/manage_customer.html",{"customers":customers})

def tour_requests(request):
    tours = Tours_request.objects.all()
    return render(request,"Admin_templates/tour_requests.html",{"tours":tours})