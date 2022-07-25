from turtle import title
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Database for our project

class Task(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank= True)  # on_delete = what happens when deleted
    title = models.CharField(max_length=200)                      # Single line strings
    description = models.TextField(null = True, blank= True)       # Multi-line Strings
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):      # When we want to print object
        return self.title

    class Meta:                # Order list item on the basis of completed status
        ordering = ['complete']
