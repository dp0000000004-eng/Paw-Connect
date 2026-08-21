from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError

# Create your views here.

def home(request):

    return render(request, 'welcome.html')


def createAccount(request):

    try:
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

            messages.success(request, "Account created Sussessfully")

    except IntegrityError:
        messages.error(request, "Username exists in this name try another :( ")
        

    return render(request, 'login.html')