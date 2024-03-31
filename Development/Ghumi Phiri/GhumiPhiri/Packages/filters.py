from django import forms
import django_filters

from Packages.models import Package

class PackageFilter(django_filters.FilterSet):
    package_price = django_filters.RangeFilter(
        
    )

    class Meta:
        model = Package
        fields=['package_price']