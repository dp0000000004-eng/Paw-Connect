from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hy(request):
    return render(request, 'exams/exam.html')


def rahul():
    return "This line is made by rahul"