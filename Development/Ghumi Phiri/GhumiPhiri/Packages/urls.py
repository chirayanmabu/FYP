from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name="home"),
    path('create-package/', views.CreatePackageView.as_view(), name="create-package"),
    path('list-package/', views.ListPackageView.as_view(), name="list-package"),
    path('package-detail/<int:pk>', views.PackageDetailView.as_view(), name="package_detail"),
]