from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone

from core.models import User

class Package(models.Model):
    package_author = models.ForeignKey(User, on_delete=models.CASCADE)
    package_title = models.CharField(max_length=50)
    package_desc = models.CharField(max_length=200, null=True, blank=True)
    package_price = models.FloatField(null=True, blank=True)
    package_duration = models.CharField(null=True, blank=True)
    package_locations = models.CharField(max_length=50, null=True, blank=True)
    package_activities = models.CharField(max_length=50, null=True, blank=True)

    favourites = models.ManyToManyField(User, related_name='favourites', blank=True)
    
    def __str__(self):
        return self.package_title


class PackageImage(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='package_pictures/', null=True, blank=True)


class Feedback(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    feedback_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.comment


class PaymentStatus(models.TextChoices):
    INITIATED = '1'
    COMPLETED = '2'
    FAILED = '3'

class Booking(models.Model):
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='package')
    booking_date = models.DateField(null=True, blank=True)
    paid_amount = models.FloatField(null=True, blank=True)
    status = models.CharField(choices=PaymentStatus.choices, max_length=15, default=PaymentStatus.INITIATED)

    def __str__(self):
        return f"{self.package} booked by {self.booked_by} - {self.booking_date}"