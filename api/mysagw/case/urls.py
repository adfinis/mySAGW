from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"case/accesses", views.CaseAccessViewSet)
r.register(r"downloads", views.CaseDownloadViewSet, basename="downloads")

urlpatterns = r.urls
