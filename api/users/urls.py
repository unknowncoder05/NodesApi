from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', views.UserViewSet, basename='invitation')


urlpatterns = [
    path('', include(router.urls))
]