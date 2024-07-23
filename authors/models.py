from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, default='')

    def str(self):
        return self.author.username
