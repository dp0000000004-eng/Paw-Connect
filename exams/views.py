from django.shortcuts import render
from .models import Syllabus

# Create your views here.

def syllabus(request):
    syllabuss = Syllabus.objects.all()

    return render(
        request,
        'exams/exam.html',
        {
            "syllabuss":syllabuss
        }
    )