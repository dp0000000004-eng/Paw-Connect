from django.urls import path
from . import views

app_name = 'user'


urlpatterns = [
    path('home/', views.home, name="home"),
    path('Create/', views.createAccount, name="create_account"),
    path('login/', views.login_view, name="login"),
    path('israt/', views.Israt, name="israt"),
    path('about/', views.about_view, name="about"),
    path('feedback/', views.feedback, name="feedback"),
    path('contact/', views.contact_view, name="contact"),
    path('logout/', views.logout_view, name="logout"),
]