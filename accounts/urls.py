from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('Create/', views.createAccount, name="create_account"),
]