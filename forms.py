
from django.forms import ImageField, ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _






sizes = Size.objects.all()
categorys = Category.objects.all()
genders = Gender.objects.all()


class loginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2']
        




class SellForm(ModelForm):
    class Meta:
        model = Product
        fields = ['pointure', 'category', 'name', 'price', 'gender', 'size','publisher', 'description', 'image', 'is_delivering', 'show_info']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', }),
            
            'size': forms.Select(attrs={'class': 'custom-select', }, choices=sizes),
            'category': forms.Select(attrs={'class': 'custom-select', }, choices=categorys),
            
            'price': forms.TextInput(attrs={'class': 'form-control', }),
            'pointure': forms.TextInput(attrs={'class': 'form-control', }),
            'gender': forms.Select(attrs={'class': 'custom-select', }, choices=genders),
            'publisher':forms.TextInput(attrs={'class': 'form-control', }),
            'description':forms.Textarea(attrs={'class': 'form-control', }),
            'is_delivering':forms.CheckboxInput(),
            'show_info':forms.CheckboxInput(),

            
        }
        labels = {
            'name': _('Name'),
            'publisher': _('Publisher'),
            'size': _('Size'),
            'category': _('Category'),
            'price': _('Price'),
            'gender': _('Gender'),
            
        }









class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    class Meta :
        model = User
        fields = ("email", "first_name", "last_name", "username", "password1", "password2")

class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', }),
            
            'first_name': forms.TextInput(attrs={'class': 'form-control', }),
            'last_name': forms.TextInput(attrs={'class': 'form-control', }),
            
            'email': forms.EmailInput(attrs={'class': 'form-control', }),
            'password': forms.PasswordInput(attrs={'class': 'form-control', }),
            
        }
        labels = {
            'username': _('Username'),
            
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            
            'email': _('Email'),
            'password': _('Password'),
            
        }
        error_messages = {
            'username': {
                'unique': _('The username is not available')
            },
            'first_name': {
                'required': _('The field can not be empty')
            },
            'last_name': {
                'required': _('The field can not be empty')
            },
            'password': {
                'required': _('The field can not be empty')
            }

        } 
