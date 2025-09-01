from django.db import models
from django.utils import timezone


# Create your models here.
class Label(models.Model):
    name = models.CharField()
    created_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name
