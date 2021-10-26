from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Userdetails,Address,Orders


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={"class": "form-control"}))

class UpdateForm(ModelForm):
    class Meta:
        model = Userdetails
        fields = ["first_name",'last_name',"mobile_number","dob","image"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "mobile_number": forms.TextInput(attrs={"class": "form-control"}),
            "dob": forms.DateInput(attrs={"class": "form-control", "placeholder": "yyyy-mm-dd"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }

class ReviewForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea())
    

class PlaceOrderForm(forms.Form):

    # address=forms.ChoiceField(widget=forms.Select(attrs={'class':"form-select"}))
    # a ddress = forms.ModelChoiceField(queryset=Address.objects.all() ,empty_label='Select Address',widget=forms.Select(attrs={'class':'form-select'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}))
    product=forms.CharField(widget=forms.TextInput(attrs={'class':"form-control"}))




class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email"]
        widgets={
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),

        }
