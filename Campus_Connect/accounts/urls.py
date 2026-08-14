from django.urls import path
from . import views

urlpatterns = [
    path('acc-hy/', views.hy, name='hy')
]