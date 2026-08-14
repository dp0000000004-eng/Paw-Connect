from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hy(request):
    return render(request, 'exams/exam.html')