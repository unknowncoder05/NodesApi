from rest_framework import serializers
from api.users.serializers import UserSerializer

from api.nodes.models import Node, ProposedRelationship


class WriteProposedRelationshipSerializer(serializers.ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProposedRelationship
        fields = ('id', 'from_node', 'to_node', 'created_by')
    
    def validate(self, data):
        from_node = data['from_node']
        to_node = data['to_node']
        if from_node == to_node:
            raise ValueError('Cannot create relationship between a node and itself')
        if from_node.proposed_relationships.filter(to_node=to_node).exists():
            raise ValueError('Relationship already exists')
        if from_node.type == to_node.type:
            raise ValueError('Cannot create relationship between same type nodes')
        return data

    def create(self, validated_data):
        return super().create(validated_data)


class ReadProposedRelationshipSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProposedRelationship
        fields = ('id', 'from_node', 'to_node', 'created_by')


class DescribeNodeSerializer(serializers.ModelSerializer):

    created_by = UserSerializer(read_only=True)
    parents = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()


    class Meta:
        model = Node
        fields = ('id', 'created_by', 'content', 'private', 'type', 'feed', 'parents', 'children')
    
    def get_parents(self, obj):
        return obj.to_node.all()
    
    def get_children(self, obj):
        return obj.from_node.all()


class ListNodeSerializer(serializers.ModelSerializer):

    parents_count = serializers.SerializerMethodField()
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Node
        fields = ('id', 'created_by', 'content', 'private', 'type', 'feed', 'parents_count', 'children_count')
    
    def get_parents_count(self, obj):
        return obj.to_node.count()
    
    def get_children_count(self, obj):
        return obj.from_node.count()


class DescribeProposedRelationshipSerializer(serializers.ModelSerializer):
    
    from_node = ListNodeSerializer()
    to_node = ListNodeSerializer()
    created_by = UserSerializer()

    class Meta:
        model = ProposedRelationship
        fields = ('id', 'from_node', 'to_node', 'created_by')


class WriteNodeSerializer(serializers.ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    parents = serializers.PrimaryKeyRelatedField(many=True, queryset=Node.objects.all(), required=False, write_only=True)
    children = serializers.PrimaryKeyRelatedField(many=True, queryset=Node.objects.all(), required=False, write_only=True)

    class Meta:
        model = Node
        fields = ('id', 'created_by', 'content', 'private', 'type', 'feed', 'parents', 'children')
        read_only_fields = ('created_by',)
        extra_kwargs = {
            'created_by': {'write_only': True},
        }

    def validate(self, data):
        if 'parents' in data:
            for parent in data['parents']:
                if parent.type == data['type']:
                    raise serializers.ValidationError('Node type must be different from parent type')
        
        if 'children' in data:
            for child in data['children']:
                if child.type == data['type']:
                    raise serializers.ValidationError('Node type must be different from child type')
        return data

    def create(self, validated_data):
        parents = validated_data.pop('parents', [])
        children = validated_data.pop('children', [])
        node = super().create(validated_data)

        self.create_children(node, children)
        self.create_parents(node, parents)
        return node

    def create_children(self, node, children):
        for child in children:
            self.create_relationship(node, child)
    
    def create_parents(self, node, parents):
        for parent in parents:
            self.create_relationship(parent, node)
    
    def create_relationship(self, from_node, to_node):
        WriteProposedRelationshipSerializer(data={
            'from_node': from_node,
            'to_node': to_node,
            'created_by': self.context['request'].user
        }).create()
