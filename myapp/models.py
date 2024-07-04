from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class ToDoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

