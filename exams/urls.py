from django.urls import path
from . import views

app_name = "exam"

urlpatterns = [
    path('dept/', views.departments, name="branch"),
    path('link/<int:branch_id>', views.Syllabus, name="syllabus"),
]