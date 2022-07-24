from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'comment', views.CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls))
]
