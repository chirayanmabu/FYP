from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.HomePageView.as_view(), name="home"),

    path('profile/<int:pk>/', views.ProfilePageView.as_view(), name="profile"),
    path('profile-edit/<int:pk>/', views.ProfileEditView.as_view(), name="profile-edit"),

    path('create-package/', views.CreatePackageView.as_view(), name="create-package"),
    path('list-package/', views.ListPackageView.as_view(), name="list-package"),
    path('package-detail/<int:pk>', views.PackageDetailView.as_view(), name="package_detail"),
]