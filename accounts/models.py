from django.db import models

# Create your models here.

class Collage_Meta_Data(models.Model):
    name = models.CharField(max_length=255)
    start_in = models.SmallIntegerField(
        null=True,
        blank=True
    )
    
