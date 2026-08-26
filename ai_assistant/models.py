from django.db import models
from django.conf import settings

# Create your models here.


class Chat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=3000)
    response = models.CharField(max_length=3000)

    def __str__(self):
        return self.prompt