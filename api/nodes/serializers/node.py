from rest_framework import serializers
from api.users.serializers import UserSerializer

from api.nodes.models import Node


class NodeSerializer(serializers.ModelSerializer):


    class Meta:
        model = Node
        fields = ('created_by', 'name', 'private')


class ListNodeSerializer(serializers.ModelSerializer):
    
        class Meta:
            model = Node
            fields = ('created_by', 'name', 'private')


class WriteNodeSerializer(serializers.ModelSerializer):
        
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Node
        fields = ('created_by', 'name', 'private')
        read_only_fields = ('created_by',)
        extra_kwargs = {
            'created_by': {'write_only': True}
        }
