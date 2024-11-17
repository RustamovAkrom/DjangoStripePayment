from django.urls import path

from . import views


urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("checkout/<int:product_id>", views.create_checkout_session, name="checkout"),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
]