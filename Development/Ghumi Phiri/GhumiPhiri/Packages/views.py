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
    """
    Allows authenticated and unautheticated users to access the home page.
    The home page lists packages created by users with the role "seller".
    Allows the user to filter according to the packages and users.

    **Template:**
    :template:`core/index.html`
    """
    def get(self, request, *args, **kwargs):
        packages = Package.objects.prefetch_related('packageimage_set').all()
        # Get every user with the role of 2(seller)
        sellers = User.objects.filter(role=2)

        # Filter for packages
        f = PackageFilter(
            request.GET, queryset=packages
        )

        # Filter for serllers
        seller_filter = SellerFilter(request.GET, queryset=sellers)

        context = {
            'packages': packages,
            'filter': f,
            'seller_filter': seller_filter,
            'user': request.user
        }

        return render(request, 'core/index.html', context)

class CreatePackageView(LoginRequiredMixin, View):
    """
    Allows authenticated users to add new packages.

    **Template:**
    :template:`core/login.html`
    """
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
    """
    Displays a list of packages with filtering options.

    The get method retrieves all packages, applies any filters from the request, and renders the list.

    **Template:**
    Renders the 'Packages/list_packages.html' template with the package list and filter.

    **Context:**
    - package_list: A queryset of all packages.
    - package_filter: A filtered queryset based on request parameters.
    """
    def get(self, request, *args, **kwargs):
        package_list = Package.objects.prefetch_related('packageimage_set').all()
        package_filter = PackageFilter(request.GET, queryset=package_list)

        context = {
            'package_list': package_list,
            'package_filter': package_filter
        }
        return render(request, 'Packages/list_packages.html', context)
    
class ComparePackage(View):
    """
    Compares two selected packages and returns their details in a JSON response.

    The get method retrieves the details of two packages specified by the request parameters
    and returns a JSON response containing their information for comparison.

    **Response:**
    Returns a JSON response with the details of the two packages.
    """
    def get(self, request, *args, **kwargs):
        package_list = Package.objects.all()
        package_filter = PackageFilter(request.GET)

        package1_id = request.GET.get('package1')
        package2_id = request.GET.get('package2')

        # Check if the same package is selected for comparision
        if package1_id == package2_id:
            messages.error(request, f"Choose different packages.")

        # Retrieve the two packages by their IDs
        package1 = get_object_or_404(Package.objects.prefetch_related('packageimage_set'), pk=package1_id)
        package2 = get_object_or_404(Package.objects.prefetch_related('packageimage_set'), pk=package2_id)

        # Retrieve the package authors
        package1_author = {'id': package1.package_author.id, 'username': package1.package_author.username}
        package2_author = {'id': package2.package_author.id, 'username': package2.package_author.username}

        # Retrieve the package images
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
    """
    Displays the details of a specific package according to the id provided in the url
    Handles posting comments and booking the package.

    The get method retrieves the package details, images, feedbacks, and user-related information.

    The post method handles posting comments and booking the package, with appropriate form validation.

    **Template:**
    :template:`Packages/package_detail.html`
    """
    def get(self, request, pk, *args, **kwargs):
        package = Package.objects.get(pk=pk)
        # retrieve images related to the package
        package_images = PackageImage.objects.filter(package=package)
        # retrieve feedbacks related to the package
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

        # checks if the package is marked as favourite by the user
        if package.favourites.filter(id=user.id).exists():
            context["is_favourite"] = False
        else:
            context["is_favourite"] = True

        # For write a review button
        if user.is_authenticated:
            # checks if the user has already reviewed the package
            if Feedback.objects.filter(package=package, feedback_author=user).exists():
                context["user_has_reviewed"] = True
            else:
                context["user_has_reviewed"] = False

            # checks if the user has already booked the package
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

        # List of existing booking dates for the package
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
            # Post comment if the form is valid
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

            # Checks if the booking date is available
            if user_booking_date in existing_booking_dates:
                messages.error(request, f"The chosen booking date is not available.")
            else:
                # Display booking date availability message if the form is valid
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


class EditDeleteFeedbackView(LoginRequiredMixin, View):
    """
    Handles editing and deleting feedbacks for a package.

    The post method allows authenticated users to update or delete their feedback
    for a specific package provided in the url.

    **Template:**
    :template:`Packages/package_detail.html`
    """
    def post(self, request, pk, *args, **kwargs):
        feedback_instace = get_object_or_404(Feedback, pk=pk)
        package_id = feedback_instace.package.id
        url = reverse('package_detail', kwargs={"pk": package_id})
        if "update_feedback" in request.POST:
            form = CreateCommentForm(request.POST, instance=feedback_instace)
            # Update the feedback if the form is valid
            if form.is_valid():
                messages.success(request, "Feedback edited successfully.")
                form.save()
                return HttpResponseRedirect(url)
            else:
                messages.error(request, "Invalid input.")
                return HttpResponseRedirect(url)
        elif "delete_feedback" in request.POST:
            # Delete feedback
            feedback_instace.delete()
            messages.success(request, "Feedback deleted.")
            return HttpResponseRedirect(url)

        
