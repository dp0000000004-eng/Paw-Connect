from django.db import models
from django.conf import settings

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



class HOD_Model(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(
        Departments,
        on_delete=models.CASCADE,
        related_name="department_name"
    )
    description = models.CharField(max_length=3000)


    def __str__(self):
        return f"{self.name} {self.department} {self.description}"


class FeedBack(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.description


class Contact(models.Model):
    email = models.EmailField()
    contact_no = models.IntegerField()

    def __str__(self):
        return f"Email - {self.email} Contact - {self.contact_no}"