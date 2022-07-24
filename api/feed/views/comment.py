import re

from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.feed.models import Comment
from api.feed.serializers import (
    CommentSerializer, ListCommentSerializer, WriteCommentSerializer
)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = ListCommentSerializer
    
    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return WriteCommentSerializer
        elif self.action == 'retrieve':
            return CommentSerializer
        return super().get_serializer_class()
