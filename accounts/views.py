from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
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

            return redirect('home')

    except IntegrityError:
        messages.error(request, "Username exists in this name try another :( ")


    return render(
        request, 
        'create_acc.html'
    )



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:
            login(
                request,
                user
            )

            return redirect('user:home')

        else:
            messages.error(
                request,
                "Invalid Credentials! "
            )

    return render(
        request,
        'Login.html'
    )

