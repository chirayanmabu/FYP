from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from Packages.forms import *
from Packages.models import *

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        packages = Package.objects.all()

        context = {
            'packages': packages
        }

        return render(request, 'core/index.html', context)

class CreatePackageView(View):
    def get(self, request, *args, **kwargs):
        form = CreatePackageModelForm()
        context = {
            'form': form
        }
        return render(request, 'Packages/create_package.html', context)

    def post(self, request, *args, **kwargs):
        form = CreatePackageModelForm(request.POST, request.FILES)
        if form.is_valid():
            new_package = form.save(commit=False)
            new_package.package_author = request.user
            new_package.save()
            print("Package created")
        else:
            print(form.errors)

        context = {
            'form': form
        }
        return render(request, 'Packages/create_package.html', context)
    

class ListPackageView(View):
    def get(self, request, *args, **kwargs):
        package_list = Package.objects.all()
        context = {
            'package_list': package_list
        }
        return render(request, 'Packages/list_packages.html', context)
    

class PackageDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        package = Package.objects.get(pk=pk)
        package_images = PackageImage.objects.filter(package=package)
        feedbacks = Feedback.objects.filter(package=package).order_by('-created_on')
        
        context = {
            'package': package,
            'package_images': package_images,
            'feedbacks': feedbacks
        }

        return render(request, 'Packages/package_detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        package = Package.objects.get(pk=pk)
        # bookings = Booking.objects.filter(package=package.package_title)
        comment_form = CreateCommentForm(request.POST)
        booking_form = BookingForm(request.POST)

        if 'post_comment' in request.POST:
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.feedback_author = request.user
                new_comment.package = package
                new_comment.save()
                print("Posted review")

            else:
                print(comment_form.errors())
        elif 'book_package' in request.POST:
            if booking_form.is_valid():
                new_booking = booking_form.save(commit=False)
                new_booking.booked_by = request.user
                new_booking.package = package
                booking_form.save()
                print("Booking successful")
            else:
                print(booking_form.errors())

        context = {
            'package': package,
            'form': comment_form,
            'booking_form': booking_form,
        }

        return render(request, 'Packages/package_detail.html', context)