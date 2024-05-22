"""
URL configuration for zeta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from car_rental import views,AdminViews,Customerviews
from django.conf import settings

urlpatterns = [  
    path('admin/', admin.site.urls),
    path('',views.index, name="home"),
    path('index',views.index, name="index"),
    path('admin_home',AdminViews.admin_home,name="admin_home"),
    path('customer_home',Customerviews.customer_home,name="customer_home"),
    path('add_vehicle',AdminViews.add_vehicle,name="add_vehicle"),
    path('add_vehicle_save',AdminViews.add_vehicle_save,name="add_vehicle_save"),
    path('manage_vehicle',AdminViews.manage_vehicles,name="manage_vehicle"),
    path('earn_responses',AdminViews.earn_responses,name="earn_responses"),   
    path('hire_requests',AdminViews.hire_requests,name="hire_requests"),  
    path('new_fleet',AdminViews.new_fleet,name="new_fleet"), 
    path('tour_requests',AdminViews.tour_requests,name="tour_requests"),
    path('add_customer',AdminViews.add_customer,name="add_customer"),
    path('add_customer_save',AdminViews.add_customer_save,name="add_customer_save"),
    path('edit_customer/<str:customer_id>',AdminViews.edit_customer,name="edit_customer"),
    path('edit_customer_save',AdminViews.edit_customer_save,name="edit_customer_save"),
    path('manage_customer',AdminViews.manage_customer,name="manage_customer"),
    path('loginpage',views.loginPage,name="show_login"),
    path('login',views.Login,name="do_login"),
    path('get_user_details',views.GetUserDetails),
    path('logout',views.Logout,name="logout"),
    path('car',views.car, name="car"),
    path('tours',views.tours,name="tours"),
    path('about',views.about,name="about"),
    path('earn',Customerviews.earn,name="earn"),
    path('response',Customerviews.response,name="response"),
    path('hire_request',Customerviews.hire_request,name="hire_request"),
    path('tour_request',Customerviews.tour_request,name="tour_request"),
    path('grow',Customerviews.grow,name="grow"),
    path('buy',Customerviews.buy,name="buy"),
    path('policy',views.policy,name="policy"),
    path('book/<int:car_id>/', Customerviews.book_car, name='book_car'),
    path('return/<int:booking_id>/', AdminViews.return_car, name='return_car'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
