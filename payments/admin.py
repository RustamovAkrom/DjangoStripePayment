from django.contrib import admin

from .models import Product, PaymentSession


admin.site.register([Product, PaymentSession])
