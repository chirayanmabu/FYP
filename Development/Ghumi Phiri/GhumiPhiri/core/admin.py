from django.contrib import admin

from .models import *

admin.site.register(UserProfile)
admin.site.register(Package)
admin.site.register(Feedback)
admin.site.register(Booking)
