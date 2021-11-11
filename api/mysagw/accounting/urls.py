from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"receipts", views.ReceiptViewSet, basename="receipts")

urlpatterns = r.urls
