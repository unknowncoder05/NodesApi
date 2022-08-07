import re

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.db.models import Q

from api.nodes.models import Node, ProposedRelationship
from api.nodes.serializers import (
    ListNodeSerializer, ReadProposedFromRelationshipSerializer,
    ReadProposedToRelationshipSerializer, DescribeProposedRelationshipSerializer,
    WriteProposedRelationshipSerializer, DescribeNodeSerializer, WriteNodeSerializer,
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


class NodeRelationshipsViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = DescribeProposedRelationshipSerializer

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return WriteProposedRelationshipSerializer
        if self.action == 'retrieve':
            return DescribeProposedRelationshipSerializer
        if self.action in ['list']:
            if self.request.query_params.get('from_node'):
                return ReadProposedFromRelationshipSerializer
            if self.request.query_params.get('to_node'):
                return ReadProposedToRelationshipSerializer
        return super().get_serializer_class()

    def get_queryset(self, **kwargs):
        if 'from_node' in kwargs:
            self.node = get_object_or_404(Node, id=kwargs['node'])
            return ProposedRelationship.objects.filter(from_node=self.node)
        if 'to_node' in kwargs:
            self.node = get_object_or_404(Node, id=kwargs['node'])
            return ProposedRelationship.objects.filter(to_node=self.node)
        return ProposedRelationship.objects.all()
