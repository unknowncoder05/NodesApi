from rest_framework import serializers

from api.feed.models import Comment
from api.users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):

    created_by = UserSerializer()

    class Meta:
        model = Comment
        fields = ('created_by', 'content', 'parent', 'feed')


class ListCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('created_by', 'content', 'comments')


class WriteCommentSerializer(serializers.ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('created_by', 'feed', 'content', 'parent')
        read_only_fields = ('created_by',)
        extra_kwargs = {
            'created_by': {'write_only': True},
            'feed': {'write_only': True},
        }
    
    def validate(self, data):
        if data['parent']:
            if data['parent'].feed != data['feed']:
                raise serializers.ValidationError('Parent comment must belong to the same feed')
        return data
