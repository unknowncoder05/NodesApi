# Django
from django.contrib import admin

# Models
from .models import *

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'content',
    )

@admin.register(ProposedRelationship)
class ProposedRelationshipAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'from_node',
        'to_node'
    )
