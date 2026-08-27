from django.db import models
from accounts.models import Departments

# Create your models here.


class Semester(models.Model):
    semester = models.SmallIntegerField()

    def __str__(self):
        return f"{self.semester}"


class Syllabus(models.Model):
    branch = models.ForeignKey(
        Departments,
        on_delete=models.CASCADE,
        related_name="dep_branch"
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name="semester_model",
        null=True
    )
    link = models.URLField()

    def __str__(self):
        return self.link