class FavouritePackageView(LoginRequiredMixin, View):
    """
    Handles adding and removing a package from the user's favourites.

    The post method allows authenticated users to add or remove a package from their favourites list.

    **Template:**
    :template:`Packages/package_detail.html`
    """
    def post(self, request, pk, *args, **kwargs):
        try:
            package = Package.objects.get(pk=pk)
            user = request.user

            # Checks if the package is already in the user's favourites
            if package.favourites.filter(id=user.id).exists():
                # removes the package from the user's favourites
                package.favourites.remove(request.user)
                messages.error(request, f"Removed from favourites.")
            else:
                # adds the package to the user's favourites
                package.favourites.add(request.user)
                messages.success(request, f"Added to favourites.")
            return HttpResponseRedirect(reverse('package_detail', kwargs={'pk': pk}))
        except Exception:
            # Error message when user is unauthenticated
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
    """
    The get method retrieves a filtered list of seller users.

    **Template:**
    :template:`core/list_sellers.html`
    """
    def get(self, request, *args, **kwargs):
        # Filter users with the role of 'SELLER'
        sellers_qs = UserProfile.objects.filter(user__role=2)
        seller_filter = SellerFilter(request.GET, queryset=sellers_qs)

        sellers=seller_filter.qs

        context = {
            'sellers': sellers,
            'filter': seller_filter
        }

        return render(request, 'Packages/list_sellers.html', context)


class ListSellerPackages(LoginRequiredMixin, View):
    """
    The get method retrieves the currently autheticated user's packages.

    The post method allows authenticated users to add new packages if the 
    form is valid.

    **Template:**
    :template:`Packages/seller_packages.html`
    """
    def get(self, request, pk, *args, **kwargs):
        profile = User.objects.get(pk=pk)
        # Allows only the authenticated user to access their profile
        if request.user.id != profile.id:
            return HttpResponse(status=400)
        # Retrives packages created by the user.
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

        # Checks if the user uploads 5 images
        if len(files) != 5:
            messages.error(request, f'Please upload exactly five images.')
            return render(request, 'Packages/seller_packages.html', context)
        
        # Creating new package if the form is valid
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
    

class ManageSellerPackages(LoginRequiredMixin, View):
    """
    Handles the updating and deleting of seller packages.

    The post method allows authenticated users to update or delete their packages 
    based on the form submission.

    **Template:**
    :template:`Packages/seller_packages.html`
    """
    def post(self, request, pk, *args, **kwargs):
        package_instance = get_object_or_404(Package, pk=pk)
        # Reverse the URL to redirect to the seller's package list
        url = reverse("my_packages", kwargs={"pk": package_instance.package_author.id})
        if "update_package" in request.POST:
            form = ImageForm(request.POST, request.FILES, instance=package_instance)
            files = request.FILES.getlist('images')
            # updating package if the form is valid
            if form.is_valid():
                # delete existing images
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
            # deletes the package
            package_instance.delete()
            messages.success(request, "Package deleted.")
            return HttpResponseRedirect(url)
        
            


class SellerDashboardView(LoginRequiredMixin, View):
    """
    Displays the seller's dashboard with booking and sales information.

    The get method retrieves the seller's packages, bookings, and sales data
    and displays it on the dashboard.

    **Template:**
    :template:`packages/seller_dashboard.html`
    """
    def get(self, request, pk, *args, **kwargs):
        seller = get_object_or_404(User, pk=pk)
        # Allows only the authenticated seller to access their dashboard
        if request.user.id != seller.id:
            return HttpResponse(status=400)
        booking_headers = [
            "#",
            "Package Title",
            "Booked By",
            "Booked Date"
        ]

        # Retrieve all packages authored by the seller
        packages = Package.objects.filter(package_author=seller)
        # Retrieve all bookings for packages authored by the seller
        booking_values = Booking.objects.filter(package__package_author=seller)

        # For weekly bookings data
        today = timezone.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Retrieve bookings for the current week that are confirmed (status = "2")
        bookings_this_week = Booking.objects.filter(
            Q(package__package_author=seller,
            booking_date__gte=start_of_week,
            booking_date__lte=end_of_week)
            &Q(status="2")
        )

        # For total sales
        total_sales = booking_values.aggregate(Sum('paid_amount')).get('paid_amount__sum')

        # Data of bookings for each month (grouped by month)
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
    
    
class ListPaymentDetails(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """
        Displays the payment details for the authenticated user's packages.

        The get method retrieves the payment details of the packages authored by the
        currently authenticated user and displays them on the payment details page.

        **Template:**
        :template:`packages/payment_details.html`
        """
        user = request.user

        headers = [
            'S no.',
            'Package Title',
            'Booked By',
            'Paid Amount',
            'Booked date',
        ]

        # Retrieve the payment details for the packages authored by the user
        booking_list = Package.objects.prefetch_related('package').filter(
            Q(package_author=user)&Q(package__status="2")
            ).values('package__package__package_title', 'package__booked_by__username', 'package__paid_amount', 'package__booking_date')

        context = {
            'headers': headers,
            'booking_list': booking_list
        }

        return render(request, 'packages/payment_details.html', context)