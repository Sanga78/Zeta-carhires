from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .models import *
from django.urls import reverse
from django.utils import timezone

# Create your views here.
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
    return render(request,'buy.html')

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

# def rent_vehicle(request):
#     id = request.POST['id']
#     vehicle = Vehicle.objects.get(id = id)
#     cost_per_day = int(vehicle.capacity)*13
#     return render(request, 'customer/confirmation.html', {'vehicle':vehicle, 'cost_per_day':cost_per_day})
     
# def confirm(request):
#     vehicle_id = request.POST['id']
#     username = request.user
#     user = CustomUser.objects.get(username = username)
#     days = request.POST['days']
#     vehicle = Vehicle.objects.get(id = vehicle_id)
#     if vehicle.is_available:
#         car_dealer = vehicle.dealer
#         rent = (int(vehicle.capacity))*13*(int(days))
#         car_dealer.wallet += rent
#         car_dealer.save()
#         try:
#             order = Order(vehicle = vehicle, car_dealer = car_dealer, user = user, rent=rent, days=days)
#             order.save()
#         except:
#             order = Order.objects.get(vehicle = vehicle, car_dealer = car_dealer, user = user, rent=rent, days=days)
#         vehicle.is_available = False
#         vehicle.save()
#         return render(request, 'customer/confirmed.html', {'order':order})
#     else:
#         return render(request, 'customer/order_failed.html')

def customer_home(request):
    return render(request,'index.html')

def book_car(request, car_id):
    car = get_object_or_404(Vehicle, id=car_id)
    if car.is_available:
        if request.method == 'POST':
            customer_id = request.POST.get('customer_id')
            customer_name = Customer.objects.get(admin=customer_id)
            Booking.objects.create(car=car, customer_name=customer_name)
            car.is_available = False
            car.save()
            return redirect('car')
        return render(request, 'bookings/book_car.html', {'car': car})
    else:
        return HttpResponse(f"Car is not available. Please call +123456789 for more information.")
