from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg

from datetime import datetime

from Packages.forms import *
from Packages.models import *
from Packages.filters import PackageFilter

from star_ratings.models import Rating
from django.template.loader import render_to_string

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        packages = Package.objects.prefetch_related('packageimage_set').all()
        f = PackageFilter(
            request.GET, queryset=packages
        )

        context = {
            'packages': packages,
            'filter': f,
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
        package_list = Package.objects.prefetch_related('packageimage_set').all()
        package_filter = PackageFilter(request.GET)

        context = {
            'package_list': package_list,
            'package_filter': package_filter
        }
        return render(request, 'Packages/list_packages.html', context)
    
class ComparePackage(View):
    def get(self, request, *args, **kwargs):
        package_list = Package.objects.all()
        package_filter = PackageFilter(request.GET)

        package1_id = request.GET.get('package1')
        package2_id = request.GET.get('package2')
        package1 = get_object_or_404(Package.objects.prefetch_related('packageimage_set'), pk=package1_id)
        package2 = get_object_or_404(Package.objects.prefetch_related('packageimage_set'), pk=package2_id)

        package1_author = {'id': package1.package_author.id, 'username': package1.package_author.username}
        package2_author = {'id': package2.package_author.id, 'username': package2.package_author.username}

        package1_image_url = package1.packageimage_set.first().images.url
        package2_image_url = package2.packageimage_set.first().images.url
    
        data = {
                'package1': {
                    'id': package1.id,
                    'title': package1.package_title,
                    'author': package1_author.get('username'),
                    'location': package1.package_locations,
                    'duration': package1.package_duration,
                    'desc': package1.package_desc,
                    'price': package1.package_price,
                    'image_url': package1_image_url,
                },
                'package2': {
                    'id': package2.id,
                    'title': package2.package_title,
                    'author': package2_author.get('username'),
                    'location': package2.package_locations,
                    'duration': package2.package_duration,
                    'desc': package2.package_desc,
                    'price': package2.package_price,
                    'image_url': package2_image_url,
                }
            }
        return JsonResponse(data)
        
    

class PackageDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        package = Package.objects.get(pk=pk)
        package_images = PackageImage.objects.filter(package=package)
        feedbacks = Feedback.objects.filter(package=package).order_by('-created_on')

        user = request.user

        comment_form = CreateCommentForm()
        booking_form = BookingForm(request.POST)
        user_booking_date_str = request.GET.get('booking_date')

        

        # add_feedback = True
        # if request.user.is_authenticated:
        #     user_feedback_count = Feedback.objects.filter(feedback_author = request.user, package = package).count()
        #     if user_feedback_count > 0:
        #         add_feedback = False
        
        context = {
            'package': package,
            'package_images': package_images,
            'feedbacks': feedbacks,
            'comment_form': comment_form,
            'booking_form': booking_form,
            'booking_date': user_booking_date_str
            # 'add_feedback': add_feedback
        }

        if package.favourites.filter(id=user.id).exists():
            context["is_favourite"] = False
        else:
            context["is_favourite"] = True

        return render(request, 'Packages/package_detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        package = Package.objects.get(pk=pk)
        bookings = Booking.objects.filter(package=package)

        existing_booking_dates=list(Booking.objects.filter(package=package).values_list('booking_date', flat=True))

        comment_form = CreateCommentForm(request.POST)
        booking_form = BookingForm(request.POST)

        context = {
            'package': package,
            'form': comment_form,
            'booking_form': booking_form,
        }

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
            user_booking_date_str = request.POST.get('booking_date')
            user_booking_date = datetime.strptime(user_booking_date_str, "%Y-%m-%d").date()
            if user_booking_date in existing_booking_dates:
                print('cannot book')
                return redirect(reverse('package_detail', kwargs={'pk': pk}) + '?bookingError=true')
            # if booking_form.is_valid():
            #     new_booking = booking_form.save(commit=False)
            #     new_booking.booked_by = request.user
            #     new_booking.package = package
            #     booking_form.save()
            #     context['booking_date_available'] = True
            #     print("Booking successful")
            else:
                context['booking_date_available'] = True
                context['booking_date'] = user_booking_date_str
        return render(request, 'Packages/package_detail.html', context)

        
class FavouritePackageView(View):
    def post(self, request, pk, *args, **kwargs):
        package = Package.objects.get(pk=pk)
        user = request.user
        if package.favourites.filter(id=user.id).exists():
            package.favourites.remove(request.user)
            messages.error(request, f"Removed from favourites.")
        else:
            package.favourites.add(request.user)
            messages.success(request, f"Added to favourites.")
        return HttpResponseRedirect(reverse('package_detail', kwargs={'pk': pk}))
    

class WriteReview(View):
    def post(self, request, pk, *args, **kwargs):
        package = Package.objects.get(pk=pk)
        user = request.user

        feedback = Feedback.objects.create(
            feedback_author=user,
            package = package,
            comment = request.POST.get('comment'),
            rating = request.POST.get('raitng')
        )

        context = {
            'user': user.username,
            'comment': request.POST.get('comment'),
            'rating': request.POST.get('raitng'),
            'date': request.POST.get('created_on')
        }

        return JsonResponse(
            {
                'bool': True,
                'context': context
            }
        )

class ListSellerPackages(View):
    def get(self, request, pk, *args, **kwargs):
        profile = User.objects.get(pk=pk)
        packages = Package.objects.prefetch_related('packageimage_set').filter(package_author=profile)
        form = ImageForm()

        context = {
            'packages': packages,
            'form': form,
        }
        return render(request, 'Packages/seller_packages.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        profile = User.objects.get(pk=pk)
        packages = Package.objects.filter(package_author=profile)
        
        form = ImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')

        if form.is_valid():
            new_package = form.save(commit=False)
            new_package.package_author = profile
            new_package.save()
            print("Package created")

            for file in files:
                package_image = PackageImage(package=new_package, images=file)
                package_image.save()
        else:
            print(form.errors)

        context = {
            'packages': packages,
            'form': form,
        }

        return render(request, 'Packages/seller_packages.html', context)
    
class ListPaymentDetails(View):
    def get(self, request, *args, **kwargs):
        user = request.user

        headers = [
            'S no.',
            'Package Title',
            'Booked By',
            'Paid Amount',
            'Booked date',
        ]

        booking_list = Package.objects.prefetch_related('package').filter(package_author=user).values('package__package__package_title', 'package__booked_by__username', 'package__paid_amount', 'package__booking_date')

        context = {
            'headers': headers,
            'booking_list': booking_list
        }

        return render(request, 'packages/payment_details.html', context)