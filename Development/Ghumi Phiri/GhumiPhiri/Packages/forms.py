from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *

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

    package_price = forms.FloatField(
        label='Package Price',
        widget=forms.NumberInput(attrs={'placeholder': 'Package price', 'class': 'form-control'})
    )

    package_start_date = forms.DateField(
        label='Start date',
        widget=forms.TextInput(attrs={'type': 'date'})
    )
    
    package_end_date = forms.DateField(
        label='End date',
        widget=forms.TextInput(attrs={'type': 'date'})
    )

    package_locations = forms.CharField(
        label='Location',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Locations', 'class': 'form-control'})
    )
    
    package_activities = forms.CharField(
        label='Activities',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Activities', 'class': 'form-control'})
    )

    package_pic = forms.ImageField(
        label='Package Picture',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'type': 'file', 'name': 'package_pic'})
    )

    class Meta:
        model = Package
        fields = ['package_title', 'package_desc', 'package_price', 'package_start_date', 'package_end_date', 'package_locations', 'package_activities', 'package_pic']


class CreateCommentForm(ModelForm):
    comment = forms.CharField(
        label='Comment',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Comment', 'class': 'form-control'})
    )

    class Meta:
        model = Feedback
        fields = ["comment"]


class BookingForm(ModelForm):
    booking_date = forms.DateField(
        label='End date',
        widget=forms.TextInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Booking
        fields = ["booking_date"]