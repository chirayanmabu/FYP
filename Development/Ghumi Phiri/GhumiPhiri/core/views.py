from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import *
from .models import *
from core.mixins import GroupRequiredMixin
from Packages.models import Package
from Packages.filters import PackageFilter

def registerPage(request):
    """
    Allows user to register with the role of buyer.
        
    **Template:**
    :template:`core/register.html`
    """
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.role=1
            new_user.save()
            group = Group.objects.get(name='buyer')
            new_user.groups.add(group)

            messages.success(request, f'Account created!')
            return redirect('login')
        else:
            if 'email' in form.errors:
                messages.error(request, f'Enter a valid email address.')
            elif 'password1' in form.errors:
                messages.error(request, f'Password must meet requirements.')
            elif 'password2' in form.errors:
                messages.error(request, f'{form.errors.get('password2')[0]}')
            elif 'username' in form.errors:
                if User.objects.filter(username=form.cleaned_data.get('username')).exists():
                    messages.error(request, f'Email already exists.')
                else:
                    messages.error(request, f'Invalid email address.')
        
    context = {
        'form': form
    }
        
    return render(request, 'core/register.html', context)

def registerSellerPage(request):
    """
    Allows user to register with the role of seller.
        
    **Template:**
    :template:`core/login.html`
    """
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.role=2
            new_user.save()
            group = Group.objects.get(name='seller')
            new_user.groups.add(group)
            
            messages.success(request, f'Seller account created!')
            return redirect('login')
        else:
            if 'email' in form.errors:
                messages.error(request, f'Enter a valid email address.')
            elif 'password1' in form.errors:
                messages.error(request, f'Password must meet requirements.')
            elif 'password2' in form.errors:
                messages.error(request, f'{form.errors.get('password2')[0]}')
            elif 'username' in form.errors:
                if User.objects.filter(username=form.cleaned_data.get('username')).exists():
                    messages.error(request, f'Email already exists.')
                else:
                    messages.error(request, f'Invalid email address.')
        
    context = {
        'form': form
    }
        
    return render(request, 'core/login.html', context)

def loginPage(request):
    """
    Allows user to login and authenticate as a user 
    if the user provides the correct credentials.
        
    **Template:**
    :template:`core/login.html`
    """
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, f"Invalid username/password.")

    return render(request, 'core/login.html')

def logoutUser(request):
    """
    Allows the authenticated user to log out of the application.
        
    **Template:**
    :template:`core/login.html`
    """
    logout(request)
    return redirect('login')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Allows the user to reset their password through their email.
        
    **Template:**
    :template:`core/password_reset.html`
    :template:`core/password_reset_email.html`
    :template:`core/password_reset_subject.html`
    :template:`core/index.html`
    """
    template_name = 'core/password_reset.html'
    email_template_name = 'core/password_reset_email.html'
    subject_template_name = 'core/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


class ProfilePageView(LoginRequiredMixin, View):
    """
    Allows the user to access their profile page. The profile
    page displays the user's details, their favourite packages and 
    allows the user to apply filters to their favourite pacakges.
        
    **Template:**
    :template:`core/profile.html`
    """
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        # Allowing only the current authenticated user to view their profile
        if request.user.id != user.id:
            return HttpResponse(status=400)

        profile = UserProfile.objects.get(pk=pk)
        fav_packages = Package.objects.filter(favourites=request.user)

        # Filter for favourite pacakges
        package_filter = PackageFilter(request.GET, queryset=fav_packages)

        context = {
            'user': user,
            'profile': profile,
            'fav_packages': fav_packages,
            'package_filter': package_filter
        }

        return render(request, 'core/profile.html', context)
    
class ProfileEditView(LoginRequiredMixin, View):
    """
    Allows the user to update their personal details.
        
    **Template:**
    :template:`core/profile.html`
    """
    def post(self, request, pk, *args, **kwargs):
        form = UpdateProfileForm(request.POST, request.FILES, initial={'user_id': pk})
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect('profile', pk=pk)
        messages.error(request, f'Invalid input for {list(form.errors)[0]}.')
        return redirect('profile', pk=pk)
    
class SellerProfileView(View):
    """
    Retrieve the details of the users with role seller.
    The packages created by that user is also retrieved.
        
    **Template:**
    :template:`core/seller_profile.html`
    """
    def get(self, request, pk, *args, **kwargs):
        seller = get_object_or_404(User, pk=pk)
        seller_profile = UserProfile.objects.filter(user=pk).first()

        # Retrieving the seller's pacakges
        seller_packages = Package.objects.prefetch_related('packageimage_set').filter(package_author=seller)
        package_filter = PackageFilter(request.GET, queryset=seller_packages)

        context = {
            'seller': seller,
            'seller_profile': seller_profile,
            'seller_packages': package_filter
        }

        return render(request, 'core/seller_profile.html', context)
    

    
    