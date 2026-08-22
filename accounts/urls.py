from django.urls import path
from . import views

app_name = 'user'


urlpatterns = [
    path('home/', views.home, name="home"),
    path('Create/', views.createAccount, name="create_account"),
    path('login/', views.login_view, name="login"),
]