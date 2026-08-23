from django.db import models

# Create your models here.

class Collage_Meta_Data(models.Model):
    name = models.CharField(max_length=255)
    start_in = models.SmallIntegerField(
        null=True,
        blank=True
    )

    
class Departments(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=24)

    def __str__(self):
        return f"{self.name}({self.code})"



class Students(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    branch = models.ForeignKey(
        Departments,
        on_delete=models.CASCADE,
        related_name="Branch"
    )
    register_no = models.CharField(max_length=24)
    phone_no = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.branch}"