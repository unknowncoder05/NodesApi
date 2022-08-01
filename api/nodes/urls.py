from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'nodes', views.NodesViewSet, basename='nodes')
router.register(r'relationships', views.NodeRelationshipsViewSet, basename='nodes_relationships')


urlpatterns = [
    path('', include(router.urls))
]
