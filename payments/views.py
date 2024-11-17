from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse

from .models import Product, PaymentSession

import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


def product_list(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})


def create_checkout_session(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': product.amount,
            },
            'quantity': int(product.quantity)
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse("success")),
        cancel_url=request.build_absolute_uri(reverse("cancel")),
    )

    PaymentSession.objects.create(
        stripe_session_id=checkout_session.id,
        product=product,
        customer_email=request.user.email if request.user.is_authenticated else None,
        currency=product.currency,
        amount_total=product.amount,
        status=checkout_session.status,
        payment_status=checkout_session.payment_status,
    )

    return redirect(checkout_session.url)


def cancel(request):
    return render(request, "cancel.html")


def success(request):
    return render(request, "success.html")
