from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.

def hy(request):
    return HttpResponse("Hello from Accounts")