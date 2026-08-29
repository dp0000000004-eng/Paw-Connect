from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import HOD_Model, FeedBack
from .forms import FeedbackForm
import smtplib
from email.message import EmailMessage
from .models import Contact

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

            return redirect('user:home')

    except IntegrityError:
        messages.error(request, "Username exists in this name try another :( ")

    msg = EmailMessage()
    msg['Subject'] = "test"
    msg['From'] = "dp0000000004@gmail.com"
    msg['To'] = "rahulsahu2007@gmail.com"
    msg.set_content("hello, from project")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465 ) as server:
        server.login("dp0000000004@gmail.com", "PASSWORD")
        server.send_message(msg)


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


@login_required
def Israt(request):
    return HttpResponse("Hello From Israt")



def about_view(request):

    hods = HOD_Model.objects.all()



    return render(
        request, 
        'about.html',
        {
            "hods":hods
        }
    )

@login_required
def feedback(request):

    if request.method == "POST":

        user = User.objects.get(
            username = request.user
        )
        username = user

        description = request.POST.get('description')

        feedback = FeedBack(
            user=username,
            description=description
        )

        feedback.save()

        return redirect(
            'user:home'
        )


    return render(
        request,
        'feedback.html'
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect('user:home')


def contact_view(request):

    datas = Contact.objects.all()[0]

    return render(
        request,
        'contact.html',
        {
            'datas':datas
        }
    )

