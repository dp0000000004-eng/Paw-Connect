from django.shortcuts import render
from django.http import HttpResponse 
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def home(request):

    return render(request, 'welcome.html')


def login_view(request):
    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        raw_password = request.POST.get('password')

        user = User(
            username=username,
            email=email
        )
        user.set_password(raw_password)

        user.save()

        messages.success(
            request,
            message="Account Created Successfully"
        )

    else:

        messages.error(
            request,
            message="Something Went Wrong :( "
        )