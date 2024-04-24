from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Sum, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta

from core.mixins import GroupRequiredMixin
from core.models import UserProfile

from Packages.forms import *
from Packages.models import *
from Packages.filters import PackageFilter, SellerFilter

from star_ratings.models import Rating
from django.template.loader import render_to_string

from django.core.exceptions import PermissionDenied


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        packages = Package.objects.prefetch_related('packageimage_set').all()
        sellers = User.objects.filter(role=2)
        f = PackageFilter(
            request.GET, queryset=packages
        )

        seller_filter = SellerFilter(request.GET, queryset=sellers)

        context = {
            'packages': packages,
            'filter': f,
            'seller_filter': seller_filter,
            'user': request.user
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
        package_filter = PackageFilter(request.GET, queryset=package_list)

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

        context = {
            'package': package,
            'package_images': package_images,
            'feedbacks': feedbacks,
            'comment_form': comment_form,
            'booking_form': booking_form,
            'booking_date': user_booking_date_str
        }

        if package.favourites.filter(id=user.id).exists():
            context["is_favourite"] = False
        else:
            context["is_favourite"] = True

        if user.is_authenticated:
            if Feedback.objects.filter(package=package, feedback_author=user).exists():
                context["user_has_reviewed"] = True
            else:
                context["user_has_reviewed"] = False

            if Booking.objects.filter(package=package, booked_by=user).exists():
                context["user_has_booked"] = True
            else:
                context["user_has_booked"] = False

        return render(request, 'Packages/package_detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        try:
            logged_in_user = request.user
        except:
            messages.error(request, f"Please log in to your account to use this feature.")

        package = Package.objects.get(pk=pk)
        package_images = PackageImage.objects.filter(package=package)
        feedbacks = Feedback.objects.filter(package=package).order_by('-created_on')

        bookings = Booking.objects.filter(package=package)

        existing_booking_dates=list(Booking.objects.filter(package=package).values_list('booking_date', flat=True))

        comment_form = CreateCommentForm(request.POST)
        booking_form = BookingForm(request.POST)

        context = {
            'package': package,
            'package_images': package_images,
            'feedbacks': feedbacks,
            'comment_form': comment_form,
            'booking_form': booking_form,
        }

        if 'post_comment' in request.POST:
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.feedback_author = logged_in_user
                new_comment.package = package
                new_comment.save()
                print("Posted review")
                messages.success(request, f"Your review has been posted.")

            else:
                messages.error(request, f"Invalid input.")
                print(comment_form.errors())

        elif 'book_package' in request.POST:
            user_booking_date_str = request.POST.get('booking_date')
            user_booking_date = datetime.strptime(user_booking_date_str, "%Y-%m-%d").date()
            if user_booking_date in existing_booking_dates:
                messages.error(request, f"The chosen booking date is not available.")
            else:
                if booking_form.is_valid():
                    if request.user.is_authenticated:
                        messages.success(request, f"The chosen booking date is available. Proceed to checkout.")
                    else:
                        messages.warning(request, f"The chosen booking date is available. Please log in to checkout.")
                    context['booking_date_available'] = True
                    context['booking_date'] = user_booking_date_str
                else:
                    messages.error(request, f"Booking date cannot be in the past.")
            
        return render(request, 'Packages/package_detail.html', context)


class EditDeleteFeedbackView(View):
    def post(self, request, pk, *args, **kwargs):
        feedback_instace = get_object_or_404(Feedback, pk=pk)
        package_id = feedback_instace.package.id
        url = reverse('package_detail', kwargs={"pk": package_id})
        if "update_feedback" in request.POST:
            form = CreateCommentForm(request.POST, instance=feedback_instace)
            if form.is_valid():
                messages.success(request, "Feedback edited successfully.")
                form.save()
                return HttpResponseRedirect(url)
            else:
                messages.error(request, "Invalid input.")
                return HttpResponseRedirect(url)
        elif "delete_feedback" in request.POST:
            feedback_instace.delete()
            messages.success(request, "Feedback deleted.")
            return HttpResponseRedirect(url)

        
class FavouritePackageView(View):
    def post(self, request, pk, *args, **kwargs):
        try:
            package = Package.objects.get(pk=pk)
            user = request.user
            if package.favourites.filter(id=user.id).exists():
                package.favourites.remove(request.user)
                messages.error(request, f"Removed from favourites.")
            else:
                package.favourites.add(request.user)
                messages.success(request, f"Added to favourites.")
            return HttpResponseRedirect(reverse('package_detail', kwargs={'pk': pk}))
        except Exception:
            messages.error(request, f"Please register as a user for this functionality.")
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
    

class ListSellerView(View):
    def get(self, request, *args, **kwargs):
        # seller_users = User.objects.filter(role=User.SELLER)
        sellers_qs = UserProfile.objects.filter(user__role=2)
        seller_filter = SellerFilter(request.GET, queryset=sellers_qs)

        sellers=seller_filter.qs

        context = {
            'sellers': sellers,
            'filter': seller_filter
        }

        return render(request, 'Packages/list_sellers.html', context)


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

        context = {
            'packages': packages,
            'form': form,
        }

        if len(files) != 5:
            messages.error(request, f'Please upload exactly five images.')
            return render(request, 'Packages/seller_packages.html', context)
        if form.is_valid():
            new_package = form.save(commit=False)
            new_package.package_author = profile
            new_package.save()
            messages.success(request, "Package added successfully.")
            print("Package created")

            for file in files:
                package_image = PackageImage(package=new_package, images=file)
                package_image.save()
        else:
            if "images" in form.errors:
                messages.error(request, f'Please upload exactly five images.')
            else:
                messages.error(request, f'Invalid input for {list(form.errors)[0]}.')
            print(form.errors)
        return render(request, 'Packages/seller_packages.html', context)
    

class ManageSellerPackages(View):
    def post(self, request, pk, *args, **kwargs):
        package_instance = get_object_or_404(Package, pk=pk)
        url = reverse("my_packages", kwargs={"pk": package_instance.package_author.id})
        if "update_package" in request.POST:
            form = ImageForm(request.POST, request.FILES, instance=package_instance)
            files = request.FILES.getlist('images')
            if form.is_valid():
                package_instance.packageimage_set.all().delete()
                form.save()
                for file in files:
                    package_image = PackageImage(package=package_instance, images=file)
                    package_image.save()
                messages.success(request, "Package edited successfully.")
                return HttpResponseRedirect(url)
            else:
                if "images" in form.errors:
                    messages.error(request, f'Please upload exactly five images.')
                else:
                    messages.error(request, f'Invalid input for {list(form.errors)[0]}.')
                print(form.errors)
                return HttpResponseRedirect(url)
        elif "delete_package" in request.POST:
            package_instance.delete()
            messages.success(request, "Package deleted.")
            return HttpResponseRedirect(url)
        
            


class SellerDashboardView(View):
    def get(self, request, pk, *args, **kwargs):
        seller = get_object_or_404(User, pk=pk)

        booking_headers = [
            "#",
            "Package Title",
            "Booked By",
            "Booked Date"
        ]

        packages = Package.objects.filter(package_author=seller)
        booking_values = Booking.objects.filter(package__package_author=seller)

        # For weekly bookings data
        today = timezone.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        bookings_this_week = Booking.objects.filter(
            Q(package__package_author=seller,
            booking_date__gte=start_of_week,
            booking_date__lte=end_of_week)
            &Q(status="2")
        )

        # For total sales
        total_sales = booking_values.aggregate(Sum('paid_amount')).get('paid_amount__sum')

        graph_data = list(Booking.objects.filter(
            Q(package__package_author=seller)&Q(status="2")
            ).annotate(month=TruncMonth('booking_date')).values('month').annotate(c=Count('id')).order_by('month').values('month', 'c'))

        context = {
            'booking_headers': booking_headers,
            'booking_values': bookings_this_week,
            'graph_data': graph_data,
            'total_packages': packages.count(),
            'bookings_this_week': bookings_this_week.count(),
            'total_sales': total_sales,
        }
        return render(request, 'packages/seller_dashboard.html', context)
    
    
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

        booking_list = Package.objects.prefetch_related('package').filter(
            Q(package_author=user)&Q(package__status="2")
            ).values('package__package__package_title', 'package__booked_by__username', 'package__paid_amount', 'package__booking_date')

        context = {
            'headers': headers,
            'booking_list': booking_list
        }

        return render(request, 'packages/payment_details.html', context)