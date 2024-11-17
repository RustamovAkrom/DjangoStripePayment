from django.utils.translation import gettext_lazy as _
from django.db import models


class Product(models.Model):
    stripe_proudct_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    currency = models.CharField(max_length=10, default="usd")
    amount = models.PositiveIntegerField(help_text="Amount in sentes, example, 2000 to $20.00")
    active = models.BooleanField(blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        db_table = "products"
    
    def __str__(self) -> str:
        return self.name


class PaymentSession(models.Model):
    stripe_session_id = models.CharField(max_length=255, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_email = models.EmailField(blank=True, null=True) # Client e-mail
    currency = models.CharField(max_length=10, default="usd")
    amount_total = models.PositiveIntegerField()
    status = models.CharField(max_length=50, blank=True, null=True) # Session status
    payment_status = models.CharField(max_length=50, blank=True, null=True) # Payment status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Payment Session")
        verbose_name_plural = _("Pyament Sessions")
        db_table = "payment_sessions"

    def __str__(self) -> str:
        return f"Session {self.stripe_session_id} = {self.status}"
