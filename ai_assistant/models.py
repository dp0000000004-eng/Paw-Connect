from django.db import models

# Create your models here.


class Chat(models.Model):
    prompt = models.CharField(max_length=3000)
    response = models.CharField(max_length=3000)

    def __str__(self):
        return self.prompt