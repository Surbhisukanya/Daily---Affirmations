from django.db import models
from django.contrib.auth.models import User

class Affirmation(models.Model):
    text = models.TextField()
    category = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
