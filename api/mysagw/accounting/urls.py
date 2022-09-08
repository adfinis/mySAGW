from django.urls import path

from . import views

urlpatterns = [
    path("receipts/<uuid:pk>", views.ReceiptView.as_view(), name="receipts"),
]
