from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    BUYER = 1
    TOUR_AGENCY = 2
    HOTEL =3
    
    ROLE_CHOICES = (
        (BUYER, 'Buyer'),
        (TOUR_AGENCY, 'Tour_Agency'),
        (HOTEL, 'Hotel'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(default="profile_pictures/default_picture.jpg", upload_to='profile_pictures/',null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username
