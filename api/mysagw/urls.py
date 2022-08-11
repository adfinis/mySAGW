from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path("api/v1/", include("mysagw.identity.urls")),
    path("api/v1/", include("mysagw.snippets.urls")),
    path("api/v1/", include("mysagw.accounting.urls")),
    path("api/v1/", include("mysagw.case.urls")),
    path("api/v1/", include("mysagw.healthz.urls")),
]
