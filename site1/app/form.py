
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer, Product

class Register(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['username', 'password']
        widgets = {
            'password': forms.TextInput(attrs={'autocomplete': 'off'}),
        }


class Login(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'autocomplete': 'off'}),
        }


class CreateProduct(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product', 'price', 'image']