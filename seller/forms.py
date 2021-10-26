from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Seller_Details,Products,ProductImage,Brand
from customer.models import Orders

class UserForm(UserCreationForm):
    username = forms.CharField(max_length=15, widget=(
        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})))
    first_name = forms.CharField(max_length=15, widget=(
        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Firstname'})))

    password1 = forms.CharField(max_length=20, label="Password", widget=(
        forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})))
    password2 = forms.CharField(max_length=20, label="Confirm-Password", widget=(
        forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})))
    email = forms.CharField(max_length=100,
                            widget=(forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})))
    class Meta:
        model = User
        fields = ['first_name','username','email','password1','password2']

class ProfileForm(forms.ModelForm):

    address = forms.CharField(max_length=500,widget=(forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter address'})))
    bank_name = forms.CharField(max_length=50,
                             widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Bank Name'})))
    account_number = forms.CharField(max_length=50,
                                widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Account-Number'})))
    ifsc_code = forms.CharField(max_length=15,
                                     widget=(forms.TextInput( attrs={'class': 'form-control', 'placeholder': 'Enter IFSC Code'})))


    class Meta:
        model = Seller_Details
        fields = ['address','bank_name','account_number','ifsc_code']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, widget=(
        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class ProductAddForm(forms.ModelForm):

    class Meta:
        model = Products
        exclude = ('user',)

        category_options = [
            ('mobile','Mobile'),
            ('laptop','Laptop'),
            ('tablet','Tablet')
        ]
        
        # brand_names = [
        #     ('apple','Apple'),
        #     ('samsung', 'Samsung'),
        #     ('oneplus', 'OnePlus'),
        #     ('redmi','Redmi'),
        #     ('oppo', 'OPPO'),
        #     ('lenovo', 'Lenovo'),
        #     ('hp', 'HP'),
        #     ('dell', 'Dell'),
        #     ('azus', 'Azus'),
        #     
        #     
        # ]

        widgets = {
            'product_name':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(choices=category_options,attrs={'class':'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control',}),
            
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'ram': forms.TextInput(attrs={'class': 'form-control'}),
            'storage': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'offer': forms.NumberInput(attrs={'class': 'form-control'})
        }
        
        labels = {
            'product_name':'Product Name'
        }
class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['status']

class ImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        exclude = ('product',)

        widgets = {
            'images':forms.FileInput(attrs={'multiple':True})
        }
        
        
class BrandCreationForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = "__all__"
        widgets = {
            'brand_name':forms.TextInput(attrs={'class':'form-control'})
        }