from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

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
        widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control', 'rows': '3'})
    )

    package_price = forms.FloatField(
        label='Package Price',
        widget=forms.NumberInput(attrs={'placeholder': 'Package price', 'class': 'form-control'})
    )

    package_duration = forms.CharField(
        label='Duration',
        widget=forms.TextInput(attrs={'placeholder': 'Duration', 'class': 'form-control'})
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

    def clean_package_price(self):
        package_price = self.cleaned_data.get('package_price')
        if package_price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return package_price

    class Meta:
        model = Package
        fields = ['package_title', 'package_desc', 'package_price', 'package_duration', 'package_locations', 'package_activities']


class ImageForm(CreatePackageModelForm):
    images = forms.FileField(
        label='Image',
        widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True, 'class': 'form-control', 'name': 'images', 'type': 'file'})
    )

    class Meta(CreatePackageModelForm.Meta):
        models = PackageImage
        fields = CreatePackageModelForm.Meta.fields + ['images']


class CreateCommentForm(ModelForm):
    comment = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Add a comment...', 'class': 'form-control', 'rows': '3'})
    )

    class Meta:
        model = Feedback
        fields = ["comment"]


class BookingForm(ModelForm):
    booking_date = forms.DateField(
        label='End date',
        widget=forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )

    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date < timezone.now().date():
            raise forms.ValidationError("Booking date cannot be in the past.")
        return booking_date

    class Meta:
        model = Booking
        fields = ["booking_date"]