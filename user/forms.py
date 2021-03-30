from django import forms
from app.models import Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#form for registration
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

#form for create a new order
class NewOrder(forms.ModelForm):
    price = forms.CharField(max_length=10)
    quantity = forms.CharField(max_length=10)

    class Meta:
        model = Order
        fields = ['price', 'quantity']

