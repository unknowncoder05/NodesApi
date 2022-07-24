# Django
from django.db import models

from api.utils.models import BaseModel
from api.users.models import User
from api.feed.models import Feed


class Comment(BaseModel):
    

    class Meta:
        default_related_name = 'comments'
    
    content = models.CharField(max_length=200)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
