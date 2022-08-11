from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r"healthz", views.HealthzView.as_view(), name="healthz"),
]
