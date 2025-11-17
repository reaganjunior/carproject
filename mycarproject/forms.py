from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Brand, Car, ContactMessage, Order, Admin


class RegisterForm(UserCreationForm):
    
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class OrderForm(forms.ModelForm):

    class Meta:
     model = Order
     fields = ['name', 'price', 'location', 'fuel_type', 'mileage', 'transmission', 'color', 'year','buyer_name','buyer_phone']
     

class BrandForm(forms.ModelForm):
     class Meta:
       model = Brand
       fields = '__all__'

class CarForm(forms.ModelForm):
    
    class Meta:
       model = Car
       fields = ['name', 'price', 'location', 'fuel_type', 'mileage', 'transmission', 'color', 'year', 'photo']
       
   



class ContactForm(forms.Form):
   
   
   full_name = forms.CharField(
      label="fullname",
      max_length=200,
      widget=forms.TextInput(attrs={'placeholder': 'fullname'})  
    )
   email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})  
    )
   subject = forms.CharField(
        label="Subject",
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Subject'})  
    )
   number = forms.CharField(
        label="Number",
        max_length=20,
        required=False,  
        widget=forms.TextInput(attrs={'placeholder': 'Number'}), 
    )
   message = forms.CharField(
        label="Write message",
        widget=forms.Textarea(attrs={'placeholder': 'Write your message here...'})
    
    )
   
   
class AdminForm(forms.Form):

    admin_password = forms.CharField( widget=forms.PasswordInput(attrs={'placeholder': 'Enter admin password'}) )
            