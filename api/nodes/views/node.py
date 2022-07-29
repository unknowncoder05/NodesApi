import re

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.nodes.models import Node
from api.nodes.serializers import (
    ListNodeSerializer, DescribeNodeSerializer, WriteNodeSerializer
)


class NodesViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = ListNodeSerializer
    
    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return WriteNodeSerializer
        if self.action == 'retrieve':
            return DescribeNodeSerializer
        return super().get_serializer_class()
