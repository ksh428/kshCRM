from django.forms import ModelForm
from .models import Order,Customer
from django.contrib.auth.forms import UserCreationForm #default form
from django import forms
from django.contrib.auth.models import User


class CustomerForm(ModelForm):# for updating customer info from settings
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']

class OrderForm(ModelForm):
	class Meta:
		model=Order
		fields='__all__' #use all fields


class CreateUserForm(UserCreationForm):
	class Meta:
		model=User
		fields=['username','email','password1','password2']