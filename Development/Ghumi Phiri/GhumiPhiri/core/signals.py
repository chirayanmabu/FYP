from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.models import Group

def user_profile(sender, instance, created, **kwargs):
    if created: 
        group = Group.objects.get(name="normal_user")
        instance.groups.add(group)

        UserProfile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
        )
        print('Profile Created')

post_save.connect(user_profile, sender=User)