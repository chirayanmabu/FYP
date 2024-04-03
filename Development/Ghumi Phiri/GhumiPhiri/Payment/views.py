from datetime import timezone
from django.shortcuts import render, redirect
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import HttpResponse

import stripe, json

from Packages.models import Package, Booking


# Create your views here.
@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    

def create_checkout_session(request,pk):
    package = Package.objects.get(pk=pk)
    print(package)
    if request.method == "GET":
        print(request.GET)
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + f'success?session_id={{CHECKOUT_SESSION_ID}}&product_id={pk}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'NPR',
                            'product_data': {
                                # "id":pk,
                                'name': package.package_title,
                            },
                            'unit_amount': int(package.package_price * 100),
                        },
                        'quantity': 1,
                    }
                ]
            )

            # Booking.objects.create(booked_by=request.user, package=package, booking_date=)

            return JsonResponse({
                'sessionId': checkout_session['id']
            })
        except Exception as e:
            return JsonResponse({"error": str(e)})
        
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    # stripe_signature = request.META.get("HTTP_STRIPE_SIGNATURE")
    sig_header = request.headers.get("stripe_signature")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError as e:
        print("error")
        return HttpResponse(status=400)
    
    if event.get("type") == 'checkout.session.completed':
        session = event['data']['object']
        
        package_id = session['metadata']['product_id']
        package = Package.objects.get(pk=package_id)
        
        payment_intent_id = session['payment_intent']
        payment_status = session['payment_status']
        payment_amount = session['amount_total']
        currency = session['currency']
        
        
        booking = Booking.objects.create(
            booked_by=request.user,
            package=package,
            booking_date=timezone.now() 
        )
        print("Payment success")

    return HttpResponse(status=200)




class PaymentSuccessView(View):
    def get(self, request, *args, **kwargs):
        ''' WRITE LOGIC FOR PAYEMENT SUCCESS '''


        return render(request, 'core/payment_success.html')


class PaymentCancelledView(View):
        def get(self, request, *args, **kwargs):
            ''' '''
            return render(request, 'core/payment_cancellation.html')
        


