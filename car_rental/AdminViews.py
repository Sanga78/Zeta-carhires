from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.contrib import messages
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .forms import AddCustomerForm,EditCustomerForm,CarForm, CarImageForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def admin_home(request):
    car_count=Vehicle.objects.all().count()
    hire_requests_count=Hire_Request.objects.all().count()
    car_for_sale_count=Car.objects.all().count()
    bookings_count=Booking.objects.all().count()
    customers_count=Customer.objects.all().count()

    cars_all=Vehicle.objects.all()

    cars_available=[]
    cars_booked=[]
    car_name_list=[]
    for car in cars_all:
        car_name_list.append(car.car_name)
        if car.is_available:
            available=Vehicle.objects.filter(id=car.id).count()
            cars_available.append(available)
        else:
            booked=Vehicle.objects.filter(id=car.id).count()
            cars_booked.append(booked)                   
    cars_av = len(cars_available)
    booked_cars = len(cars_booked)
    context = {"car_count":car_count,"hire_requests_count":hire_requests_count,"car_for_sale_count":car_for_sale_count,"bookings_count":bookings_count,"customers_counts":customers_count,"booked":cars_booked,"available":cars_available,"car_name_list":car_name_list,"cars_av":cars_av,"booked_cars":booked_cars}
    return render(request, "Admin_templates/home.html",context)

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
            return HttpResponseRedirect(reverse("manage_vehicle"))
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
    responses = Responses.objects.all()
    requests = Hire_Request.objects.all()
    tours = Tours_request.objects.all()
    return render(request,"Admin_templates/earn_requests.html",{"responses": responses,"requests": requests,"tours":tours})

def hire_requests(request):
    responses = Responses.objects.all()
    requests = Hire_Request.objects.all()
    tours = Tours_request.objects.all()
    return render(request,"Admin_templates/hire_requests.html",{"requests": requests,"responses": responses,"tours":tours})

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
    request.session['customer_id']=customer_id
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

            profile_pic_url = None
            if 'profile_pic' in request.FILES:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename) 

            try:
                user=CustomUser.objects.get(id=customer_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                customer = Customer.objects.get(admin=customer_id)
                customer.address=address
                if profile_pic_url:
                    customer.profile_pic = profile_pic_url
                customer.save() 
                del request.session['customer_id']
                messages.success(request,"Successfully Edited Customer")
                return HttpResponseRedirect(reverse("edit_customer",kwargs={"customer_id":customer_id}))
            except:
                messages.error(request,"Failed to Edit Customer")
                return HttpResponseRedirect(reverse("edit_customer",kwargs={"customer_id":customer_id}))
        else:
            form = EditCustomerForm(request.POST)
            customer = Customer.objects.get(admin=customer_id)
            return render(request,"Admin_templates/edit_customer.html",{"form":form,"id":customer_id,"username":customer.admin.username})

def manage_customer(request):
    customers=Customer.objects.all()
    return render(request,"Admin_templates/manage_customer.html",{"customers":customers})

def tour_requests(request):
    responses = Responses.objects.all()
    requests = Hire_Request.objects.all()
    tours = Tours_request.objects.all()
    return render(request,"Admin_templates/tour_requests.html",{"tours":tours,"responses":responses,"requests":requests})

def return_car(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return_date = timezone.now()
    booking.return_date = return_date
    # Calculate total cost
    days_booked = (return_date - booking.booking_date).days
    total_cost = days_booked * booking.car.price
    booking.total_cost = total_cost
    car = booking.car
    car.is_available = True
    car.save()
    booking.save()
    # Send billing email
    subject = 'Zeta CarHires Billing Details'
    html_message = render_to_string('emails/billing_details.html', {
        'customer_name': booking.customer_name.admin.username,
        'car_name': car.car_name,
        'total_cost': total_cost,
        'days_booked': days_booked,
        'booking_date': booking.booking_date,
        'return_date': return_date,
    })
    plain_message = strip_tags(html_message)
    from_email = 'zetacarhires@gmail.com'
    to = booking.customer_name.admin.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    return HttpResponseRedirect(reverse("bookings"))

def new_fleet(request):
    fleets = Fleet.objects.all()
    return render(request,"Admin_templates/fleet.html",{"fleets":fleets})

def bookings(request):
    cars = Car.objects.all()
    bookings = Booking.objects.all()
    return render(request,"Admin_templates/bookings.html",{"cars":cars,"bookings":bookings})

def add_car(request):
    if request.method == 'POST':
        car_form = CarForm(request.POST, request.FILES)
        if car_form.is_valid():
            car = car_form.save()
            messages.success(request, 'Car added successfully!')
            return redirect('car_list')
        else:
            messages.error(request, 'Error adding car. Please correct the errors below.')
    else:
        car_form = CarForm()
    return render(request, 'Admin_templates/add_car_for_sale.html', {'car_form': car_form})
def car_list(request):
    cars = Car.objects.all()
    return render(request, 'Admin_templates/car_list.html', {'cars': cars})

def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request,"Admin_templates/admin_profile.html",{"user":user})

def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        profile_pic_url = None
        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            admin = CarDealer.objects.get(admin=customuser)
            if profile_pic_url:
                admin.profile_pic = profile_pic_url
            admin.save()
            messages.success(request,"Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request,"Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
