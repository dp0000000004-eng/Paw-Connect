
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import HOD_Model, FeedBack
from django.core.mail import send_mail
import os
import logging
import requests
from .models import Contact


# ---------------------------------------------------------------------------
# HOME
# Shows the welcome / landing page (welcome.html)
# ---------------------------------------------------------------------------
def home(request):
    return render(request, 'welcome.html')


def createAccount(request):

    try:
        with transaction.atomic():
            
        # Form was submitted (not just opening the page)
            if request.method == "POST":

                # Values typed in the signup form
                username = request.POST.get('username')
                email = request.POST.get('email')
                raw_password = request.POST.get('password')

                # New user object (password is set separately so it is hashed)
                user = User(
                    username=username,
                    email=email
                )

                # Hash the password before saving (never store plain text in DB)
                user.set_password(raw_password)

                send_welcome_email(username, email)

                # Write the user to the database
                user.save()
                # After signup, send them to the home page
                return redirect('user:home')

    # Username (or another unique field) already taken
    except IntegrityError:
        messages.error(request, "Username exists in this name try another :( ")

    # GET request, or signup failed: show the form again
    return render(
        request,
        'create_acc.html'
    )


logger = logging.getLogger(__name__)

def send_welcome_email(username, email):
    try:
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "api-key": os.environ.get('BREVO_API_KEY'),
                "Content-Type": "application/json",
            },
            json={
                "sender": {"name": "PawBytes Team", "email": os.environ.get('EMAIL_HOST_USER')},
                "to": [{"email": email, "name": username}],
                "subject": "Your PawConnect account is ready",
                "textContent": f"""
                            Hi {username},
            
                    Welcome to PawConnect — your college portal for attendance, notices, 
                    exam results, and your AI study assistant, Paw AI.
            
                    Your account has been created successfully. Here's what you can do next:
            
                    - Practice with Paw AI before your next exam
                    - View the latest notices
                    - Can Know Closely about our collage
            
            
                    Thanks,
                    The PawBytes Team
            
                    ---
                    PawConnect | Govt. Polytechnic Angul, Odisha
                            """,
            },
            timeout=5,  
        )
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to send welcome email: {e}")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Returns a User if credentials match, otherwise None
        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:
            # Create the logged-in session (request.user becomes this user)
            login(
                request,
                user
            )

            return redirect('user:home')

        else:
            # Wrong username or password
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
            "hods": hods
        }
    )


@login_required
def feedback(request):

    if request.method == "POST":

        # Logged-in user from the session
        user = User.objects.get(
            username=request.user
        )
        username = user

        # Text from the feedback form
        description = request.POST.get('description')

        feedback = FeedBack(
            user=username,
            description=description
        )

        feedback.save()

        return redirect(
            'user:home'
        )

    feedbacks = FeedBack.objects.all()

    return render(
        request,
        'feedback.html',
        {
            'feedbacks':feedbacks
        }
    )


@login_required
def logout_view(request):
    logout(request)
    return redirect('user:home')


def contact_view(request):

    try:

        datas = Contact.objects.all()[0]

    except IndexError:
        return redirect('user:home')
    
    return render(
        request,
        'contact.html',
        {
            'datas': datas
        }
    )
