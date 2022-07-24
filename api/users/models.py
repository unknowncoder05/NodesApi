import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class IdentityProviders(models.TextChoices):
        GOOGLE = 'GO', 'google-oauth2'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auth0_id = models.CharField(default='', max_length=100)

    def __str__(self):
        return self.username
