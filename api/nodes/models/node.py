# Django
from django.db import models

# Models
from api.utils.models import BaseModel
from api.users.models import User
from api.feed.models import Feed


class NodeTypes(models.TextChoices):
    QUESTION = 'QUESTION', 'q'
    ANSWER = 'ANSWER', 'a'


class Node(BaseModel):
    

    class Meta:
        default_related_name = 'nodes'
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    content = models.CharField(max_length=200)

    type = models.CharField(max_length=200, choices=NodeTypes.choices)

    private = models.BooleanField(default=False)

    feed = models.ForeignKey(Feed, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.content} {self.created_by} {self.type}'
    
    @property
    def parents_count(self):
        return self.to_node.count()
    
    @property
    def children_count(self):
        return self.from_node.count()
    

class ProposedRelationship(BaseModel):
    
    class Meta:
        default_related_name = 'proposed_relationships'
    
    from_node = models.ForeignKey(Node, related_name='to_nodes', on_delete=models.CASCADE)

    to_node = models.ForeignKey(Node, related_name='from_nodes', on_delete=models.CASCADE)
    
    created_by = models.ForeignKey(User, related_name='proposed_relationships', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.from_node} {self.type} {self.to_node}'

    def save(self, *args, **kwargs):
        if self.from_node == self.to_node:
            raise ValueError('Cannot create relationship between a node and itself')
        if self.from_node.from_nodes.filter(to_node=self.to_node).exists():
            raise ValueError('Relationship already exists')
        if self.from_node.type == self.to_node.type:
            raise ValueError('Cannot create relationship between same type nodes')
        super().save(*args, **kwargs)
        