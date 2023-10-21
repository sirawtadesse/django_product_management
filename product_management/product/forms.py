from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ProductItem

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()

    class Meta:
        model=User
        fields=['username','email','password1', 'password2']

class ProductItemForm(forms.ModelForm):
    class Meta:
        model=ProductItem
        fields=['name', 'description', 'price', 'quantity_in_stock']