from django.db import models

from backend.labels.models import Label
from backend.statuses.models import Status
from backend.users.models import User
from django.utils import timezone


# Create your models here.
class Task(models.Model):
    name = models.CharField(unique=True)
    description = models.TextField(null=True, blank=True)
    status = models.ForeignKey(
        Status, on_delete=models.CASCADE, related_name="status", null=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author", null=True
    )
    executor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="executor", null=True
    )
    labels = models.ManyToManyField(Label, related_name="labels", blank=True)
    created_at = models.DateTimeField(default=timezone.now())
