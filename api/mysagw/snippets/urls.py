from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"snippets", views.SnippetViewSet)

urlpatterns = r.urls
