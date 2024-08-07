from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractUser):
    user_type_data = ((1,"Dealer"),(2,"Customer"))
    user_type = models.CharField(default=1,choices=user_type_data,max_length=10)

class CarDealer(models.Model):
    id = models.AutoField(primary_key=True)
    profile_pic = models.FileField(default='static/images/person_1.jpg')
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    profile_pic = models.FileField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects= models.Manager()  

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    car_name = models.CharField(max_length = 20)
    car_image = models.ImageField(default='static/car-1.png',upload_to='vehicle_images',blank=True,null=True)
    color = models.CharField(max_length = 10)
    capacity = models.CharField(max_length = 2)
    price = models.FloatField()
    is_available = models.BooleanField(default = True)
    description = models.CharField(max_length = 100)
    objects = models.Manager()

    def __str__(self):
        return self.car_name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
class Responses(models.Model):
    customer_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.IntegerField()
    message = models.CharField(max_length=300)
    def __str__(self):
        return str(self.email)   

class Booking(models.Model):
    car = models.ForeignKey(Vehicle, on_delete=models.SET_NULL,null=True, blank=True)
    customer_name = models.ForeignKey(Customer,on_delete= models.SET_NULL,null=True, blank=True)
    booking_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)
    total_cost = models.FloatField(null=True, blank=True)
    def __str__(self):
        return f"{self.customer_name} - {self.car.car_name}"


class CarImage(models.Model):
    image = models.ImageField(upload_to='car_images/')

class Car(models.Model):
    model = models.CharField(max_length=100)
    price = models.CharField(max_length=20)
    description = models.TextField()
    colors = models.CharField(max_length=100)
    seats = models.IntegerField()
    main_image = models.ImageField(upload_to='cars/')
    additional_images = models.ManyToManyField(CarImage, related_name='cars')
       
class Hire_Request(models.Model):
    full_name = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    car_id = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    rented_on = models.DateTimeField(auto_now_add=True)
    rented_to = models.DateTimeField(auto_now_add=True)
    objects= models.Manager()
    def __str__(self):
        return str(self.full_name)   

class Tours_request(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.IntegerField()
    message = message = models.TextField()
    objects= models.Manager()
    def __str__(self):
        return str(self.email)  
    
class Fleet(models.Model):
    full_name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.IntegerField()
    no_of_cars = models.IntegerField()
    objects= models.Manager()
    def __str__(self):
        return str(self.email) 
      
@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            CarDealer.objects.create(admin=instance)  
        if instance.user_type==2:
            Customer.objects.create(admin=instance,address="",profile_pic="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,created,**kwargs):
    if instance.user_type==1:
        instance.cardealer.save()
    if instance.user_type==2:
        instance.customer.save()    
