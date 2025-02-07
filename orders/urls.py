from django.urls import path

from . import views

urlpatterns = [
    path("list", views.indexOrders, name="order-list"),
]