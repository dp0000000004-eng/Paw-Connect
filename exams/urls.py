from django.urls import path
from . import views

urlpatterns = [
    path('exams-hy/', views.hy, name='hy')
]