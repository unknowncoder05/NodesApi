# Django
from django.db import models

# Models
from api.users.models import User


class NodeTypes(models.TextChoices):
    QUESTION = 'QUESTION', 'q'
    ANSWER = 'ANSWER', 'a'


class Feed(models.Model):
    

    class Meta:
        default_related_name = 'feed'
    
