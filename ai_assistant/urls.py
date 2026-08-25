from django.urls import path
from . import views

app_name = "ai"

urlpatterns = [
    path('paw-ai/', views.chat, name="ai"),
]