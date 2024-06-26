from django.urls import path, register_converter
from . import views

app_name = 'Payment'
urlpatterns = [
    path('config/', views.stripe_config),
    path('create-checkout-session/<int:pk>/', views.create_checkout_session, name='checkout_session'),
    path('success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('cancelled/', views.PaymentCancelledView.as_view(), name='payment_cancel'),
    path('webhook/', views.stripe_webhook, name='webhook'),
    # path('webhook/', views.StripeWebhookView.as_view(), name='webhook'),
]