from django import forms
from .models import Car, CarImage

class DateInput(forms.DateInput):
    input_type = "date"

class AddCustomerForm(forms.Form):
    email = forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Picture",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"})) 

class EditCustomerForm(forms.Form):
    email = forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Picture",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False) 

class UpdateProfileForm(forms.Form):
    email = forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Picture",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False) 

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['model', 'price', 'description', 'colors', 'seats', 'main_image', 'additional_images']

class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image']
