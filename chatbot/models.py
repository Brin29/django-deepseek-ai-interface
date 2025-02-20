from django.db import models

# Create your models here.
class Chat(models.Model):
    message = models.FileField()
    response = models.TextField()