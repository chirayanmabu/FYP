from django import forms
import django_filters
from django_filters.widgets import RangeWidget

from core.models import UserProfile
from Packages.models import Package
from star_ratings.models import Rating

RATING_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5')
)


class PackageFilter(django_filters.FilterSet):
    package_price = django_filters.RangeFilter(
        widget=RangeWidget(attrs={'class': 'test-range-filter'})
    )
    package_locations = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'type': 'input', 'class': 'form-control', 'placeholder': 'Search for locations'})
    )
    package_duration = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'type': 'input', 'class': 'form-control', 'placeholder': 'Search for duration'})
    )
    package__rating_average = django_filters.ChoiceFilter(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )

    class Meta:
        model = Package
        fields=['package_price', 'package_locations', 'package_duration', 'package__rating_average']


class SellerFilter(django_filters.FilterSet):
    address = django_filters.CharFilter(
        widget=forms.TextInput(attrs={'type': 'input', 'class': 'form-control', 'placeholder': 'Search for locations'})
    )

    class Meta:
        model = UserProfile
        fields=['address']

