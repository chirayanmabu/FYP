from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from Packages.models import Package

def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.role=1
            new_user.save()

            print("success")
            return redirect('login')
        
    context = {
        'form': form
    }
        
    return render(request, 'core/register.html', context)

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print('error')

    return render(request, 'core/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')


class ProfilePageView(View, LoginRequiredMixin):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user

        context = {
            'user': user,
            'profile': profile,
        }

        return render(request, 'core/profile.html', context)
    
class ProfileEditView(View):

    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user

        context = {
            'user': user,
            'profile': profile,
        }
        return render(request, 'core/profileEdit.html', context)

    def post(self, request, pk, *args, **kwargs):
        form = UpdateProfileForm(request.POST, request.FILES, initial={'user_id': pk})
        if form.is_valid():
            form.save()
            return redirect('profile', pk=pk)
        print(form.errors)
        return redirect('profile-edit', pk=pk)
    
class SellerProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        seller = get_object_or_404(User, pk=pk)
        seller_profile = UserProfile.objects.filter(user=pk).first()
        seller_packages = Package.objects.filter(package_author=seller)

        context = {
            'seller': seller,
            'seller_profile': seller_profile,
            'seller_packages': seller_packages
        }

        return render(request, 'core/seller_profile.html', context)
    

    
    