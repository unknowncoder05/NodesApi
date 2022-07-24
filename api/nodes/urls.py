from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'nodes', views.NodesViewSet, basename='nodes')


urlpatterns = [
    path('', include(router.urls))
]