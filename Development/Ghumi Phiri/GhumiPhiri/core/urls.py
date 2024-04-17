from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('register-seller/', views.registerSellerPage, name="register_seller"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('password-reset/', views.ResetPasswordView.as_view(), name="password_reset"),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'),
    name='password_reset_complete'),

    path('profile/<int:pk>/', views.ProfilePageView.as_view(), name="profile"),
    path('profile-edit/<int:pk>/', views.ProfileEditView.as_view(), name="profile-edit"),

    path('seller-profile/<int:pk>/', views.SellerProfileView.as_view(), name="seller_profile"),
]