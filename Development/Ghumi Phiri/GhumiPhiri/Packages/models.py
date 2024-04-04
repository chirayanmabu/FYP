from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone

from core.models import User

class Package(models.Model):
    package_author = models.ForeignKey(User, on_delete=models.CASCADE)
    package_title = models.CharField(max_length=50)
    package_desc = models.CharField(max_length=200, null=True, blank=True)
    package_price = models.FloatField(null=True, blank=True)
    package_start_date = models.DateField(null=True, blank=True)
    package_end_date = models.DateField(null=True, blank=True)
    package_locations = models.CharField(max_length=50, null=True, blank=True)
    package_activities = models.CharField(max_length=50, null=True, blank=True)
    package_pic = models.ImageField(upload_to='package_pictures/', null=True, blank=True)
    

    def __str__(self):
        return self.package_title


class PackageImage(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='package_pictures/', null=True, blank=True)


class Feedback(models.Model):
    RATING_RANGE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    )
    created_on = models.DateTimeField(default=timezone.now)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    feedback_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(choices = RATING_RANGE, blank=True, null=True)

    def __str__(self):
        return self.comment


class Booking(models.Model):
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='package')
    booking_date = models.DateField(null=True, blank=True)