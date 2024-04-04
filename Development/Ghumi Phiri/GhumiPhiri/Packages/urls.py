from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name="home"),
    path('create-package/', views.CreatePackageView.as_view(), name="create-package"),
    path('list-package/', views.ListPackageView.as_view(), name="list-package"),
    path('package-detail/<int:pk>', views.PackageDetailView.as_view(), name="package_detail"),
    path('add-feedback/<int:pk>', views.WriteReview.as_view(), name="add_feedback"),

    path('my-packages/<int:pk>', views.ListSellerPackages.as_view(), name="my_packages"),
    path('payment-details/', views.ListPaymentDetails.as_view(), name="payment_details"),
]