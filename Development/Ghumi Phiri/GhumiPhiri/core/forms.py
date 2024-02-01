from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *


class CreateUserForm(UserCreationForm):
    username = forms.CharField(
        label = 'Username',
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})
    )
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'form-control'})
    )
    first_name = forms.CharField(
        label='',
        required=False,
        min_length=2, max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='',
        required=False,
        min_length=2, max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'})
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class ProfileForm(ModelForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    profile_pic = forms.ImageField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'file'})
    )
    
    phone = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'type': 'number'})
    )
    address = forms.CharField(
        label='',
        min_length=2, max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Address'})
    )
    dob = forms.DateField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'type': 'date'})
    )
    gender = forms.ChoiceField(
        label='',
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = UserProfile
        fields = '__all__'
        # exclude = ['user']


class UpdateProfileForm(forms.Form):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    username = forms.CharField(
        label = 'Username',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'})
    )
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'})
    )
    first_name = forms.CharField(
        label='',
        required=False,
        min_length=2, max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='',
        required=False,
        min_length=2, max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'})
    )
    profile_pic = forms.ImageField(
        label='',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file'})
    )
    
    phone = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'type': 'number'})
    )
    address = forms.CharField(
        label='',
        min_length=2, max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Address'})
    )
    dob = forms.DateField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'type': 'date'})
    )
    gender = forms.ChoiceField(
        label='',
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def save(self):
        user_id = self.initial.get('user_id')
        user_data=self.cleaned_data

        profile = UserProfile.objects.get(pk=user_id)
        user = profile.user

        user.username = user_data.get("username", user.username)
        user.email = user_data.get("email", user.email)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)

        profile.phone = user_data.get("phone", profile.phone)
        profile.address = user_data.get("address", profile.address)
        profile.gender = user_data.get("gender", profile.gender)
        profile.phone = user_data.get("phone", profile.phone)
        profile.dob = user_data.get("dob", profile.dob)
        profile.profile_pic = user_data.get("profile_pic", profile.profile_pic)

        user.save()
        profile.save()

        print(user_data)    
        print(user_id)


class CreatePackageForm(forms.Form):
    package_title = forms.CharField(
        label='',
        min_length = 3,
        max_length = 50,
        widget=forms.TextInput(attrs={'placeholder': 'Package title', 'class': 'form-control'})
    )
    
    package_desc = forms.CharField(
        label='',
        min_length = 3,
        max_length = 100,
        widget=forms.TextInput(attrs={'placeholder': 'Package title', 'class': 'form-control'})
    )

class CreatePackageModelForm(ModelForm):
    package_title = forms.CharField(
        label='Package title',
        min_length = 3,
        max_length = 50,
        widget=forms.TextInput(attrs={'placeholder': 'Package title', 'class': 'form-control'})
    )
    
    package_desc = forms.CharField(
        label='Package description',
        min_length = 2,
        max_length = 100,
        widget=forms.TextInput(attrs={'placeholder': 'Package description', 'class': 'form-control'})
    )

    class Meta:
        model = Package
        fields = ['package_title', 'package_desc']





        
