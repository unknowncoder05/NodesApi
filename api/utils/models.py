from django.db import models

class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

    modified_at = models.DateTimeField(auto_now=True)

    deleted_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True
        get_latest_by = 'created_at'
        ordering = ['-created_at', '-modified_at']
