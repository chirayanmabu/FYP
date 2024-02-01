from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.homePage, name="home"),

    path('profile/<int:pk>/', views.ProfilePageView.as_view(), name="profile"),
    path('profile-edit/<int:pk>/', views.ProfileEditView.as_view(), name="profile-edit"),

    path('create-package/', views.CreatePackageView.as_view(), name="create-package"),
]