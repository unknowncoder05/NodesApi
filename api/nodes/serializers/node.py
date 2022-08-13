from cmath import log
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
        if from_node.from_nodes.filter(to_node=to_node).exists():
            raise ValueError('Relationship already exists')
        return data

    def create(self, validated_data):
        return super().create(validated_data)


class ReadProposedRelationshipSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProposedRelationship
        fields = ('id', 'from_node', 'to_node', 'created_by')


class DescribeNodeSerializer(serializers.ModelSerializer):

    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Node
        fields = ('id', 'created_by', 'content', 'private', 'feed', 'parents_count', 'children_count')


class ListNodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        fields = ('id', 'created_by', 'content', 'private', 'feed', 'parents_count', 'children_count')


class ReadProposedFromRelationshipSerializer(serializers.ModelSerializer):
    
    from_node = ListNodeSerializer()

    class Meta:
        model = ProposedRelationship
        fields = ('id', 'from_node', 'created_by')


class ReadProposedToRelationshipSerializer(serializers.ModelSerializer):
    
    to_node = ListNodeSerializer()
    
    class Meta:
        model = ProposedRelationship
        fields = ('id', 'to_node', 'created_by')


class DescribeProposedRelationshipSerializer(serializers.ModelSerializer):
    
    from_node = ListNodeSerializer()
    to_node = ListNodeSerializer()
    created_by = UserSerializer()

    class Meta:
        model = ProposedRelationship
        fields = ('id', 'from_node', 'to_node', 'created_by')


class WriteNodeSerializer(serializers.ModelSerializer):

    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    from_nodes = serializers.PrimaryKeyRelatedField(many=True, queryset=Node.objects.all(), required=False, write_only=True)
    to_nodes = serializers.PrimaryKeyRelatedField(many=True, queryset=Node.objects.all(), required=False, write_only=True)

    class Meta:
        model = Node
        fields = ('id', 'created_by', 'content', 'private', 'feed', 'from_nodes', 'to_nodes')
        read_only_fields = ('created_by',)
        extra_kwargs = {
            'created_by': {'write_only': True},
        }

    def validate(self, data):
        return data

    def create(self, validated_data):
        from_nodes = validated_data.pop('from_nodes', [])
        to_nodes = validated_data.pop('to_nodes', [])
        node = super().create(validated_data)

        self.create_to(node, to_nodes)
        self.create_from(node, from_nodes)
        return node
    
    def update(self, instance, validated_data):
        from_nodes = validated_data.pop('from_nodes', [])
        to_nodes = validated_data.pop('to_nodes', [])
        super().update(instance, validated_data)

        self.create_to(instance, to_nodes)
        self.create_from(instance, from_nodes)
        return instance

    def create_to(self, node, to_nodes):
        for to_node in to_nodes:
            self.create_relationship(node, to_node)
    
    def create_from(self, node, from_nodes):
        for from_node in from_nodes:
            self.create_relationship(from_node, node)
    
    def create_relationship(self, from_node, to_node):
        serializer = WriteProposedRelationshipSerializer(data={
            'from_node': from_node.id,
            'to_node': to_node.id,
        }, context=self.context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
