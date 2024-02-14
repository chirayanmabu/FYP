from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    # username = models.CharField(max_length=200)
    # first_name = models.CharField(max_length=30, null=True, blank=True)
    # last_name = models.CharField(max_length=30, null=True, blank=True)
    # email=models.CharField(max_length=200)
    phone = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(default="profile_pictures/default_picture.jpg", upload_to='profile_pictures/',null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])

    # def __str__(self):
    #     return self.username

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



class Feedback(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    feedback_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.comment


# class Booking(models.Model):
#     booked_by = models.ForeignKey(User, on_delete=models.CASCADE)


