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

def registerPage(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

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

def homePage(request):
    context = {

    }
    return render(request, 'core/index.html', context)

class HomePageView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.get.objects.get(pk=pk)
        context = {
            'profile': profile,
        }

        return render(request, 'core/index.html', context)


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
    

class CreatePackageView(View):
    def get(self, request, *args, **kwargs):
        form = CreatePackageModelForm()
        context = {
            'form': form
        }
        return render(request, 'core/create_package.html', context)

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
        return render(request, 'core/create_package.html', context)
    

class ListPackageView(View):
    def get(self, request, *args, **kwargs):
        package_list = Package.objects.all()
        context = {
            'package_list': package_list
        }
        return render(request, 'core/list_packages.html', context)
    

class PackageDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        package = Package.objects.get(pk=pk)
        context = {
            'package': package
        }

        return render(request, 'core/package_detail.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        package = Package.objects.get(pk=pk)
        form = CreateCommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.feedback_author = request.user
            new_comment.package = package
            new_comment.save()
            print("Posted review")

        else:
            print(form.errors)

        context = {
            'package': package,
            'form': form
        }

        return render(request, 'core/package_detail.html', context)

    
    