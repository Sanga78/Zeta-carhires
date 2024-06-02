from django.shortcuts import render, get_object_or_404, redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .models import *
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .forms import UpdateProfileForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
            customer = get_object_or_404(Customer, admin=customer_id)
            Booking.objects.create(car=car, customer_name=customer)
            car.is_available = False
            car.save()

            # Send booking confirmation email
            subject = 'Booking Confirmation'
            booking_link = request.build_absolute_uri(reverse('booked_cars_list'))
            html_message = render_to_string('emails/booking_confirmation.html', {'customer_name': customer.admin.username, 'car_name': car.car_name, 'booking_link': booking_link})
            plain_message = strip_tags(html_message)
            from_email = 'zetacarhires@gmail.com'
            to = customer.admin.email

            send_mail(subject, plain_message, from_email, [to], html_message=html_message)

            return redirect('car')
        return render(request, 'book_car.html', {'car': car})
    else:
        return HttpResponse(f"Car is not available. Please call +123456789 for more information.")

def update_profile(request, customer_id):
    request.session['customer_id'] = customer_id
    customer = get_object_or_404(Customer, admin=customer_id)
    form = UpdateProfileForm(initial={
        'email': customer.admin.email,
        'first_name': customer.admin.first_name,
        'last_name': customer.admin.last_name,
        'username': customer.admin.username,
        'address': customer.address
    })
    return render(request, "profile.html", {"form": form, "id": customer_id, "username": customer.admin.username})

def profile_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")

    customer_id = request.session.get("customer_id")
    if not customer_id:
        return HttpResponseRedirect(reverse("update_profile", kwargs={"customer_id": customer_id}))

    form = UpdateProfileForm(request.POST, request.FILES)
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
            user = CustomUser.objects.get(id=customer_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

            customer = Customer.objects.get(admin=customer_id)
            customer.address = address
            if profile_pic_url:
                customer.profile_pic = profile_pic_url
            customer.save()

            # Send profile update notification email
            subject = 'Profile Updated'
            html_message = render_to_string('emails/profile_update_notification.html', {'customer_name': customer.admin.username})
            plain_message = strip_tags(html_message)
            from_email = 'your-email@gmail.com'
            to = customer.admin.email

            send_mail(subject, plain_message, from_email, [to], html_message=html_message)

            del request.session['customer_id']
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("index"))  # Redirect to the index page after successful update
        except CustomUser.DoesNotExist:
            messages.error(request, "Failed to Update Profile: User not found")
        except Exception as e:
            messages.error(request, f"Failed to Update Profile: {str(e)}")

    customer = get_object_or_404(Customer, admin=customer_id)
    return render(request, "profile.html", {"form": form, "id": customer_id, "username": customer.admin.username})
def booked_cars_list(request):
    user = request.user
    if user.is_authenticated:
        bookings = Booking.objects.filter(customer_name__admin=user)
        return render(request, 'my_bookings.html', {'bookings': bookings})
    else:
        messages.error(request,"Make sure you are registered")
        return HttpResponseRedirect(reverse("index"))