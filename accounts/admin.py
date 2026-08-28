from django.contrib import admin
from .models import HOD_Model, Departments
from .models import Contact

# Register your models here.

admin.site.register(HOD_Model)
admin.site.register(Departments)
admin.site.register(Contact)