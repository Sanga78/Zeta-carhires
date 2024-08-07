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

def update_profile(request, customer_id):
    request.session['customer_id'] = customer_id
    customer = get_object_or_404(Customer, admin=customer_id)
    context={
        "id": customer_id,
        'email': customer.admin.email,
        'first_name': customer.admin.first_name,
        'last_name': customer.admin.last_name,
        'username': customer.admin.username,
        'address': customer.address,
        'profile_pic': customer.profile_pic
    }
    return render(request, "profile.html", context)

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