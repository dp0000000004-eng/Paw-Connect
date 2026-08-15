from django.urls import path
from . import views

urlpatterns = [
    path('ai-hy/', views.hy, name='hy')
]