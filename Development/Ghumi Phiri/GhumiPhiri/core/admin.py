from django.contrib import admin

from .models import *

admin.site.register(UserProfile)
admin.site.register(Feedback)
admin.site.register(Booking)


class PackageImageAdmin(admin.StackedInline):
    model=PackageImage

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    inlines = [PackageImageAdmin]

    class Meta:
        model = Package

@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    pass