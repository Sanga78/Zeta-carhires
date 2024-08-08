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
from django.contrib.auth.decorators import login_required
# Create your views here.
def customer_home(request):
    return render(request,'index.html')

@login_required
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

def pay(request):
    return render(request,'pay.html')

def update_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    customer = Customer.objects.get(admin=user)
    return render(request, "profile.html",{"user":user,"customer":customer})

def profile_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        profile_pic_url = None
        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

        try:
            user = CustomUser.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            customer = Customer.objects.get(admin=user)
            customer.address = address
            if profile_pic_url:
                customer.profile_pic = profile_pic_url
            customer.save()

            # Send profile update notification email
            subject = 'Profile Updated'
            html_message = render_to_string('emails/profile_update_notification.html', {'customer_name': user.username})
            plain_message = strip_tags(html_message)
            from_email = 'your-email@gmail.com'
            to = customer.admin.email

            send_mail(subject, plain_message, from_email, [to], html_message=html_message)

            del request.user.id
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("update_profile"))  # Redirect to the index page after successful update
        except CustomUser.DoesNotExist:
            messages.error(request, "Failed to Update Profile: User not found")
            return HttpResponseRedirect(reverse("index"))
        except Exception as e:
            messages.error(request, f"Failed to Update Profile: {str(e)}")
            return HttpResponseRedirect(reverse("index"))

def booked_cars_list(request):
    user = request.user
    if user.is_authenticated:
        bookings = Booking.objects.filter(customer_name__admin=user)
        return render(request, 'my_bookings.html', {'bookings': bookings})
    else:
        messages.error(request,"Make sure you are registered")
        return HttpResponseRedirect(reverse("index"))